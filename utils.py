import pdfplumber


def _load_pdf(pdf_path):
    """
    Load the contents of a PDF file and return a list of dictionaries,
    each containing the content of one page and the page number.

    Parameters:
        pdf_path (str): Path to the PDF file.

    Returns:
        List[dict]: A list of dictionaries with page content and page number.
    """
    data = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    data.append({"content": text, "page": str(i + 1)})
    except Exception as e:
        print(f"Error reading PDF file: {e}")

    return data
