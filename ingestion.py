import pymupdf


def extract_pages(pdf_file):

    pdf = pymupdf.open(stream=pdf_file, filetype="pdf")

    pages = []

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text().strip()

        if text:
            pages.append({
                "page_number": page_number,
                "text": text
            })

    pdf.close()

    return pages