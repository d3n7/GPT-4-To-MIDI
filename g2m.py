import os, requests, argparse, re
from fractions import Fraction
from midiutil.MidiFile import MIDIFile
import openai

#settings
openaiKey = '<YOUR API KEY HERE>'
system = 'You are MusicGPT, a music creation and completion chat bot that. When a user gives you a prompt,' \
         'you return them a melody showing the notes and the rhythms. Respond only with the music.' \
         '\n\nNotation looks like this:\nC5-1/4, E5 1/2 etc.'

#environment
path = os.path.realpath(os.path.dirname(__file__))

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prompt", help="specify prompt to use (default: Jazz!)", default="Jazz!")
parser.add_argument("-o", "--output", help="specify output directory (default: current)", default=path)
parser.add_argument("-a", "--auth", help="specify openai api key (edit this script file to set a default)", default=openaiKey)
args = parser.parse_args()

#openai api
print("[*] Making request to OpenAI API")
openai.api_key = args.auth
r = openai.ChatCompletion.create(
    model = 'gpt-4',
    messages = [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': args.prompt}
    ]
)
content = r['choices'][0]['message']['content']

#parse content
print("[*] Parsing content")
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
noteInfo = []
#thanks GPT-4 for this monstrosity of regex that seems to work
for i in re.findall(r'(?<![A-Za-z\d])([A-G](?:#|b)?\d-(?:\d+\/\d+|\d+))(?![A-Za-z\d])', content):
    note, duration = i.split("-")
    note = noteToInt(note)
    duration = float(Fraction(duration))*4
    noteInfo.append([note, duration])

#make midi
print("[*] Generating MIDI file")
melody = MIDIFile(1)
track = 0
channel = 0
time = 0
volume = 100
for i in noteInfo:
    pitch = i[0]
    dur = i[1]
    melody.addNote(track, channel, pitch, time, dur, volume)
    time += dur
with open(os.path.join(args.output, 'output.mid'), 'wb') as f:
    melody.writeFile(f)