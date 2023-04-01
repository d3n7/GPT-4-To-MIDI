import os, requests, argparse, re
from fractions import Fraction
from midiutil.MidiFile import MIDIFile
import openai

#settings
openaiKey = '<YOUR API KEY>'
sys1 = 'You are MusicGPT, a music creation and completion chat bot that. When a user gives you a prompt,' \
          ' you return them a song showing the notes, durations, and times that they occur. Respond only with the music.' \
          '\n\nNotation looks like this:\n(Note-duration-time in beats)\nC4-1/4-0, E4-1/4-2.5, D4-1/4-3, F4-1/4-3 etc.'
sys2 = 'You are MusicGPT, a music creation and completion chat bot that. When a user gives you a prompt,' \
         'you return them a melody showing the notes and the rhythms. Respond only with the music.' \
         '\n\nNotation looks like this:\nC5-1/4, E5 1/2 etc.'
system = sys1

#other vars n functions
melody = MIDIFile(1, deinterleave=False)
track = 0
channel = 0
volume = 100
def noteToInt(n):
    oct = int(n[-1])
    letter = n[:-1]
    notes = [["C"], ["Db", "C#"], ["D"], ["Eb", "D#"], ["E"], ["F"], ["Gb", "F#"], ["G"], ["Ab", "G#"], ["A"], ["Bb", "A#"], ["B"]]
    id = 0
    for ix, x in enumerate(notes):
        for y in x:
            if letter == y:
                id = ix
    return id+oct*12+12

#environment
path = os.path.realpath(os.path.dirname(__file__))

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prompt', help='specify prompt to use (default: Jazz!)', default='Jazz!')
parser.add_argument('-m', '--mono', help='alternative system to generate monophonic MIDI outputs', action='store_true')
parser.add_argument('-o', '--output', help='specify output directory (default: current)', default=path)
parser.add_argument('-a', '--auth', help='specify openai api key (edit this script file to set a default)', default=openaiKey)
args = parser.parse_args()
if args.mono:
    system = sys2

counter = 1
while 1:
    #openai request
    print('[*] Making request to OpenAI API')
    openai.api_key = args.auth
    r = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages = [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': args.prompt}
        ]
    )
    response = r['choices'][0]['message']['content']


    #parse content
    print('[*] Parsing content')
    noteInfo = []
    #thanks GPT-4 for this monstrosity of regex that seems to work
    reg1 = r'(?<![A-Za-z\d])([A-G](?:#|b)?\d(?:-\d+(?:\/\d+)?(?:-\d+(?:\.\d+)?)?)+)(?![A-Za-z\d])'
    reg2 = r'(?<![A-Za-z\d])([A-G](?:#|b)?\d-(?:\d+\/\d+|\d+))(?![A-Za-z\d])'
    regx = re.findall(reg2, response) if args.mono else re.findall(reg1, response)
    print(regx)
    for i in regx:
        n = i.split('-')
        note, duration = noteToInt(n[0]), float(Fraction(n[1]))*4
        time = None if len(n) == 2 else float(n[2])
        noteInfo.append([note, duration, time])

    #make midi
    print('[*] Generating MIDI...')
    time = 0
    for i in noteInfo:
        pitch = i[0]
        dur = i[1]
        if not args.mono:
            time = i[2]
        melody.addNote(track, channel, pitch, time, dur, volume)
        if args.mono:
            time += dur
    if counter>=1:
        break
    counter += 1
with open(os.path.join(args.output, 'output.mid'), 'wb') as f:
    melody.writeFile(f)
print('[*] Wrote the MIDI file. Bye!')
