import random

translations_instrument = {
    "trumpet": ["A trumpet", "A brass instrument"],
    "synth_organ_bass": ["An organ bass synthesizer", "A bass synth", "A bass synthesizer"],
    "sax_tenor": ["A tenor saxophone"],
    "sitar": ["A sitar"],
    "piano_electric": ["An electric piano", "An electronic piano"],
    "drum_kit": ["A drum kit", "A drum set"],
    "guitar_acoustic": ["An acoustic guitar"],
    "shakuhachi": ["A shakuhachi", "A bamboo flute"],
    "piano": ["A piano"],
    "cello": ["A cello", "A violoncello"],
    "morin_khuur": ["A morin khuur", "A horsehead fiddle"],
    "balalaika": ["A balalaika"],
    "double_bass_plucked": ["A plucked double bass", "A plucked string bass", "A pizzicato bass", "A pizzicato double bass", "A pizzicato string bass"],
    "ukulele": ["A ukulele"],
    "flugelhorn": ["A flugelhorn", "A flugel horn"],
    "piano_bright": ["A piano", "A bright piano"],
    "violin": ["A violin"],
    "viola": ["A viola"],
    "guitar_electric_clean": ["A clean electric guitar"],
    "panpipes": ["A pan flute", "A set of panpipes"],
    "fujara": ["A fujara", "A tabor pipe"],
    "guitar_electric_distorted": ["A distorted electric guitar", "A dirty electric guitar"],
    "clarinet": ["A clarinet"],
    "flute": ["A flute"],
    "bass_guitar": ["A bass guitar", "An electric bass"],
    "double_bass": ["A bowed double bass", "A bowed string bass", "An arco bass", "An arco double bass"],
    "sax_alto": ["A saxophone", "An alto saxophone"],
    "erhu": ["An erhu", "A chinese violin", "A two stringed fiddle"],
    "trombone": ["A trombone", "A brass instrument"],
    "jinghu": ["A jinghu", "a chinese violin", "A two stringed fiddle"],
    "brass": ["A brass instrument", "An unknown brass instrument", "A brass section"],
    "organ": ["An organ"],
    "percussion": ["Assorted percussion", "Untuned percussion", "A-tonal percussion"],
    "synth_bass": ["A bass synth", "A bass synthesizer"],
    "percussion_pitched": ["Tuned percussion", "Assorted percussion", "A pitched percussion section"],
    "lead_male_singer": ["A male vocalist", "A male voice", "A solo male singer", "A male singer"],
    "lead_female_singer": ["A female vocalist", "A female voice", "A solo female singer", "A female singer"],
    "background_vocals": ["Backing vocalist(s)", "Backing vocals", "A backing group", "Some background vocals", "A background voice"],
    "synth_lead": ["A synth lead", "A synthesizer lead"],
    "synth_lead": ["A synth pad", "A synthesizer pad"],
    "drum_machine": ["A drum machine", "A synth drum"],
    "string_section": ["A string section", "Mixed string instruments", "A strings group"],
    "": ["An unknown instrument"]
    }

translations_role = {
    "melody": ["the main melody", "a melodic part", "a lead part", "the leading role", "the tune"],
    "harmony": ["a harmony", "a backing part"],
    "chords": ["the chords of the piece", "a chord harmony", "a chord part", "chords"],
    "arpeggio": ["notes of the chord", "an arpeggiated part", "chord arpeggios", "arpeggios"],
    "rhythm_beat": ["the main beat", "a rhythm part", "the rhythm", "the beat"],
    "rhythm_aux": ["a rhythm part", "an auxiliary rhythm"],
    "bassline": ["the bassline", "a bass line", "a bassline", "the bass part"]
    }

translations_dynamics = {
    "quiet": ["quietly", "at low volume", "softly", "in piano dynamic"],
    "loud": ["loudly", "forcefully", "in forte", "in forte dynamic"]
    }

translations_melody = {
    "ostinato": ["a repeating phrase", "an ostinato", "a riff"],
    "pedal": ["pedal notes", "a pedal note", "repeating notes"],
    "scale": ["a scale sequence", "a scale", "notes in sequence", "scales"]
    }

translations_rhythm = {
    "straight": ["a straight beat rhythm", "a straight rhythm", "a steady rhythm"],
    "straight_half": ["a straight half beat rhythm", "a quaver beat", "repeating quavers", "a steady half rhythm", "straight quavers"],
    "sustain": ["a sustained note rhythm", "long notes", "a sustained feel"],
    "legato": ["a fluid feel", "a legato rhythm", "a fluid rhythm", "smooth connected notes"],
    "syncopation": ["a syncopated rhythm", "an off-beat rhythm"],
    "staccato": ["short sharp notes", "a staccato rhythm", "a punchy feel"]
    }

