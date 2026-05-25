import os
from reportlab.pdfgen import canvas
from io import BytesIO

# Create test PDF with factual claims
output = BytesIO()
c = canvas.Canvas(output)
c.drawString(100, 750, "PDF Test Document")
c.drawString(100, 700, "Claim 1: OpenAI reached 200 million users in 2025.")
c.drawString(100, 650, "Claim 2: India AI market is worth 17 billion dollars.")
c.drawString(100, 600, "Claim 3: The Earth has 8 billion people in 2025.")
c.drawString(100, 550, "Claim 4: COVID-19 pandemic started in 2019.")
c.save()
output.seek(0)

with open("test_doc.pdf", "wb") as f:
    f.write(output.getvalue())
    
print("✓ Test PDF created: test_doc.pdf")
