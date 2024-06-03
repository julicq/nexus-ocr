import logging
from logging import getLogger

import streamlit as st
import cv2
import easyocr
from pdf2image import convert_from_path
from PIL import Image
import tempfile
from pathlib import Path
import pkg_resources

# Check the Pillow version
pillow_version = pkg_resources.get_distribution("Pillow").version
resampling = Image.Resampling.LANCZOS if pillow_version >= "9.1.0" else Image.LANCZOS

class OCRTool:
    def __init__(self):
        self.logger = getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.reader = easyocr.Reader(['en'])  # Initialize easyocr Reader with English language

    def process_pdf(self, source, result, verbose):
        if verbose:
            self.logger.info('PDF file is in input')
        pages = convert_from_path(source, 500)
        image_counter = 1
        for page in pages:
            filename = f"{result.stem}_page_{image_counter}.jpg"
            page.save(filename, 'JPEG')
            image_counter += 1
        if verbose:
            self.logger.info('{} pages from PDF retrieved'.format(image_counter - 1))

        file_limit = image_counter - 1
        outfile = result
        with open(outfile, "a", encoding='utf-8') as f:
            if verbose:
                self.logger.info('Output file {} created'.format(result))
            for i in range(1, file_limit + 1):
                filename = f"{result.stem}_page_{i}.jpg"
                text = self.reader.readtext(filename, detail=0, paragraph=True)
                f.write("\n".join(text) + "\n")
                if verbose:
                    self.logger.info('Output file written')

    def process_image(self, source, result, verbose):
        img = cv2.imread(str(source))
        if verbose:
            self.logger.info('Image file is in input')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if verbose:
            self.logger.info('Converting image to gray palette')
        blur = cv2.medianBlur(gray, 1)
        if verbose:
            self.logger.info('Image blur applied')
        outfile = result
        with open(outfile, "a", encoding='utf-8') as f:
            if verbose:
                self.logger.info('Output file {} created'.format(result))
            text = self.reader.readtext(blur, detail=0, paragraph=True)
            f.write("\n".join(text) + "\n")
            if verbose:
                self.logger.info('Output file filled with OCRd text')

    def run(self, source, result, verbose):
        if verbose:
            self.logger.info(f"Processing file: {source}")
        
        extension = source.suffix.lower()
        if verbose:
            self.logger.info(f"File extension: {extension}")
        
        if extension == ".pdf":
            self.process_pdf(source, result, verbose)
        elif extension in [".png", ".jpg", ".jpeg"]:
            self.process_image(source, result, verbose)
        else:
            self.logger.error('Unsupported file format')

def main():
    st.title("OCR Tool")
    st.write("Upload a PDF or image file (PNG or JPG) to extract text.")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg"])
    verbose = st.checkbox("Enable verbose logging")

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp:
            temp.write(uploaded_file.read())
            temp_path = Path(temp.name)
        
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name

        ocr_tool = OCRTool()
        ocr_tool.run(temp_path, Path(output_path), verbose)

        with open(output_path, "r", encoding='utf-8') as f:
            st.text(f.read())

if __name__ == "__main__":
    main()
