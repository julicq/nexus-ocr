import logging
from logging import getLogger

import click
import cv2
import isort
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

isort.file("main.py")

logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@click.command()
@click.option('--input', '-i', required=True,
              help='Path to file(.pdf/.png/.jpg) to be processed',
              type=click.Path(exists=True, dir_okay=False, readable=True), )
@click.option('--output', '-o', default="output.text",
              help='Path to file to store result',
              type=click.Path(dir_okay=False), )
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose log mode', )
def ocr(input, output, verbose):
    source = input
    result = output
    # for Windows provide if getting error
    # Example config: r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"'
    # It's important to add double quotes around the dir path.
    tessdata_dir_config = '--oem 2 --psm 12 --tessdata-dir "/usr/local/share/tessdata/"'

    while True:
        if source.split(".")[-1] == "pdf":
            pdf_file = source
            if verbose:
                logging.info('PDF file is in input')
            pages = convert_from_path(pdf_file, 500)
            image_counter = 1
            for page in pages:
                filename = "page_" + str(image_counter) + ".jpg"
                page.save(filename, 'JPEG')
                image_counter = image_counter + 1
            if verbose:
                logging.info('{} pages from PDF retrieved'.format(image_counter - 1))

            file_limit = image_counter - 1
            outfile = result
            f = open(outfile, "a")
            if verbose:
                logging.info('Output file {} created'.format(result))
            for i in range(1, file_limit + 1):
                filename = "page_" + str(i) + ".jpg"
                text = str((pytesseract.image_to_string(Image.open(filename))))
                text = text.replace('-\n', '')
                f.write(text)
                if verbose:
                    logging.info('Output file written')
            f.close()
            break
        else:
            if source.split(".")[-1] == "png" or source.split(".")[-1] == "jpg":
                img = cv2.imread(source)
                if verbose:
                    logging.info('Image file is in input')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                if verbose:
                    logging.info('Converting image to gray palette')
                blur = cv2.medianBlur(gray, 1)
                if verbose:
                    logging.info('Image blur applied')
                # thresh = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                # if verbose:
                #     logging.info('Image threshold applied')
                outfile = result
                f = open(outfile, "a")
                if verbose:
                    logging.info('Output file {} created'.format(result))
                text = str(pytesseract.image_to_string(blur, lang='eng', config=tessdata_dir_config))
                f.write(text)
                if verbose:
                    logging.info('Output file filled with OCRd text')
                f.close()
                break
        print('Unsupported file format')
        break


if __name__ == "__main__":
    ocr()
