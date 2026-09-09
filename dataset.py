import os
import csv
import json
import torch
import numpy as np
import torchaudio
import sys
import random
import pandas as pd
import yaml
from torch.utils.data import DataLoader

import querymaker

#add the paths as expected by FlowSep
sys.path.append("FlowSep/src")
from utilities.data.dataset import AudioDataset
from utilities.tools import load_json

class MusicAudioDataset(AudioDataset):
    def __init__(
            self,
            config=None,
            split="train",
            waveform_only=False,
            add_ons = [],
            size_limit = -1
        ):
        self.config = config
        self.bigvgan = False
        self.split = split
        self.pad_wav_start_sample = 0 # If none, random choose
        self.waveform_only = waveform_only
        self.metadata_root = load_json(self.config["metadata_root"])
        self.mix_channels = config["data"].get("mix_channels", -1) # -1 for random number of mixing samples
        self.label_drop_rate = config["data"].get("label_drop_rate", 0.1)
        self.generate_caption = self.config["data"]["generate_caption"]
        self.dataset_name = self.config["data"][self.split]
        self.add_ons = [eval(x) for x in add_ons]
        self.build_setting_parameters()
        self.build_dataset()
        self.build_dsp()
        self.size_limit = size_limit
        self.label_num = 0
        self.retrival=False
        self.re_num=0
        if self.split == "test":
            self.generate_caption = False

    def __getitem__(self, index):
        (
            fname,
            waveform,
            stft,
            log_mel_spec,
            label_vector,  # the one-hot representation of the audio class
            (datum, mix_datum),
            random_start,
            fcaption,
            cur_label,
        ) = self.feature_extraction(index,self.retrival,self.re_num)

        text = fcaption


        mixed_waveform, mixed_mel  = self.generate_audio_mix(fname,waveform.numpy(),index)


        data = {
        "fname": fname,  # list
        "text": text,  # list
        "label_vector": label_vector.float(),
        "waveform": waveform.float(),
        "stft": "" if(stft is None) else stft.float(),  
        "log_mel_spec": "" if(log_mel_spec is None) else log_mel_spec.float(),
        "duration": self.duration,
        "sampling_rate": self.sampling_rate,
        "random_start_sample_in_original_audio_file": random_start,
        "mixed_waveform":mixed_waveform.float(),
        "mixed_mel":mixed_mel.float(),
        "caption":fcaption,
        }
        return data

    def feature_extraction(self, index,retrival=False,re_num=0):
        if index > len(self.index_data) - 1:
            print(
                "The index of the dataloader is out of range: %s/%s"
                % (index, len(self.index_data))
            )
            index = random.randint(0, len(self.index_data) - 1)

        fname = "none"

        # Read wave file and extract feature
        while True:
            try:
                label_indices = np.zeros(self.label_num, dtype=np.float32)
                # if random.random() < self.mixup:

                index_f, index_t = self.index_data[index]

                datum = self.data[index_f]["tracks"][index_t]
                fname = os.path.join(self.data[index_f]["path"], datum["file_name"])
                log_mel_spec, stft, mix_lambda, waveform, random_start = self.read_audio_file(fname)
                mix_datum = None
                
                # If the key "label" is not in the metadata, return all zero vector
                label_indices = torch.FloatTensor(label_indices)
                break
            except Exception as e:
                index = (index + 1) % len(self.index_data)
                print("Error encounter during audio feature extraction: ", e, fname)
                break
        if self.generate_caption:
            fcaption = querymaker.generate_query(
                label_drop_rate=self.label_drop_rate,
                instrument=datum.get("instrument", ""), 
                role=datum.get("role", ""),
                melody=datum.get("melody", ""),
                rhythm=datum.get("rhythm", ""),
                technique=datum.get("technique", ""),
                genre=datum.get("genre", ""),
                dynamics=datum.get("dynamics", ""),
                effect=datum.get("effect", "")
                )
        else:
            fcaption = datum["query"]
        waveform = torch.FloatTensor(waveform)

        return (fname, waveform, stft, log_mel_spec, label_indices, (datum, mix_datum), random_start, fcaption, "Music")

    def build_dataset(self):
        self.data = []
        self.index_data = []
        print("Build dataset split %s from %s" % (self.split, self.dataset_name))
        if type(self.dataset_name) is str:
            with open(self.metadata_root[self.dataset_name][self.split]) as f:
                data_json = json.load(f)
            self.data = list(data_json.values())
        elif type(self.dataset_name) is list:
            pass

        for i in range(len(self.data)):
            for j in range(len(self.data[i]["tracks"])):
                self.index_data.append((i, j))

    def __len__(self):
        if self.size_limit > 0:
            return self.size_limit
        return len(self.index_data)

    def generate_audio_mix(self, fname, waveform, index):
        index_f, index_t = self.index_data[index]
        tracks = self.data[index_f]["tracks"].copy()
        tracks.pop(index_t)

        k = self.mix_channels
        if k < 1:
            k = random.randint(1, 5)
        mix_tracks = random.sample(tracks, min(k, len(tracks)))

        waveforms = waveform
        for track in mix_tracks:
            w, _ = self.read_wav_file(os.path.join(self.data[index_f]["path"], track["file_name"]))
            waveforms = np.append(waveforms, w, axis=0)

        mixed_waveform = self.mix_waveforms(waveforms)
        mixed_mel, stft = self.wav_feature_extraction(mixed_waveform.reshape(1,-1))

        return torch.from_numpy(mixed_waveform.reshape(1,-1)), mixed_mel

    #since in music, multitracks the stems are already the correct gain, we don't need to do normalisation
    def mix_waveforms(self, waveforms):
        mixture = waveforms.sum(axis=0)
        peak = np.absolute(mixture).max()

        if peak > 0.95:
            mixture = mixture * (0.95 / peak)
        return mixture

    def read_wav_file(self, filename):
        # waveform, sr = librosa.load(filename, sr=None, mono=True) # 4 times slower
        waveform, sr = torchaudio.load(filename)

        waveform = self.resample(waveform, sr)
        # random_start = int(random_start * (self.sampling_rate / sr))

        waveform = waveform.numpy()[0, ...]
        
        if(self.trim_wav):
            waveform = self.trim_wav(waveform)

        waveform = waveform[None, ...]
        waveform = self.pad_wav(waveform, target_length = int(self.sampling_rate * self.duration))
        return waveform, 0