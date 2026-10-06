from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF resume.

    Works with:
    - Streamlit UploadedFile
    - File-like PDF objects
    """

    if pdf_file is None:
        raise ValueError("No resume file was provided.")

    try:
        # Make sure reading starts from the beginning
        if hasattr(pdf_file, "seek"):
            pdf_file.seek(0)

        reader = PdfReader(pdf_file)

    except Exception as e:
        raise ValueError(
            f"Unable to read the PDF resume: {e}"
        )

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found in the PDF. "
            "The resume may be scanned/image-based."
        )

    return text