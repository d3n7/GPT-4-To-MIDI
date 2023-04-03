# GPT-4 To MIDI
Text prompt to MIDI File using OpenAI's GPT-4. Now with polyphony and MIDI input!

<img width="637" alt="Screen Shot 2023-04-01 at 9 57 21 AM" src="https://user-images.githubusercontent.com/29033313/229273576-7c0b9313-ca48-4c9a-8a37-8989176c8dec.png">


# Dependencies:
```pip install openai midiutil mido```

# Usage:
Ask it in plain english to generate, including any musical details that you want.

Input:

```
python g2m.py -p "Full piece of melancholy music with multiple parts. Plan out the structure beforehand, including chords, parts (soprano, alto, tenor, bass), meter, etc." -c
[*] Making request to OpenAI API
[*] Parsing content
[*] Wrote the MIDI file.

Next prompt> Keep it Eb instead of E for the second note 

...

Next prompt> Write a simple soprano melody in the high octave range that fits over this piece.
```

Output:

https://user-images.githubusercontent.com/29033313/229352561-a0b16078-4d5b-4381-b433-673d38d4d987.mp4

Input:

```python g2m.py -p "Full piece by Mozart with multiple parts. Plan out the structure beforehand, including chords, parts (soprano, alto, tenor, bass), meter, etc. Over 400 notes total."```

Output:

https://user-images.githubusercontent.com/29033313/229316684-028d2e55-9f4e-4a0e-a47a-a99452d9d14f.mp4

Input:

```
python g2m.py -p "twinkle twinkle little star" -c
[*] Parsing content
[*] Wrote the MIDI file.

Next prompt> Tranpose it to A minor
```

Output:

https://user-images.githubusercontent.com/29033313/229319912-6b3ec70c-d77b-4e6e-a537-41a9c5aeabc6.mp4

Full options:
```
  -h, --help            show this help message and exit
  -p PROMPT, --prompt PROMPT
                        specify prompt to use (default: Jazz!)
  -c, --chat            send follow up messages to make revisions,
                        continuations, etc. (type 'exit' to quit)
  -l LOAD, --load LOAD  load a MIDI file to be appended to your prompt
  -v, --verbose         display GPT-4 output
  -m, --mono            alternative system to generate monophonic MIDI outputs
  -o OUTPUT, --output OUTPUT
                        specify output directory (default: current)
  -a AUTH, --auth AUTH  specify openai api key (edit this script file to set a
                        default)
