import argparse
import re
from bs4 import BeautifulSoup
from pathlib import Path
from TTS.api import TTS
from typing import Union

IGNORE_IDS = ['nav', 'TableOfContents', 'nav-footer']
IGNORE_ELEMENTS = ['img', 'figcaption', 'nav', 'audio']
FILTERED_ELEMENTS = ["h1", "h2", "h3", "h4", "p", "ul", "ol"]

SCRIPT_BEGIN = "This audio version of the blog post is auto generated. For tables and images, check out the website."
SCRIPT_END = "The end. Hope you enjoyed it and apologies for any errors!"

MODEL = 'tts_models/en/vctk/vits'
SPEAKER = "p230"

REPLACE_TEXT = {
  r"\(.*?\)": "",
  r"wrt.": "with respect to",
  r"etc.": "et cetera.",
  r"~": "approximately ",
  r"\*.*?\*": "",
  r"\/": "  slash  ",
  r"\.com": "dot com",
  r"\@": "at",
  r"\.\.": ".",
  r" \.": ".",
  r"  ": " ",
}


def get_html_file(html: Union[str, Path]) -> Path:
  if isinstance(html, str):
    html = Path(html)
  if html.is_file():
    if html.suffix != ".html":
      raise Exception("The html-file is not an html file!?")
  else:
    html = html / "index.html"
  return html


def get_script(html_loc: Union[str, Path]) -> str:
  html = get_html_file(html_loc)
  with open(html) as fob:
    txt = fob.read().encode('utf-8')
  soup = BeautifulSoup(txt, "html.parser")

  res = []

  for ele in soup.find_all(FILTERED_ELEMENTS):
    text = ele.get_text().strip()
    wrong_ids = 'id' in ele.parent.attrs and ele.parent.attrs['id'] in IGNORE_IDS
    wrong_elements = ele.parent.name in IGNORE_ELEMENTS
    empty_text = text == ''
    if wrong_ids or wrong_elements or empty_text:
      continue

    res.append({
      'type': ele.name,
      'text': text,
      'parent_tag': ele.parent.name,
      'parent_attrs': ele.parent.attrs,
    })

  final_text = SCRIPT_BEGIN
  for ele in res:
    pad = "\n\n" if ele['type'] in ['h1', 'h2', 'h3', 'h4'] else "\n"
    final_text += f'{pad}{ele["text"]}'
  final_text += f"\n\n{SCRIPT_END}"

  for pattern, replacement in REPLACE_TEXT.items():
    final_text = re.sub(pattern, replacement, final_text)

  return final_text


def get_audio(html_loc: str, script_loc: str, audio_loc: str) -> None:
  script_dir = Path(script_loc)
  audio_dir = Path(audio_loc)
  html = get_html_file(html_loc)

  script_dir.mkdir(parents=True, exist_ok=True)
  audio_dir.mkdir(parents=True, exist_ok=True)

  filename = html.parts[-2] if html.stem == "index" else html.stem
  script_path = script_dir / f"{filename}.txt"
  audio_path = audio_dir / f"{filename}.wav"

  print("\n\n1. Generating Script")
  script = get_script(html)
  print("\n\n2. Generating Audio")
  if Path(script_path).exists():
    with open(script_path) as fob:
      if fob.read() == script:
        print(f"Audio already exists at {audio_path}.")
        return

  tts = TTS(MODEL, progress_bar=True, gpu=True)
  tts.tts_to_file(text=script, file_path=audio_path, speaker=SPEAKER)
  with open(script_path, "w") as fob:
    fob.write(script)
  print(f"Audio rendered at {audio_path}.")
  return


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Generate an audio-script and audio file from a blog post')
  parser.add_argument('mode', help='generation mode [script, audio]', choices=["script", "audio"])
  parser.add_argument('--html-loc', help='location of the html file', required=True)
  parser.add_argument('--audio-script-loc', help='location of audio scripts', default="./static/audio_scripts")
  parser.add_argument('--audio-loc', help='location of generated audio files', default="./static/audios")
  args = parser.parse_args()

  if args.mode == "script":
    print(get_script(args.html_loc))
  elif args.mode == "audio":
    get_audio(args.html_loc, args.audio_script_loc, args.audio_loc)
