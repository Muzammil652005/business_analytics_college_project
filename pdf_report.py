from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(prediction):
    file_name = "prediction_report.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    c.setFont("Helvetica", 14)

    c.drawString(100, 800, "Business Analytics Prediction Report")
    c.drawString(100, 760, f"Predicted Sales Value: ₹ {prediction:.2f}")
    c.drawString(100, 720, "Generated using Streamlit & Machine Learning")

    c.save()
    return file_name
