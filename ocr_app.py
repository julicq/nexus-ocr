import logging
from logging import getLogger

import streamlit as st
import cv2
import easyocr
from pdf2image import convert_from_path
from PIL import Image
import isort
import tempfile

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
        with open(outfile, "a") as f:
            if verbose:
                self.logger.info('Output file {} created'.format(result))
            for i in range(1, file_limit + 1):
                filename = f"{result.stem}_page_{i}.jpg"
                text = self.reader.readtext(filename, detail=0, paragraph=True)
                f.write("\n".join(text))
                if verbose:
                    self.logger.info('Output file written')

    def process_image(self, source, result, verbose):
        img = cv2.imread(source)
        if verbose:
            self.logger.info('Image file is in input')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if verbose:
            self.logger.info('Converting image to gray palette')
        blur = cv2.medianBlur(gray, 1)
        if verbose:
            self.logger.info('Image blur applied')
        outfile = result
        with open(outfile, "a") as f:
            if verbose:
                self.logger.info('Output file {} created'.format(result))
            text = self.reader.readtext(blur, detail=0, paragraph=True)
            f.write("\n".join(text))
            if verbose:
                self.logger.info('Output file filled with OCRd text')

    def run(self, source, result, verbose):
        isort.file(source)
        if source.suffix == ".pdf":
            self.process_pdf(source, result, verbose)
        elif source.suffix in [".png", ".jpg"]:
            self.process_image(source, result, verbose)
        else:
            self.logger.error('Unsupported file format')

def main():
    st.title("OCR Tool")
    st.write("Upload a PDF or image file (PNG or JPG) to extract text.")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg"])
    verbose = st.checkbox("Enable verbose logging")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(uploaded_file.read())
            temp_path = temp.name
        
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name

        ocr_tool = OCRTool()
        ocr_tool.run(temp_path, output_path, verbose)

        with open(output_path, "r") as f:
            st.text(f.read())

if __name__ == "__main__":
    main()
