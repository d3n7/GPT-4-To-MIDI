# GPT-4-To-MIDI-Music
Text prompt to MIDI File using OpenAI's GPT-4

Since GPT-4 is apparently trained on musical data, I made this script to convert text prompts into short melodies and then MIDI files.

# Dependencies:
```pip install openai midiutil```

# Usage:
```  -h, --help            show this help message and exit
  -p PROMPT, --prompt PROMPT
                        specify prompt to use (default: Jazz!)
  -o OUTPUT, --output OUTPUT
                        specify output directory (default: current)
  -a AUTH, --auth AUTH  specify openai api key (edit this script file to set a
                        default)
