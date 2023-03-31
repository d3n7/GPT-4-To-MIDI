# GPT-4 To MIDI
Text prompt to MIDI File using OpenAI's GPT-4. For now it's monophonic.

# Dependencies:
```pip install openai midiutil```

# Usage:
Ask it in plain english to generate, including any musical details that you want.

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
  -a AUTH, --auth AUTH  specify openai api key (edit this script file to set a
                        default)
