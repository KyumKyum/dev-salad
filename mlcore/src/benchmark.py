import json
import time
from preprocess import clean_text
from summarizer import summarize
from extractor import spacy_nouns
from terms import tech_terms, filter_tech_terms

def process_item(item):
    # 1. Clean
    text = clean_text(item["title"] + " " + item["description"])
    # 2. Summarize
    summary = summarize(text)
    # 3. Extract nouns
    nouns = spacy_nouns(summary)
    # 4. Filter to tech terms
    techs = filter_tech_terms(nouns, tech_terms)
    return techs

def benchmark(items):
    stats = {
        "clean": 0.0,
        "summ": 0.0,
        "extract": 0.0,
        "filter": 0.0,
        "total": 0.0
    }

    N = len(items)
    start_total = time.perf_counter()
    details = []
    for idx, item in enumerate(items, start=1):
        t0 = time.perf_counter()
        text = clean_text(item["title"] + " " + item["description"])
        t1 = time.perf_counter()
        summary = summarize(text)
        t2 = time.perf_counter()
        nouns = spacy_nouns(summary)
        t3 = time.perf_counter()
        techs = filter_tech_terms(nouns, tech_terms)
        t4 = time.perf_counter()

        stats["clean"]   += (t1 - t0)
        stats["summ"]    += (t2 - t1)
        stats["extract"] += (t3 - t2)
        stats["filter"]  += (t4 - t3)

        details.append({
            "id": idx,
            "text": text,
            "summary": summary,
            "nouns": nouns,
            "techs": techs
        })

    stats["total"] = time.perf_counter() - start_total

    with open("./result", "w", encoding="utf-8") as outf:
        for d in details:
            outf.write(json.dumps(d, ensure_ascii=False) + "\n")

    print(f"Processed {N} items in {stats['total']:.2f}s  → {N/stats['total']:.1f} items/sec")
    print(f"  clean:   {stats['clean']:.2f}s ({stats['clean']/N*1000:.1f} ms/item)")
    print(f"  summary: {stats['summ']:.2f}s ({stats['summ']/N*1000:.1f} ms/item)")
    print(f"  extract: {stats['extract']:.2f}s ({stats['extract']/N*1000:.1f} ms/item)")
    print(f"  filter:  {stats['filter']:.2f}s ({stats['filter']/N*1000:.1f} ms/item)")

if __name__ == "__main__":
    with open("test_data.json") as f:
        items = json.load(f)
    benchmark(items)
