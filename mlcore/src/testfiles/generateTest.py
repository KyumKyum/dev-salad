import json
import re

def parse_blocks(text):
    # Split on lines of ====
    raw_blocks = re.split(r"=+\n", text)
    items = []
    idx = 1

    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.splitlines()
        # First line is the title
        title = lines[0].strip()

        # Find where the “source” line (e.g. Reddit/, Dev.to, HackerNews, etc) begins
        desc_lines = []
        for line in lines[1:]:
            if re.match(r"^(Reddit|Dev\.to|HackerNews|GitHub Trending|TechCrunch)", line):
                break
            desc_lines.append(line)
        description = "\n".join(desc_lines).strip()

        items.append({
            "id": str(idx),
            "title": title,
            "description": description
        })
        idx += 1

    return items

if __name__ == "__main__":
    # 1) Copy–paste all your scraped output into scraped.txt
    # 2) Run this script: python make_json.py
    with open("scraped.txt", encoding="utf-8") as f:
        raw = f.read()

    parsed = parse_blocks(raw)
    with open("items.json", "w", encoding="utf-8") as outf:
        json.dump(parsed, outf, indent=2, ensure_ascii=False)

    print(f"Wrote {len(parsed)} items to items.json")
