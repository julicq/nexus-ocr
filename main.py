import cv2
import pytesseract
from PIL import Image
import argparse
from pdf2image import convert_from_path

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="path to input file")
ap.add_argument("-o", "--output", required=True,
                help="path to put file with text")
ap.add_argument("-v", "--verbose",
                help="Verbose mode, shows progress", action="count",
                default=0)
args = vars(ap.parse_args())
args = ap.parse_args()

source = args.input
result = args.output
tessdata_dir_config = '--oem 2 --psm 12 --tessdata-dir "/usr/local/share/tessdata/"'

while True:
    if ".pdf" in source:
        PDF_file = source
        if args.verbose:
            print('PDF file is in input')
        pages = convert_from_path(PDF_file, 500)
        image_counter = 1
        for page in pages:
            filename = "page_" + str(image_counter) + ".jpg"
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1
        if args.verbose:
            print('{} pages from PDF retrieved'.format(image_counter-1))

        file_limit = image_counter - 1
        outfile = result
        f = open(outfile, "a")
        if args.verbose:
            print('Output file {} created'.format(result))
        for i in range(1, file_limit + 1):
            filename = "page_" + str(i) + ".jpg"
            text = str((pytesseract.image_to_string(Image.open(filename))))
            text = text.replace('-\n', '')
            f.write(text)
            if args.verbose:
                print('Output file written')
        f.close()
        break
    else:
        img = cv2.imread(source)
        if args.verbose:
            print('Image file is in input')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if args.verbose:
            print('Converting image to gray palette')
        blur = cv2.medianBlur(gray, 1)
        if args.verbose:
            print('Image blur applied')
        # thresh = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # if args.verbose:
        #     print('Image threshold applied')

        outfile = result
        f = open(outfile, "a")
        if args.verbose:
            print('Output file {} created'.format(result))
        text = str(pytesseract.image_to_string(blur, lang='eng', config=tessdata_dir_config))
        f.write(text)
        if args.verbose:
            print('Output file filled with OCRd text')
        f.close()

        break
