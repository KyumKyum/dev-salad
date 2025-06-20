import re
from bs4 import BeautifulSoup

def clean_text(text:str) -> str:
    # Preprocess: Remove HTML, URLs, control chars, lowercase
    text = BeautifulSoup(text, "lxml").get_text(separator=" ")
    text = re.sub(r"http\S+|\s+", " ", text)
    return text.strip().lower()
