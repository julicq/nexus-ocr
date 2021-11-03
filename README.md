# nexus-ocr

## Task:
Create a command‐line tool to do OCR and extract text from a given scanned document image.

### Input
Scanned document images ( include English only ). Your command needs to accept the following file formats.
* PNG 
* JPEG 
* PDF

### Output
Extracted texts as a text file.

``python your_code.py --input=./test.pdf --output=output.text --verbose``

### Interface

- –input : input file
- –output : output text file
- –verbose : verbose mode ( output detailed logs )

### Requirements
Before doing the OCR process with TessaractOCR, you should do pre‐processing to improve OCR accuracy. 
Afterer doing the OCR process with TessaractOCR, you should do post processing to do text correctioon to remove OCR mis‐recogniton.

### Regulations
* Use *Click* as an command line interface builder 
* Use *Poetry* to install required thirdparty packages
* Use *yapf* and *isort* to format python codes
* Use logging package to do output. Never use ``print`` for log output. 
* Use ``.gitignore`` to exclude unnesesarry files.
* Upload your code to GitHub