translations_technique = {
    "latin": ["latin rhythms", "a latin beat"],
    "ornament": ["heavy ornamentation", "flourishes", "grace notes"],
    "recitative": ["recitative vocals", "spoken words", "speech-like rhythm"],
    "harmonics": ["string harmonics", "natural harmonics"],
    "cymbal": ["a cymbal ride", "a riding cymbal", "a cymbal beat"],
    "breathy": ["breathy sounding vocals", "an airy voice"],
    "fill": ["drum fills", "frequent drum fills", "short drum solos", "regular drum fills"],
    "mute": ["palm muting", "muted string sound", "string muting", "muted notes"],
    "double_stop": ["double stopping", "two strings simultaneously", "two strings at once"],
    "scream": ["screaming vocals", "harsh vocal style", "an aggressive voice"],
    "growl": ["growling vocals", "vocal growls", "a low gutteral voice"],
    "low_register": ["chest voice", "low register singing", "lower pitch vocals"],
    "bend": ["string bending", "string bends", "bent notes"],
    "slide": ["string slides", "guitar slides"]
    }

translations_effect = {
    "reverb": ["reverb", "an echo effect", "a reverb effect"],
    "fuzz": ["a fuzz effect", "distorted tone"],
    "wah": ["a distorted wah effect", "a wah pedal"],
    "distortion": ["heavy distortion", "a crunchy tone"],
    "phase": ["a phaser effect", "a phase effect"]
    }

translations_genre = {
    "rock": ["a rock genre", "a rock style"],
    "electronic": ["an electronic genre", "an electronic style"],
    "singer_songwriter": ["a singer-songwriter genre", "a singer-songwriter style"],
    "bossa_nova": ["a bossa nova genre", "a bossa nova style", "a latin style"],
    "pop": ["a pop genre", "a pop style", "a popular music style"],
    "jazz": ["a jazz genre", "a jazz style"],
    "rap": ["a rap genre", "a rap style"],
    "musical_theatre": ["a musical theatre genre", "a musical theatre style", "a theatrical style"],
    }

def get_verb(instrument):
    match instrument:
        case "lead_male_singer" | "lead_female_singer":
            return random.choice(["sings", "is singing", "singing"])
        case "background_vocals":
            return random.choice(["sings", "singing"])
        case _:
            return random.choice(["plays", "is playing", "playing"])

def random_translation(translations_dict, string, label_drop_rate = 0):
    rand = 1
    if string != "":
        rand = random.random()
        if rand < label_drop_rate:
            string = ""
    if string in translations_dict:
        return random.choice(translations_dict[string]), (rand < label_drop_rate)
    else:
        return "", (rand < label_drop_rate)

def generate_query(instrument="", role="", melody="", rhythm="", technique="", genre="", dynamics="", effect="", label_drop_rate = 0):
    is_empty = True
    while is_empty:
        q_inst, dropped = random_translation(translations_instrument, instrument, label_drop_rate)
        is_empty = is_empty and dropped
        q_role, dropped = random_translation(translations_role, role, label_drop_rate)
        is_empty = is_empty and dropped
        q_dyna, dropped = random_translation(translations_dynamics, dynamics, label_drop_rate)
        is_empty = is_empty and dropped
        q_melo, dropped = random_translation(translations_melody, melody, label_drop_rate)
        is_empty = is_empty and dropped
        q_rhyt, dropped = random_translation(translations_rhythm, rhythm, label_drop_rate)
        is_empty = is_empty and dropped
        q_technique, dropped = random_translation(translations_technique, technique, label_drop_rate)
        is_empty = is_empty and dropped
        q_effect, dropped = random_translation(translations_effect, effect, label_drop_rate)
        is_empty = is_empty and dropped
        q_genre, dropped = random_translation(translations_genre, genre, label_drop_rate)
        is_empty = is_empty and dropped
    
    if q_role != "":
        q_role = " " + q_role
        if q_dyna != "":
            q_role = q_role + " " + q_dyna
            q_dyna = ""
        
    if(q_melo != "" and q_rhyt != ""):
        q_rhythmelo = f"{q_melo} with {q_rhyt}"
    elif(q_melo != ""):
        q_rhythmelo = q_melo
    elif(q_rhyt != ""):
        q_rhythmelo = q_rhyt
    else:
        q_rhythmelo = ""

    if q_rhythmelo != "":
        if q_role != "":
            prefix = random.choice(["using", "creating", "consisting of", "comprising", "involving"])
            q_rhythmelo = f", {prefix} {q_rhythmelo}"
        else:
            if(q_melo != ""):
                q_rhythmelo = f" {q_rhythmelo}"
            else:
                q_rhythmelo = f" with {q_rhythmelo}"
    else:
        q_rhythmelo = ""

    if q_role == "" and q_dyna != "":
        q_dyna = " " + q_dyna

    if(q_technique != "" and q_effect != ""):
        q_effecttech = f"{q_technique} and {q_effect}"
    elif(q_technique != ""):
        q_effecttech = q_technique
    elif(q_effect != ""):
        q_effecttech = q_effect
    else:
        q_effecttech = ""

    if q_effecttech != "":
        prefix = random.choice(["It utilises", "They play with", "The musician uses", "It uses", "The track has", "It has", "The track uses"])
        q_effecttech = f" {prefix} {q_effecttech}"
        if q_genre != "":
            prefix = random.choice([", and", " and", ", in", " and has", ", with"])
            q_genre = f"{prefix} {q_genre}"
    else:
        if q_genre != "":
            prefix = random.choice(["It uses", "The track has", "It has", "The track uses"])
            q_genre = f" {prefix} {q_genre}"

    return f"{q_inst} {get_verb(instrument)}{q_role}{q_rhythmelo}{q_dyna}.{q_effecttech}{q_genre}"


