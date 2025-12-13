"""
FoxDot Knowledge Base - Complete documentation for AI context
Contains all synths, samples, patterns, scales, effects, and FoxDot syntax
"""

# =============================================================================
# SYNTHDEF REFERENCE - All available synthesizers
# =============================================================================

SYNTH_DEFINITIONS = {
    # Melodic Synths
    "pluck": {
        "description": "A plucked string sound, good for melodies and arpeggios",
        "category": "melodic",
        "character": "bright, percussive attack with decay",
        "use_cases": ["melodies", "arpeggios", "chords"],
        "key_params": ["amp", "dur", "sus", "oct", "pan", "room", "vib"]
    },
    "bass": {
        "description": "Deep bass synthesizer for low-end",
        "category": "bass",
        "character": "warm, deep, powerful low frequencies",
        "use_cases": ["basslines", "sub bass", "low drones"],
        "key_params": ["amp", "dur", "sus", "oct", "slide", "room"]
    },
    "sawbass": {
        "description": "Sawtooth wave bass, aggressive and cutting",
        "category": "bass",
        "character": "aggressive, buzzy, rich harmonics",
        "use_cases": ["aggressive basslines", "lead bass", "techno"],
        "key_params": ["amp", "dur", "sus", "oct", "lpf", "res"]
    },
    "sinepad": {
        "description": "Soft sine wave pad for ambient textures",
        "category": "pad",
        "character": "smooth, warm, ethereal",
        "use_cases": ["ambient", "background", "atmosphere", "chords"],
        "key_params": ["amp", "dur", "sus", "room", "mix", "pan"]
    },
    "pads": {
        "description": "Lush pad synth for chords and atmosphere",
        "category": "pad",
        "character": "full, rich, sustaining",
        "use_cases": ["chord pads", "ambient textures", "backgrounds"],
        "key_params": ["amp", "dur", "sus", "room", "vib", "oct"]
    },
    "charm": {
        "description": "Bell-like charm synth with shimmer",
        "category": "melodic",
        "character": "bell-like, shimmering, crystalline",
        "use_cases": ["leads", "arpeggios", "melodic accents"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "bell": {
        "description": "Pure bell tone synthesizer",
        "category": "melodic",
        "character": "metallic, resonant, clear attack",
        "use_cases": ["bells", "chimes", "accents"],
        "key_params": ["amp", "dur", "sus", "oct", "room", "pan"]
    },
    "gong": {
        "description": "Large gong-like metallic sound",
        "category": "percussion",
        "character": "deep, resonant, metallic",
        "use_cases": ["accents", "transitions", "ambient"],
        "key_params": ["amp", "dur", "sus", "room"]
    },
    "soprano": {
        "description": "High vocal-like synthesizer",
        "category": "melodic",
        "character": "airy, vocal, high register",
        "use_cases": ["high melodies", "vocal-like leads"],
        "key_params": ["amp", "dur", "sus", "oct", "vib", "room"]
    },
    "blip": {
        "description": "Short blip sound, good for rhythmic patterns",
        "category": "melodic",
        "character": "short, punchy, electronic",
        "use_cases": ["arpeggios", "rhythmic patterns", "bleeps"],
        "key_params": ["amp", "dur", "oct", "pan"]
    },
    "pulse": {
        "description": "Pulse wave synthesizer",
        "category": "melodic",
        "character": "hollow, classic, variable width",
        "use_cases": ["retro sounds", "leads", "basslines"],
        "key_params": ["amp", "dur", "sus", "oct", "width"]
    },
    "saw": {
        "description": "Raw sawtooth wave synthesizer",
        "category": "melodic",
        "character": "bright, buzzy, harmonically rich",
        "use_cases": ["leads", "aggressive sounds", "EDM"],
        "key_params": ["amp", "dur", "sus", "oct", "lpf", "res"]
    },
    "square": {
        "description": "Square wave synthesizer",
        "category": "melodic",
        "character": "hollow, retro, chiptune-like",
        "use_cases": ["retro/chiptune", "leads", "basses"],
        "key_params": ["amp", "dur", "sus", "oct", "lpf"]
    },
    "soft": {
        "description": "Soft, mellow synth tone",
        "category": "melodic",
        "character": "gentle, warm, unobtrusive",
        "use_cases": ["background melodies", "soft leads"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "keys": {
        "description": "Electric piano-like keys sound",
        "category": "keys",
        "character": "warm, Rhodes-like, jazzy",
        "use_cases": ["jazz", "chords", "lo-fi"],
        "key_params": ["amp", "dur", "sus", "oct", "room", "vib"]
    },
    "piano": {
        "description": "Acoustic piano simulation",
        "category": "keys",
        "character": "natural, percussive, dynamic",
        "use_cases": ["classical", "jazz", "ballads"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "marimba": {
        "description": "Marimba-like mallet sound",
        "category": "melodic",
        "character": "wooden, warm, mallet percussion",
        "use_cases": ["melodic percussion", "world music"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "scatter": {
        "description": "Scattered granular-like texture",
        "category": "experimental",
        "character": "textured, scattered, ambient",
        "use_cases": ["ambient", "experimental", "textures"],
        "key_params": ["amp", "dur", "sus", "room", "pan"]
    },
    "noise": {
        "description": "White noise generator",
        "category": "noise",
        "character": "noisy, textural, percussive",
        "use_cases": ["percussion", "hi-hats", "textures", "risers"],
        "key_params": ["amp", "dur", "hpf", "lpf"]
    },
    "dub": {
        "description": "Dub-style bass/synth",
        "category": "bass",
        "character": "deep, reggae/dub influenced",
        "use_cases": ["dub", "reggae", "bass drops"],
        "key_params": ["amp", "dur", "sus", "oct", "room", "slide"]
    },
    "orient": {
        "description": "Oriental/Eastern style synth",
        "category": "melodic",
        "character": "exotic, eastern scales",
        "use_cases": ["world music", "exotic melodies"],
        "key_params": ["amp", "dur", "sus", "oct", "vib"]
    },
    "donk": {
        "description": "UK Hardcore 'donk' sound",
        "category": "percussion",
        "character": "bouncy, pitched percussion",
        "use_cases": ["hardcore", "bouncy beats"],
        "key_params": ["amp", "dur", "oct"]
    },
    "scratch": {
        "description": "Scratchy texture synth",
        "category": "experimental",
        "character": "noisy, scratchy, textural",
        "use_cases": ["transitions", "textures"],
        "key_params": ["amp", "dur", "room"]
    },
    "klank": {
        "description": "Metallic klank percussion",
        "category": "percussion",
        "character": "metallic, industrial",
        "use_cases": ["industrial", "metallic percussion"],
        "key_params": ["amp", "dur", "room"]
    },
    "feel": {
        "description": "Expressive synth with feeling",
        "category": "melodic",
        "character": "expressive, dynamic",
        "use_cases": ["emotional melodies", "leads"],
        "key_params": ["amp", "dur", "sus", "oct", "vib", "room"]
    },
    "glass": {
        "description": "Glassy, crystalline synth",
        "category": "melodic",
        "character": "clear, glass-like, delicate",
        "use_cases": ["delicate melodies", "ambient"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "creep": {
        "description": "Creepy atmospheric synth",
        "category": "experimental",
        "character": "dark, unsettling, atmospheric",
        "use_cases": ["dark ambient", "horror"],
        "key_params": ["amp", "dur", "sus", "room"]
    },
    "growl": {
        "description": "Growling bass sound",
        "category": "bass",
        "character": "aggressive, growling, dubstep-like",
        "use_cases": ["dubstep", "aggressive bass"],
        "key_params": ["amp", "dur", "sus", "oct", "lpf"]
    },
    "dirt": {
        "description": "Dirty/distorted synth",
        "category": "experimental",
        "character": "distorted, gritty, lo-fi",
        "use_cases": ["lo-fi", "distorted sounds"],
        "key_params": ["amp", "dur", "sus", "room"]
    },
    "crunch": {
        "description": "Crunchy distorted synth",
        "category": "experimental",
        "character": "crunchy, bitcrushed",
        "use_cases": ["lo-fi", "glitch"],
        "key_params": ["amp", "dur", "sus"]
    },
    "rave": {
        "description": "Classic rave stab synth",
        "category": "melodic",
        "character": "punchy, 90s rave",
        "use_cases": ["rave", "stabs", "EDM"],
        "key_params": ["amp", "dur", "sus", "oct"]
    },
    "razz": {
        "description": "Razzy buzzy synth",
        "category": "melodic",
        "character": "buzzy, aggressive",
        "use_cases": ["aggressive leads", "buzzy bass"],
        "key_params": ["amp", "dur", "sus", "oct", "lpf"]
    },
    "spark": {
        "description": "Sparkling synth texture",
        "category": "melodic",
        "character": "sparkling, bright, animated",
        "use_cases": ["arpeggios", "bright textures"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "fuzz": {
        "description": "Fuzzy distorted synth",
        "category": "bass",
        "character": "fuzzy, distorted, warm",
        "use_cases": ["fuzzy bass", "distorted leads"],
        "key_params": ["amp", "dur", "sus", "oct"]
    },
    "bug": {
        "description": "Bug-like buzzing synth",
        "category": "experimental",
        "character": "insect-like, buzzing",
        "use_cases": ["experimental", "textures"],
        "key_params": ["amp", "dur", "sus"]
    },
    "ripple": {
        "description": "Rippling modulated synth",
        "category": "melodic",
        "character": "watery, rippling, modulated",
        "use_cases": ["ambient", "water textures"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "snick": {
        "description": "Short snick percussion sound",
        "category": "percussion",
        "character": "short, clicky",
        "use_cases": ["percussion accents", "clicks"],
        "key_params": ["amp", "dur"]
    },
    "twang": {
        "description": "Twangy string-like synth",
        "category": "melodic",
        "character": "twangy, plucked string",
        "use_cases": ["country-ish sounds", "plucks"],
        "key_params": ["amp", "dur", "sus", "oct"]
    },
    "karp": {
        "description": "Karplus-Strong string synthesis",
        "category": "melodic",
        "character": "physical modeling, realistic strings",
        "use_cases": ["realistic strings", "plucks"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "arpy": {
        "description": "Arpeggiated synth sound",
        "category": "melodic",
        "character": "arpeggio-friendly, bright",
        "use_cases": ["arpeggios", "sequences"],
        "key_params": ["amp", "dur", "sus", "oct"]
    },
    "nylon": {
        "description": "Nylon string guitar simulation",
        "category": "melodic",
        "character": "warm, acoustic, nylon guitar",
        "use_cases": ["acoustic textures", "gentle melodies"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "varsaw": {
        "description": "Variable sawtooth synth",
        "category": "melodic",
        "character": "variable harmonics",
        "use_cases": ["evolving tones", "leads"],
        "key_params": ["amp", "dur", "sus", "oct", "lpf"]
    },
    "lazer": {
        "description": "Laser-like sweep sound",
        "category": "effects",
        "character": "sci-fi, sweeping",
        "use_cases": ["sci-fi effects", "transitions"],
        "key_params": ["amp", "dur"]
    },
    "star": {
        "description": "Starry, twinkling synth",
        "category": "melodic",
        "character": "twinkling, celestial",
        "use_cases": ["ambient", "cosmic textures"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "prophet": {
        "description": "Prophet-style analog synth",
        "category": "melodic",
        "character": "classic analog, warm",
        "use_cases": ["classic synth leads", "pads"],
        "key_params": ["amp", "dur", "sus", "oct", "lpf", "res"]
    },
    "quin": {
        "description": "Quintet-style ensemble synth",
        "category": "melodic",
        "character": "ensemble, full",
        "use_cases": ["full chords", "ensemble sounds"],
        "key_params": ["amp", "dur", "sus", "oct", "room"]
    },
    "jbass": {
        "description": "Jazz bass simulation",
        "category": "bass",
        "character": "jazzy, upright bass feel",
        "use_cases": ["jazz", "walking bass"],
        "key_params": ["amp", "dur", "sus", "oct", "slide"]
    },
    "space": {
        "description": "Spacey atmospheric synth",
        "category": "pad",
        "character": "cosmic, ambient, huge",
        "use_cases": ["ambient", "space textures", "drones"],
        "key_params": ["amp", "dur", "sus", "room", "pan"]
    },
    "zap": {
        "description": "Quick zap effect sound",
        "category": "effects",
        "character": "quick, zappy, percussive",
        "use_cases": ["effects", "accents", "glitch"],
        "key_params": ["amp", "dur"]
    },
}

# =============================================================================
# SAMPLE CHARACTERS - For play() SynthDef
# =============================================================================

SAMPLE_CHARACTERS = {
    # Drums
    "x": {"description": "Kick drum", "category": "drums", "character": "punchy, low"},
    "o": {"description": "Snare drum", "category": "drums", "character": "snappy, mid"},
    "O": {"description": "Heavy snare", "category": "drums", "character": "thick, powerful"},
    "*": {"description": "Clap", "category": "drums", "character": "snappy, wide"},
    "-": {"description": "Hi-hat (closed)", "category": "drums", "character": "tight, short"},
    "=": {"description": "Hi-hat (open)", "category": "drums", "character": "sizzle, longer"},
    "~": {"description": "Ride cymbal", "category": "drums", "character": "washy, sustained"},
    ":": {"description": "Shaker", "category": "drums", "character": "textured, continuous"},
    "#": {"description": "Crash cymbal", "category": "drums", "character": "big, washy"},
    
    # Percussion
    "t": {"description": "High tom", "category": "percussion", "character": "high, punchy"},
    "u": {"description": "Mid tom", "category": "percussion", "character": "mid, round"},
    "v": {"description": "Low tom", "category": "percussion", "character": "low, deep"},
    "+": {"description": "Click/tick", "category": "percussion", "character": "short, high"},
    "s": {"description": "Rim shot", "category": "percussion", "character": "crisp, metallic"},
    "p": {"description": "Cowbell/block", "category": "percussion", "character": "metallic, pitched"},
    "w": {"description": "Wood block", "category": "percussion", "character": "woody, short"},
    "m": {"description": "Maracas", "category": "percussion", "character": "shaky, textured"},
    
    # Electronic/FX
    "^": {"description": "Glitch/noise burst", "category": "fx", "character": "glitchy, digital"},
    "&": {"description": "Synth hit", "category": "fx", "character": "electronic, tonal"},
    "@": {"description": "Vocal chop", "category": "fx", "character": "voice, choppy"},
    "!": {"description": "Impact/boom", "category": "fx", "character": "big, impactful"},
    "?": {"description": "Question sound", "category": "fx", "character": "rising, tonal"},
    "/": {"description": "Sweep", "category": "fx", "character": "sweeping, transition"},
    "\\": {"description": "Reverse sweep", "category": "fx", "character": "reverse, build"},
    
    # Bass/Low
    "b": {"description": "Bass hit", "category": "bass", "character": "low, punchy"},
    "d": {"description": "Deep kick", "category": "bass", "character": "sub, deep"},
    
    # Melodic samples  
    "a": {"description": "Atmospheric sound", "category": "melodic", "character": "textured"},
    "c": {"description": "Chord stab", "category": "melodic", "character": "harmonic"},
    "e": {"description": "Electronic blip", "category": "melodic", "character": "short, pitched"},
    "f": {"description": "Flute/wind", "category": "melodic", "character": "airy, breathy"},
    "g": {"description": "Guitar strum", "category": "melodic", "character": "stringy"},
    "h": {"description": "Horn hit", "category": "melodic", "character": "brassy"},
    "i": {"description": "Industrial sound", "category": "fx", "character": "metallic, harsh"},
    "j": {"description": "Jingle/bell", "category": "melodic", "character": "bright, ringing"},
    "k": {"description": "Key/piano", "category": "melodic", "character": "tonal, harmonic"},
    "l": {"description": "Loop fragment", "category": "melodic", "character": "varied"},
    "n": {"description": "Noise", "category": "fx", "character": "noisy, textural"},
    "q": {"description": "Quirky sound", "category": "fx", "character": "unusual, varied"},
    "r": {"description": "Rattle/roll", "category": "percussion", "character": "rolling, textured"},
    "y": {"description": "Yeah/vocal", "category": "fx", "character": "voice, exclamation"},
    "z": {"description": "Zap/laser", "category": "fx", "character": "sci-fi, pitched"},
    
    # Numbers (alternative samples)
    "1": {"description": "Variant sample 1", "category": "varied", "character": "alternate kick"},
    "2": {"description": "Variant sample 2", "category": "varied", "character": "alternate snare"},
    "3": {"description": "Variant sample 3", "category": "varied", "character": "alternate hat"},
    "4": {"description": "Variant sample 4", "category": "varied", "character": "alternate perc"},
}

# =============================================================================
# SCALES - All available musical scales
# =============================================================================

SCALES = {
    "major": {
        "notes": [0, 2, 4, 5, 7, 9, 11],
        "character": "Happy, bright, uplifting",
        "genres": ["pop", "classical", "happy music"]
    },
    "minor": {
        "notes": [0, 2, 3, 5, 7, 8, 10],
        "character": "Sad, emotional, dark",
        "genres": ["sad songs", "emotional", "rock"]
    },
    "dorian": {
        "notes": [0, 2, 3, 5, 7, 9, 10],
        "character": "Jazzy, sophisticated, minor with bright 6th",
        "genres": ["jazz", "funk", "soul"]
    },
    "phrygian": {
        "notes": [0, 1, 3, 5, 7, 8, 10],
        "character": "Spanish, exotic, flamenco",
        "genres": ["flamenco", "metal", "world music"]
    },
    "lydian": {
        "notes": [0, 2, 4, 6, 7, 9, 11],
        "character": "Dreamy, floating, ethereal",
        "genres": ["film music", "ambient", "progressive"]
    },
    "mixolydian": {
        "notes": [0, 2, 4, 5, 7, 9, 10],
        "character": "Bluesy, rock, dominant feel",
        "genres": ["blues", "rock", "funk"]
    },
    "locrian": {
        "notes": [0, 1, 3, 5, 6, 8, 10],
        "character": "Dark, unstable, dissonant",
        "genres": ["metal", "experimental", "dark music"]
    },
    "pentatonic": {
        "notes": [0, 2, 4, 7, 9],
        "character": "Universal, safe, melodic",
        "genres": ["all genres", "rock solos", "folk"]
    },
    "minorPentatonic": {
        "notes": [0, 3, 5, 7, 10],
        "character": "Blues, rock, universal minor",
        "genres": ["blues", "rock", "soul"]
    },
    "blues": {
        "notes": [0, 3, 5, 6, 7, 10],
        "character": "Bluesy, soulful, expressive",
        "genres": ["blues", "jazz", "rock"]
    },
    "chromatic": {
        "notes": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "character": "All notes, atonal, experimental",
        "genres": ["experimental", "jazz", "classical"]
    },
    "harmonicMinor": {
        "notes": [0, 2, 3, 5, 7, 8, 11],
        "character": "Middle Eastern, classical, dramatic",
        "genres": ["classical", "middle eastern", "metal"]
    },
    "melodicMinor": {
        "notes": [0, 2, 3, 5, 7, 9, 11],
        "character": "Jazz, smooth, ascending minor",
        "genres": ["jazz", "classical"]
    },
    "whole": {
        "notes": [0, 2, 4, 6, 8, 10],
        "character": "Dreamy, mysterious, Debussy-like",
        "genres": ["impressionist", "ambient", "film"]
    },
    "halfWhole": {
        "notes": [0, 1, 3, 4, 6, 7, 9, 10],
        "character": "Diminished, tense, jazz",
        "genres": ["jazz", "film noir"]
    },
    "wholeHalf": {
        "notes": [0, 2, 3, 5, 6, 8, 9, 11],
        "character": "Diminished, symmetrical",
        "genres": ["jazz", "classical"]
    },
    "egyptian": {
        "notes": [0, 2, 5, 7, 10],
        "character": "Ancient, mystical, Egyptian",
        "genres": ["world music", "ambient", "film"]
    },
    "japanese": {
        "notes": [0, 1, 5, 7, 8],
        "character": "Japanese traditional, zen",
        "genres": ["world music", "ambient", "meditation"]
    },
    "chinese": {
        "notes": [0, 4, 6, 7, 11],
        "character": "Chinese traditional",
        "genres": ["world music", "film"]
    },
    "indian": {
        "notes": [0, 1, 4, 5, 7, 8, 11],
        "character": "Indian classical, raga-like",
        "genres": ["world music", "meditation"]
    },
    "prometheus": {
        "notes": [0, 2, 4, 6, 9, 10],
        "character": "Scriabin's mystic chord based",
        "genres": ["experimental", "ambient"]
    },
    "locrianMajor": {
        "notes": [0, 2, 4, 5, 6, 8, 10],
        "character": "Strange, hybrid",
        "genres": ["experimental"]
    },
}

# =============================================================================
# ROOT NOTES - Available root/key notes
# =============================================================================

ROOT_NOTES = {
    "C": 0, "c": 0,
    "C#": 1, "Cs": 1, "Db": 1,
    "D": 2, "d": 2,
    "D#": 3, "Ds": 3, "Eb": 3,
    "E": 4, "e": 4,
    "F": 5, "f": 5,
    "F#": 6, "Fs": 6, "Gb": 6,
    "G": 7, "g": 7,
    "G#": 8, "Gs": 8, "Ab": 8,
    "A": 9, "a": 9,
    "A#": 10, "As": 10, "Bb": 10,
    "B": 11, "b": 11,
}

# =============================================================================
# PLAYER ATTRIBUTES - Parameters for player objects
# =============================================================================

PLAYER_ATTRIBUTES = {
    # Core timing
    "dur": {
        "description": "Duration of each note in beats",
        "type": "number or pattern",
        "default": 1,
        "examples": ["dur=1", "dur=[1, 0.5, 0.5]", "dur=1/4"],
        "tip": "Use fractions for subdivisions: 1/2, 1/4, 1/8, 1/16"
    },
    "sus": {
        "description": "Sustain - how long the note sounds (independent of dur)",
        "type": "number or pattern",
        "default": "equals dur",
        "examples": ["sus=2", "sus=[1, 0.5]"],
        "tip": "sus > dur creates overlapping notes, sus < dur creates staccato"
    },
    "delay": {
        "description": "Delay before the note plays (in beats)",
        "type": "number or pattern",
        "default": 0,
        "examples": ["delay=0.5", "delay=[0, 0.25]"],
        "tip": "Use for swing/shuffle feel or polyrhythms"
    },
    
    # Pitch
    "degree": {
        "description": "Note pitch relative to scale (first argument)",
        "type": "number or pattern",
        "default": 0,
        "examples": ["[0, 2, 4]", "P[0, 1, 2, 3]"],
        "tip": "Use tuples for chords: (0, 2, 4)"
    },
    "oct": {
        "description": "Octave number",
        "type": "number or pattern",
        "default": 5,
        "examples": ["oct=4", "oct=[4, 5]"],
        "tip": "Lower octaves (3-4) for bass, higher (5-7) for leads"
    },
    "scale": {
        "description": "Musical scale to use",
        "type": "Scale object",
        "default": "Scale.default",
        "examples": ["scale=Scale.minor", "scale=Scale.dorian"],
        "tip": "See SCALES dictionary for all options"
    },
    "root": {
        "description": "Root note of the scale",
        "type": "string or number",
        "default": "Root.default (C)",
        "examples": ["root='C'", "root='F#'", "root=7"],
        "tip": "Use note names or semitone numbers"
    },
    
    # Dynamics
    "amp": {
        "description": "Amplitude/volume (0-1 or higher)",
        "type": "number or pattern",
        "default": 1,
        "examples": ["amp=0.5", "amp=[0.8, 0.4, 0.6]"],
        "tip": "Values > 1 will clip, use 0.3-0.8 for mix balance"
    },
    "pan": {
        "description": "Stereo panning (-1 left, 0 center, 1 right)",
        "type": "number or pattern",
        "default": 0,
        "examples": ["pan=-0.5", "pan=[-1, 1]"],
        "tip": "Use patterns for auto-panning effects"
    },
    
    # Effects - Modulation
    "vib": {
        "description": "Vibrato depth",
        "type": "number",
        "default": 0,
        "examples": ["vib=0.5", "vib=2"],
        "tip": "Adds pitch wobble, good for strings/vocals"
    },
    "vibdepth": {
        "description": "Vibrato depth modifier",
        "type": "number",
        "default": 0.02,
        "examples": ["vibdepth=0.05"],
        "tip": "How much pitch varies"
    },
    "slide": {
        "description": "Pitch slide between notes",
        "type": "number",
        "default": 0,
        "examples": ["slide=1", "slide=[0, 1]"],
        "tip": "Creates portamento/glide effect"
    },
    "slidedelay": {
        "description": "Delay before slide starts",
        "type": "number",
        "default": 0,
        "examples": ["slidedelay=0.5"],
        "tip": "Makes slide happen later in the note"
    },
    "bend": {
        "description": "Pitch bend amount",
        "type": "number",
        "default": 0,
        "examples": ["bend=0.5", "bend=-1"],
        "tip": "Bends pitch up/down from the note"
    },
    "benddelay": {
        "description": "Delay before bend starts",
        "type": "number",
        "default": 0,
        "examples": ["benddelay=0.25"],
        "tip": "Controls when the bend begins"
    },
    
    # Effects - Filter
    "lpf": {
        "description": "Low-pass filter cutoff frequency (Hz)",
        "type": "number or pattern",
        "default": "0 (off)",
        "examples": ["lpf=2000", "lpf=var([500, 2000], 4)"],
        "tip": "Lower values = darker/muffled sound"
    },
    "hpf": {
        "description": "High-pass filter cutoff frequency (Hz)",
        "type": "number or pattern",
        "default": "0 (off)",
        "examples": ["hpf=200", "hpf=500"],
        "tip": "Removes low frequencies, thins sound"
    },
    "res": {
        "description": "Filter resonance/Q",
        "type": "number",
        "default": 0.5,
        "examples": ["res=0.8", "res=0.2"],
        "tip": "Higher = more emphasis at cutoff frequency"
    },
    "lpr": {
        "description": "Low-pass filter resonance",
        "type": "number",
        "default": 1,
        "examples": ["lpr=2"],
        "tip": "Resonance specifically for low-pass"
    },
    
    # Effects - Time/Space
    "room": {
        "description": "Reverb room size",
        "type": "number",
        "default": 0,
        "examples": ["room=0.5", "room=0.8"],
        "tip": "0-1, higher = larger space/more reverb"
    },
    "mix": {
        "description": "Reverb wet/dry mix",
        "type": "number",
        "default": 0.1,
        "examples": ["mix=0.5"],
        "tip": "How much reverb vs. dry signal"
    },
    "echo": {
        "description": "Echo/delay amount",
        "type": "number",
        "default": 0,
        "examples": ["echo=0.5"],
        "tip": "Creates rhythmic delays"
    },
    "echotime": {
        "description": "Echo delay time in beats",
        "type": "number",
        "default": 0.5,
        "examples": ["echotime=0.25"],
        "tip": "Sync with tempo using beat fractions"
    },
    
    # Effects - Rhythmic
    "chop": {
        "description": "Chops the sound into pieces",
        "type": "number",
        "default": 0,
        "examples": ["chop=4", "chop=8"],
        "tip": "Higher number = more chops"
    },
    "spin": {
        "description": "Spinning stereo effect",
        "type": "number",
        "default": 0,
        "examples": ["spin=4"],
        "tip": "Creates rotating pan effect"
    },
    "cut": {
        "description": "Cut group - stops other sounds in same group",
        "type": "number",
        "default": 0,
        "examples": ["cut=1"],
        "tip": "Use to make hi-hats cut each other"
    },
    "coarse": {
        "description": "Bitcrush/sample rate reduction",
        "type": "number",
        "default": 0,
        "examples": ["coarse=8"],
        "tip": "Lo-fi effect, lower = more crushed"
    },
    "striate": {
        "description": "Granular stretching",
        "type": "number",
        "default": 0,
        "examples": ["striate=4"],
        "tip": "Granular time-stretch effect"
    },
    "pshift": {
        "description": "Pitch shift in semitones",
        "type": "number",
        "default": 0,
        "examples": ["pshift=12", "pshift=-7"],
        "tip": "12 = octave up, -12 = octave down"
    },
    "rate": {
        "description": "Playback rate for samples",
        "type": "number",
        "default": 1,
        "examples": ["rate=0.5", "rate=2"],
        "tip": "2 = double speed/octave up, 0.5 = half speed"
    },
    "sample": {
        "description": "Sample number for sample characters",
        "type": "number",
        "default": 0,
        "examples": ["sample=1", "sample=[0, 1, 2]"],
        "tip": "Each character has multiple sample variations"
    },
    
    # Effects - Distortion
    "drive": {
        "description": "Overdrive/distortion amount",
        "type": "number",
        "default": 0,
        "examples": ["drive=0.5"],
        "tip": "Adds harmonic distortion"
    },
    "shape": {
        "description": "Wave shaping amount",
        "type": "number",
        "default": 0,
        "examples": ["shape=0.5"],
        "tip": "Soft to hard clipping"
    },
    "formant": {
        "description": "Formant filter (vowel sounds)",
        "type": "number",
        "default": 0,
        "examples": ["formant=0.5"],
        "tip": "Creates vocal-like resonances"
    },
}

# =============================================================================
# PATTERN FUNCTIONS - Pattern generators and transformations
# =============================================================================

PATTERN_FUNCTIONS = {
    # Generators
    "P": {
        "description": "Basic pattern constructor",
        "syntax": "P[0, 1, 2, 3]",
        "example": "p1 >> pluck(P[0, 2, 4, 7])"
    },
    "PRange": {
        "description": "Pattern from range of numbers",
        "syntax": "PRange(start, stop, step)",
        "example": "PRange(8) # P[0,1,2,3,4,5,6,7]"
    },
    "PRand": {
        "description": "Random values from a list",
        "syntax": "PRand([values], length)",
        "example": "PRand([0, 2, 4], 8) # 8 random notes from [0,2,4]"
    },
    "PwRand": {
        "description": "Weighted random selection",
        "syntax": "PwRand([values], [weights])",
        "example": "PwRand([0, 1, 2], [0.5, 0.3, 0.2])"
    },
    "PSine": {
        "description": "Sine wave pattern",
        "syntax": "PSine(length)",
        "example": "PSine(16) # Smooth wave over 16 steps"
    },
    "PSaw": {
        "description": "Sawtooth wave pattern",
        "syntax": "PSaw(length)",
        "example": "PSaw(8)"
    },
    "PTri": {
        "description": "Triangle wave pattern",
        "syntax": "PTri(length)",
        "example": "PTri(8)"
    },
    "PSquare": {
        "description": "Square wave pattern",
        "syntax": "PSquare(length)",
        "example": "PSquare(8)"
    },
    "PEuclid": {
        "description": "Euclidean rhythm pattern",
        "syntax": "PEuclid(pulses, steps)",
        "example": "PEuclid(3, 8) # 3 pulses over 8 steps"
    },
    "PDur": {
        "description": "Duration pattern from Euclidean rhythm",
        "syntax": "PDur(pulses, steps)",
        "example": "PDur(3, 8)"
    },
    "PStep": {
        "description": "Step sequencer pattern",
        "syntax": "PStep(pattern, dur)",
        "example": "PStep([1,0,0,1,0], 0.25)"
    },
    "PSum": {
        "description": "Pattern that sums to a value",
        "syntax": "PSum(target, count)",
        "example": "PSum(4, 3) # 3 values that sum to 4"
    },
    "PWhite": {
        "description": "White noise pattern (random floats)",
        "syntax": "PWhite(lo, hi)",
        "example": "PWhite(0, 1) # Random floats 0-1"
    },
    "PBrown": {
        "description": "Brownian motion pattern",
        "syntax": "PBrown(lo, hi, step)",
        "example": "PBrown(0, 7, 1)"
    },
    "PWalk": {
        "description": "Random walk pattern",
        "syntax": "PWalk(max_step)",
        "example": "PWalk(2)"
    },
    
    # Transformations (methods on patterns)
    "reverse": {
        "description": "Reverse the pattern",
        "syntax": "pattern.reverse()",
        "example": "P[0,1,2,3].reverse() # P[3,2,1,0]"
    },
    "rotate": {
        "description": "Rotate pattern by n steps",
        "syntax": "pattern.rotate(n)",
        "example": "P[0,1,2,3].rotate(1) # P[1,2,3,0]"
    },
    "shuffle": {
        "description": "Randomly shuffle pattern",
        "syntax": "pattern.shuffle()",
        "example": "P[0,1,2,3].shuffle()"
    },
    "mirror": {
        "description": "Append reversed version",
        "syntax": "pattern.mirror()",
        "example": "P[0,1,2].mirror() # P[0,1,2,2,1,0]"
    },
    "palindrome": {
        "description": "Create palindrome (without repeat)",
        "syntax": "pattern.palindrome()",
        "example": "P[0,1,2].palindrome() # P[0,1,2,1,0]"
    },
    "stutter": {
        "description": "Repeat each element n times",
        "syntax": "pattern.stutter(n)",
        "example": "P[0,1,2].stutter(2) # P[0,0,1,1,2,2]"
    },
    "amen": {
        "description": "Apply amen break pattern",
        "syntax": "pattern.amen()",
        "example": "P['x-o-'].amen()"
    },
    "stretch": {
        "description": "Stretch pattern to length",
        "syntax": "pattern.stretch(length)",
        "example": "P[0,1,2,3].stretch(8)"
    },
    "trim": {
        "description": "Trim pattern to length",
        "syntax": "pattern.trim(length)",
        "example": "P[0,1,2,3,4,5].trim(4)"
    },
    "loop": {
        "description": "Loop pattern n times",
        "syntax": "pattern.loop(n)",
        "example": "P[0,1,2].loop(3)"
    },
    "offadd": {
        "description": "Add offset to alternating elements",
        "syntax": "pattern.offadd(value)",
        "example": "P[0,0,0,0].offadd(2) # P[0,2,0,2]"
    },
    "layer": {
        "description": "Layer with transformation",
        "syntax": "pattern.layer(method, args)",
        "example": "P[0,1,2].layer('reverse')"
    },
}

# =============================================================================
# TIMEVAR REFERENCE - Time-dependent variables
# =============================================================================

TIMEVAR_TYPES = {
    "var": {
        "description": "Basic time-varying variable",
        "syntax": "var([values], [durations])",
        "example": "var([0, 4], 8) # Alternates every 8 beats",
        "use_case": "Chord progressions, changing roots"
    },
    "linvar": {
        "description": "Linear interpolation between values",
        "syntax": "linvar([values], [durations])",
        "example": "linvar([0, 1], 8) # Ramps 0 to 1 over 8 beats",
        "use_case": "Filter sweeps, volume fades"
    },
    "expvar": {
        "description": "Exponential interpolation",
        "syntax": "expvar([values], [durations])",
        "example": "expvar([100, 4000], 16)",
        "use_case": "Frequency sweeps (more musical)"
    },
    "sinvar": {
        "description": "Sinusoidal oscillation",
        "syntax": "sinvar([min, max], [period])",
        "example": "sinvar([0.3, 0.8], 4) # LFO effect",
        "use_case": "Pulsing effects, tremolo"
    },
    "Pvar": {
        "description": "Pattern that changes over time",
        "syntax": "Pvar([[pattern1], [pattern2]], [durations])",
        "example": "Pvar([[0,1,2], [0,2,4]], 8)",
        "use_case": "Changing melodies/rhythms"
    },
}

# =============================================================================
# CLOCK OPERATIONS - Tempo and timing control
# =============================================================================

CLOCK_OPERATIONS = {
    "Clock.bpm": {
        "description": "Set or get the tempo in beats per minute",
        "syntax": "Clock.bpm = 120",
        "example": "Clock.bpm = 140",
        "tip": "Range typically 60-200 BPM"
    },
    "Clock.clear()": {
        "description": "Stop all players and clear the clock",
        "syntax": "Clock.clear()",
        "example": "Clock.clear()  # Stops everything",
        "tip": "Shortcut: Ctrl+."
    },
    "Clock.now()": {
        "description": "Get current beat number",
        "syntax": "Clock.now()",
        "example": "print(Clock.now())",
        "tip": "Useful for conditional logic"
    },
    "Clock.schedule()": {
        "description": "Schedule a function to run at a time",
        "syntax": "Clock.schedule(func, beat)",
        "example": "Clock.schedule(my_func, Clock.now() + 4)",
        "tip": "For timed events and arrangements"
    },
    "Clock.future()": {
        "description": "Schedule function in n beats",
        "syntax": "Clock.future(beats, func)",
        "example": "Clock.future(8, my_func)",
        "tip": "Easier than calculating beat numbers"
    },
}

# =============================================================================
# PLAYER METHODS - Operations on player objects
# =============================================================================

PLAYER_METHODS = {
    "stop()": {
        "description": "Stop the player",
        "syntax": "p1.stop()",
        "example": "p1.stop()"
    },
    "solo()": {
        "description": "Solo this player (mute others)",
        "syntax": "p1.solo()",
        "example": "p1.solo()"
    },
    "only()": {
        "description": "Play only this player",
        "syntax": "p1.only()",
        "example": "p1.only()"
    },
    "follow()": {
        "description": "Follow another player's pitch",
        "syntax": "p2.follow(p1)",
        "example": "p2 >> bass().follow(p1)"
    },
    "accompany()": {
        "description": "Accompany with harmony",
        "syntax": "p2.accompany(p1)",
        "example": "p2 >> keys().accompany(p1)"
    },
    "every()": {
        "description": "Apply method every n beats",
        "syntax": "player.every(beats, method, *args)",
        "example": "d1 >> play('x-o-').every(8, 'shuffle')"
    },
    "degrade()": {
        "description": "Randomly drop notes",
        "syntax": "player.degrade(amount)",
        "example": "p1 >> pluck([0,1,2]).degrade(0.3)"
    },
    "offbeat()": {
        "description": "Shift to offbeat",
        "syntax": "player.offbeat()",
        "example": "d2 >> play('-').offbeat()"
    },
    "strum()": {
        "description": "Strum chords",
        "syntax": "player.strum(duration)",
        "example": "p1 >> pluck([(0,2,4)]).strum(0.1)"
    },
    "spread()": {
        "description": "Spread across stereo",
        "syntax": "player.spread()",
        "example": "p1 >> pluck([0,1,2,3]).spread()"
    },
}

# =============================================================================
# PLAYSTRING NOTATION - Special characters for play() strings
# =============================================================================

PLAYSTRING_NOTATION = {
    "()": {
        "description": "Alternating - plays different character each loop",
        "example": "d1 >> play('(xo)-')",
        "result": "First loop: x-, Second loop: o-"
    },
    "[]": {
        "description": "Subdivide - plays all characters in time of one",
        "example": "d1 >> play('x[--]-o-')",
        "result": "Two quick hi-hats in space of one beat"
    },
    "{}": {
        "description": "Random - picks random character each time",
        "example": "d1 >> play('x-{o*}-')",
        "result": "Randomly plays snare or clap"
    },
    "<>": {
        "description": "Layer - plays multiple patterns together",
        "example": "d1 >> play('<x-o-><---->)",
        "result": "Kick/snare with hi-hats layered"
    },
    " ": {
        "description": "Rest - silence for one beat",
        "example": "d1 >> play('x  o')",
        "result": "Kick, rest, rest, snare"
    },
    "|x2|": {
        "description": "Sample select - choose sample number",
        "example": "d1 >> play('|x2|---|o|')",
        "result": "Kick sample 2, hats, snare sample 0"
    },
}

# =============================================================================
# GENRE PRESETS - Common patterns for different styles
# =============================================================================

GENRE_PATTERNS = {
    "house": {
        "bpm": "120-130",
        "drums": "x-o-x-o- (four-on-floor)",
        "hats": "-------- or --[--]--[--]",
        "synths": ["bass", "keys", "pads"],
        "tips": ["Strong kick on every beat", "Offbeat hi-hats", "Chord stabs"]
    },
    "techno": {
        "bpm": "125-150",
        "drums": "x-x-x-x- (driving kick)",
        "hats": "[--][--][--][--]",
        "synths": ["bass", "saw", "noise"],
        "tips": ["Relentless kick", "Filter sweeps", "Minimal melodic content"]
    },
    "drum_and_bass": {
        "bpm": "160-180",
        "drums": "x--o--x-o- (breakbeat feel)",
        "hats": "complex patterns with [] and {}",
        "synths": ["bass", "growl", "pads"],
        "tips": ["Syncopated breaks", "Heavy sub bass", "Complex rhythms"]
    },
    "hiphop": {
        "bpm": "85-115",
        "drums": "x--x--o- (boom bap)",
        "hats": "-[--]-[--]",
        "synths": ["keys", "piano", "bass"],
        "tips": ["Swing/shuffle", "Sample-based feel", "Space in patterns"]
    },
    "ambient": {
        "bpm": "60-90",
        "drums": "Sparse or none",
        "hats": "Subtle textures",
        "synths": ["pads", "sinepad", "space", "soft"],
        "tips": ["Long sustains", "Heavy reverb", "Slow evolution"]
    },
    "jazz": {
        "bpm": "100-180 (varies)",
        "drums": "-~-~ (ride pattern)",
        "hats": "Brushes/light",
        "synths": ["piano", "keys", "bass", "jbass"],
        "tips": ["Swing feel", "Complex harmonies", "Scale modes"]
    },
    "lo-fi": {
        "bpm": "70-90",
        "drums": "Relaxed hip-hop feel",
        "hats": "Vinyl crackle texture",
        "synths": ["keys", "piano", "soft"],
        "tips": ["Coarse/bit crush", "Room reverb", "Detuned sounds"]
    },
    "dubstep": {
        "bpm": "140",
        "drums": "x--o----x--o---- (half-time)",
        "hats": "sparse",
        "synths": ["growl", "bass", "wobble"],
        "tips": ["Heavy wobble bass", "Half-time feel", "Dramatic drops"]
    },
}

# =============================================================================
# Build complete knowledge string for AI context
# =============================================================================

def get_foxdot_knowledge() -> str:
    """Generate comprehensive FoxDot knowledge for AI context."""
    
    knowledge = """
# FoxDot Live Coding Knowledge Base
## Complete Reference for AI Music Agent

### AVAILABLE SYNTHS (use with: p1 >> synth_name([notes]))
"""
    
    # Add synths
    for name, info in SYNTH_DEFINITIONS.items():
        knowledge += f"- **{name}**: {info['description']} | Character: {info['character']}\n"
    
    knowledge += """
### SAMPLE CHARACTERS (use with: d1 >> play("string"))
"""
    
    # Add samples
    for char, info in SAMPLE_CHARACTERS.items():
        if char.isalnum() or char in "xo*-=~:#":
            knowledge += f"- '{char}': {info['description']} ({info['character']})\n"
    
    knowledge += """
### SCALES (use with: Scale.default = Scale.name or scale=Scale.name)
"""
    
    # Add scales
    for name, info in SCALES.items():
        knowledge += f"- **Scale.{name}**: {info['character']} | Good for: {', '.join(info['genres'])}\n"
    
    knowledge += """
### KEY PLAYER ATTRIBUTES
"""
    
    # Add key attributes
    key_attrs = ["dur", "amp", "oct", "sus", "pan", "room", "lpf", "vib", "slide", "chop", "delay"]
    for attr in key_attrs:
        if attr in PLAYER_ATTRIBUTES:
            info = PLAYER_ATTRIBUTES[attr]
            knowledge += f"- **{attr}**: {info['description']} | Example: {info['examples'][0]}\n"
    
    knowledge += """
### PATTERN SYNTAX
- P[0, 1, 2, 3] - Basic pattern
- (0, 2, 4) - Play notes simultaneously (chord)
- [0, 1, 2] in play strings - Subdivide time
- (x o) in play strings - Alternate each loop
- {x o} in play strings - Random choice

### PLAYSTRING BRACKETS
- "x-o-" - Simple sequence
- "(xo)--" - Alternates x and o
- "x[--]o-" - Two quick hits
- "x{o*}-" - Random snare or clap

### TIMEVARS (values that change over time)
- var([0, 4], 8) - Switch between values every 8 beats
- linvar([0, 1], 16) - Ramp from 0 to 1 over 16 beats

### CLOCK CONTROL
- Clock.bpm = 120 - Set tempo
- Clock.clear() - Stop everything

### USEFUL PATTERNS
- PRange(8) - P[0,1,2,3,4,5,6,7]
- PRand([0,2,4], 8) - 8 random notes
- PEuclid(3, 8) - Euclidean rhythm

### PLAYER METHODS
- p1.stop() - Stop player
- p1.every(8, 'shuffle') - Shuffle every 8 beats
- p1.follow(p2) - Follow another player
"""
    
    return knowledge


# Export all for easy access
__all__ = [
    'SYNTH_DEFINITIONS',
    'SAMPLE_CHARACTERS', 
    'SCALES',
    'ROOT_NOTES',
    'PLAYER_ATTRIBUTES',
    'PATTERN_FUNCTIONS',
    'TIMEVAR_TYPES',
    'CLOCK_OPERATIONS',
    'PLAYER_METHODS',
    'PLAYSTRING_NOTATION',
    'GENRE_PATTERNS',
    'get_foxdot_knowledge',
]
