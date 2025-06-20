import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load('en_core_web_sm')

def spacy_nouns(text: str):
    doc = nlp(text)
    return [tok.lemma_ for tok in doc if tok.pos_ in ("NOUN", "PROPN") and len(tok) > 2]

def tfidf_keywords(corpus: list[str], top_k=10):
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
    X = vec.fit_transform(corpus)
    features = vec.get_feature_names_out()
    scores = X.sum(axis=0).A1
    idx = scores.argsort()[::-1]
    return [(features[i], scores[i]) for i in idx[:top_k]]