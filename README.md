# dhwani

Create audio recordings of blog posts (generated html files).

## Usage
```
python dhwani/dhwani.py -h
usage: dhwani.py [-h] --html-loc HTML_LOC [--audio-script-loc AUDIO_SCRIPT_LOC]
                 [--audio-loc AUDIO_LOC]
                 {script,audio}

Generate an audio-script and audio file from a blog post

positional arguments:
  {script,audio}        generation mode [script, audio]

optional arguments:
  -h, --help            show this help message and exit
  --html-loc HTML_LOC   location of the html file
  --audio-script-loc AUDIO_SCRIPT_LOC
                        location of audio scripts
  --audio-loc AUDIO_LOC
                        location of generated audio files
```
## Example
```
python dhwani/dhwani.py audio --html-loc <path-to-html-file/hugo post dir> --audio-script-loc resources/audio_scripts --audio-loc resources/audios
```
