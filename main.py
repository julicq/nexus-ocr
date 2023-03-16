import logging
from logging import getLogger

import click
import cv2
import isort
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


class OCRTool:
    def __init__(self):
        self.logger = getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def process_pdf(self, source, result, verbose):
        pdf_file = source
        if verbose:
            self.logger.info('PDF file is in input')
        pages = convert_from_path(pdf_file, 500)
        image_counter = 1
        for page in pages:
            filename = "page_" + str(image_counter) + ".jpg"
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1
        if verbose:
            self.logger.info('{} pages from PDF retrieved'.format(image_counter - 1))

        file_limit = image_counter - 1
        outfile = result
        f = open(outfile, "a")
        if verbose:
            self.logger.info('Output file {} created'.format(result))
        for i in range(1, file_limit + 1):
            filename = "page_" + str(i) + ".jpg"
            text = str((pytesseract.image_to_string(Image.open(filename))))
            text = text.replace('-\n', '')
            f.write(text)
            if verbose:
                self.logger.info('Output file written')
        f.close()

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
        tessdata_dir_config = '--oem 2 --psm 12 --tessdata-dir "/usr/local/share/tessdata/"'
        outfile = result
        f = open(outfile, "a")
        if verbose:
            self.logger.info('Output file {} created'.format(result))
        text = str(pytesseract.image_to_string(blur, lang='eng', config=tessdata_dir_config))
        f.write(text)
        if verbose:
            self.logger.info('Output file filled with OCRd text')
        f.close()

    def run(self, source, result, verbose):
        isort.file(source)
        if source.split(".")[-1] == "pdf":
            self.process_pdf(source, result, verbose)
        elif source.split(".")[-1] == "png" or source.split(".")[-1] == "jpg":
            self.process_image(source, result, verbose)
        else:
            self.logger.error('Unsupported file format')


@click.command()
@click.option('--input', '-i', required=True,
              help='Path to file(.pdf/.png/.jpg) to be processed',
              type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option('--output', '-o', default="output.text",
              help='Path to file to store result',
              type=click.Path(dir_okay=False))
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose log mode')
def main(input, output, verbose):
    ocr_tool = OCRTool()
    ocr_tool.run(input, output, verbose)


if __name__ == "__main__":
    main()
