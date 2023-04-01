# GPT-4 To MIDI
Text prompt to MIDI File using OpenAI's GPT-4. For now it's monophonic.

<img width="637" alt="Screen Shot 2023-04-01 at 9 57 21 AM" src="https://user-images.githubusercontent.com/29033313/229273576-7c0b9313-ca48-4c9a-8a37-8989176c8dec.png">


# Dependencies:
```pip install openai midiutil```

# Usage:
Ask it in plain english to generate, including any musical details that you want.

Input:

```python g2m.py -p "Plan out a romantic chord progression. Arpeggiate each full chord for one bar with 8th and 16th notes."```

Output:

https://user-images.githubusercontent.com/29033313/229306944-fa8be2db-75f1-449b-a4a1-e9885eeb7e75.mp4

Input:

```python g2m.py -p "Plan out an evil sounding chord progression with 4 chords. Then articulate each chord for one bar each using 8th notes and 16th notes."```

Output:

https://user-images.githubusercontent.com/29033313/229309003-7bd18206-4c03-4203-a6d8-e1ea8661d233.mp4

Input:

```python g2m.py -p "jazzy pentatonic, meandering up and down, rhythmic variation, syncopated, over 100 notes total. Plan the chord progression beforehand."```

Output:

https://user-images.githubusercontent.com/29033313/229188943-dc4d257c-61d6-47bb-bc58-9e81e637005e.mp4

Input:

```python g2m.py -p "A minor pentatonic flourishes ranging from C2 to C7, ranging from (rarely) 64th notes to 8th notes, over 200 notes total" -n 3```

Output:

https://user-images.githubusercontent.com/29033313/229198071-ef964ea9-958e-4fb1-921c-9428b74f2261.mp4

Full options:
```  -h, --help            show this help message and exit
  -p PROMPT, --prompt PROMPT
                        specify prompt to use (default: Jazz!)
  -o OUTPUT, --output OUTPUT
                        specify output directory (default: current)
  -a AUTH, --auth AUTH  specify openai api key (edit this script file to set a default)
  -n NUM, --num NUM     generate n number of outputs and merge them (context unaware)
