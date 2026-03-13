from app.parser import extract_text_and_images
from app.pipeline import generate_ddr
from app.report import generate_report


inspection = "data/input/inspection.pdf"
thermal = "data/input/thermal.pdf"

text1 = extract_text_and_images(inspection, "data/images")
text2 = extract_text_and_images(thermal, "data/images")

text = text1 + text2

report = generate_ddr(text)

generate_report(report)

print("DDR report generated.")
