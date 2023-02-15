import re
from bs4 import BeautifulSoup

IGNORE_IDS = ['nav', 'TableOfContents', 'nav-footer']
IGNORE_ELEMENTS = ['img', 'figcaption', 'nav']
FILTERED_ELEMENTS = ["h1", "h2", "h3", "h4", "p", "ul", "ol"]

SCRIPT_BEGIN = "This audio version of the blog post is auto generated. For tables and images, check out the website."
SCRIPT_END = "The end. Hope you enjoyed it and apologies for any errors!"

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


def get_script(loc):
  with open("../build/posts/continuous-glucose-monitoring/index.html") as fob:
    txt = fob.read()
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
