import streamlit as st
import os
from dotenv import load_dotenv

from app.parser import extract_text_and_images
from app.pipeline import generate_ddr
from app.report import generate_report

load_dotenv()

st.title("AI DDR Report Generator")

inspection = st.file_uploader("Upload Inspection Report", type="pdf")
thermal = st.file_uploader("Upload Thermal Report", type="pdf")

if st.button("Generate DDR"):

    if inspection and thermal:

        os.makedirs("data/input", exist_ok=True)
        os.makedirs("data/images", exist_ok=True)

        inspection_path = "data/input/inspection.pdf"
        thermal_path = "data/input/thermal.pdf"

        # Save uploaded PDFs
        with open(inspection_path, "wb") as f:
            f.write(inspection.read())

        with open(thermal_path, "wb") as f:
            f.write(thermal.read())

        st.write("Extracting data from reports...")

        # Extract text and images
        text1 = extract_text_and_images(inspection_path, "data/images")
        text2 = extract_text_and_images(thermal_path, "data/images")

        combined_text = text1 + "\n\n" + text2

        st.write("Generating DDR with AI...")

        # Generate DDR using AI
        report_content = generate_ddr(combined_text)

        # Save report
        report_path = generate_report(report_content)

        st.success("DDR Generated!")

        # Show report inside Streamlit
        st.markdown("## Generated DDR Report")
        st.markdown(report_content)

        # Download button
        with open(report_path, "r", encoding="utf-8") as f:
            st.download_button(
                label="Download DDR Report",
                data=f.read(),
                file_name="DDR_Report.md",
                mime="text/markdown"
            )

    else:
        st.warning("Please upload both Inspection and Thermal reports.")