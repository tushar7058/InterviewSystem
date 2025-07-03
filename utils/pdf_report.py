from fpdf import FPDF
import os

def generate_pdf_report(transcript, faces_detected, output_path="reports/report.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Interview Analysis Report", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Transcript:\n{transcript}")
    pdf.ln(10)
    pdf.cell(0, 10, f"Frames with faces detected: {faces_detected}", ln=True)
    pdf.output(output_path)
    return output_path

if __name__ == "__main__":
    generate_pdf_report("Sample transcript", 5)
