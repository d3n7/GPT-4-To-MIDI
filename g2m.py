import os, requests, argparse, re
from fractions import Fraction
from midiutil.MidiFile import MIDIFile
import openai, mido

#settings
openaiKey = '<YOUR API KEY>'
system = 'You are MusicGPT, a music creation and completion chat bot that. When a user gives you a prompt,' \
          ' you return them a song showing the notes, durations, and times that they occur. Respond with just the music.' \
         '\n\nNotation looks like this:\n(Note-duration-time in beats)\nC4-1/4-0, Eb4-1/8-2.5, D4-1/4-3, F4-1/4-3 etc.'

#alternative notation
#'\n\nNotation looks like this:\n(Note-duration in beats-time in beats)\nC4-3-0, Eb4-0.5-2.5, D4-1-3, A4-0.5-3, G4-0.5-3.5, D4-1-4, F4-1-4 etc.' \

#environment
path = os.path.realpath(os.path.dirname(__file__))

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prompt', help='specify prompt to use (default: Jazz!)', default='Jazz!')
parser.add_argument('-c', '--chat', help='send follow up messages to make revisions, continuations, etc. (type \'exit\' to quit)', action='store_true')
parser.add_argument('-l', '--load', help='load a MIDI file to be appended to your prompt')
parser.add_argument('-v', '--verbose', help='display GPT-4 output', action='store_true')
parser.add_argument('-o', '--output', help='specify output directory (default: current)', default=path)
parser.add_argument('-a', '--auth', help='specify openai api key (edit this script file to set a default)', default=openaiKey)
args = parser.parse_args()

#other vars n functions
notes = [['C'], ['Db', 'C#'], ['D'], ['Eb', 'D#'], ['E'], ['F'], ['Gb', 'F#'], ['G'], ['Ab', 'G#'], ['A'], ['Bb', 'A#'], ['B']]

def noteToInt(n):
    oct = int(n[-1])
    letter = n[:-1]
    id = 0
    for ix, x in enumerate(notes):
        for y in x:
            if letter == y:
                id = ix
    return id+oct*12+12

def midiToStr(mPath):
    midIn = mido.MidiFile(os.path.expanduser(mPath))
    ticks = midIn.ticks_per_beat
    midOut = []
    globalT = 0
    opens = {}
    for track in midIn.tracks:
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                globalT += msg.time/ticks
                if msg.note in opens:
                    noteTime = opens[msg.note]
                    noteTime = str(int(noteTime)) if noteTime.is_integer() else str(noteTime)
                    noteDur = str(Fraction((globalT-noteTime)/4))
                    noteDur = str(round((globalT-noteTime),3)) if len(notDur)>=6 else noteDur
                    midOut.append("-".join([notes[msg.note%12][0]+str(msg.note//12-1), noteDur, noteTime]))
                    del opens[msg.note]
                if msg.type == 'note_on':
                    opens[msg.note] = globalT
    return '\n'+', '.join(midOut)+'\n'

prompt = args.prompt
if args.load:
    try:
        prompt += midiToStr(args.load)
    except:
        print("[!] There was an error parsing your MIDI file. Make sure the path is correct.")
        exit()

history = [{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}]

# main loop
while 1:
    #openai request
    print('[*] Making request to OpenAI API')
    openai.api_key = args.auth
    r = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages = history
    )
    response = r['choices'][0]['message']['content']
    if args.verbose:
        print('\n'+response+'\n')
    history.append({'role': 'assistant', 'content': response})

    #parse content
    print('[*] Parsing content')
    noteInfo = []
    #thanks GPT-4 for this monstrosity of regex that seems to work
    #r'(?<![A-Za-z\d])([A-G](?:#|b)?\d-\d+(?:\.\d+)?-\d+(?:\.\d+)?)(?![A-Za-z\d])' alternative notation
    for i in re.findall(r'(?<![A-Za-z\d])([A-G](?:#|b)?\d(?:-\d+(?:\/\d+)?(?:-\d+(?:\.\d+)?)?)+)(?![A-Za-z\d])', response):
        n = i.split('-')
        noteInfo.append([noteToInt(n[0]), float(Fraction(n[1]))*4, float(n[2])]) #note, duration, time

    #make midi
    melody = MIDIFile(1, deinterleave=False)
    for i in noteInfo:
        pitch, dur, time = i
        melody.addNote(0, 0, pitch, time, dur, 100)
    with open(os.path.join(args.output, 'output.mid'), 'wb') as f:
        melody.writeFile(f)
    print('[*] Wrote the MIDI file.')

    #break loop or get next prompt
    if args.chat:
        prompt = input('\nNext prompt> ')
        print('\n')
        if prompt == 'exit':
            break
        else:
            history.append({'role': 'user', 'content': prompt})
    else:
        break
