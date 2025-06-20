from transformers import pipeline

summarizer = pipeline("summarization", model = "facebook/bart-large-cnn")

def summarize(text: str) -> str:
    # don’t try to summarize very short text
    if len(text.split()) < 50:
        return text

    # ask the pipeline to truncate if the input is too long
    try:
        result = summarizer(
            text,
            max_length=60,
            min_length=20,
            do_sample=False,
        )
    except Exception as e:
        # pipeline itself failed
        print(f"[summarizer error] {e}")
        return text

    # if the pipeline returned an empty list, just return the original
    if not result:
        return text

    return result[0].get("summary_text", text)
