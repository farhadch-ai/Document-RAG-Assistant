from ingestion import extract_pages


def create_chunks(pages, chunk_size=800, overlap=200):

    chunks = []

    full_text = ""
    page_ranges = []

    current_position = 0

    for page in pages:

        text = page["text"]

        start_position = current_position

        full_text += text + "\n"

        current_position = len(full_text)

        page_ranges.append({
            "page_number": page["page_number"],
            "start": start_position,
            "end": current_position
        })

    start = 0

    while start < len(full_text):

        end = start + chunk_size

        chunk_text = full_text[start:end]

        chunk_pages = []

        for page in page_ranges:

            if page["start"] < end and page["end"] > start:
                chunk_pages.append(page["page_number"])

        chunks.append({
            "page_numbers": chunk_pages,
            "text": chunk_text
        })

        start = end - overlap

    return chunks

"""
pages = extract_pages()

chunks = create_chunks(pages)

"""