from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import textwrap

def generate_pdf_report(content: str, output_path: str):
    """
    Generates a PDF report with line wrapping.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    text = c.beginText(50, height - 50)
    text.setFont("Helvetica", 12)

    max_chars_per_line = 90  # Adjust this based on your font size & margin

    for line in content.strip().split("\n"):
        wrapped_lines = textwrap.wrap(line.strip(), width=max_chars_per_line)
        for wrapped_line in wrapped_lines:
            text.textLine(wrapped_line)
        text.textLine("")  # Extra space between sections

    c.drawText(text)
    c.save()
