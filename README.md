# GPT-4 To MIDI
Text prompt to MIDI File using OpenAI's GPT-4

# Dependencies:
```pip install openai midiutil```

# Usage:
Ask it in plain english to generate, including any musical details that you want.

```python g2m.py -p "Exciting arpeggios in D minor pentatonic, 4 measures"```
```  -h, --help            show this help message and exit
  -p PROMPT, --prompt PROMPT
                        specify prompt to use (default: Jazz!)
  -o OUTPUT, --output OUTPUT
                        specify output directory (default: current)
  -a AUTH, --auth AUTH  specify openai api key (edit this script file to set a
                        default)
