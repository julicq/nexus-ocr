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

### Regulations
* Use *Click* as an command line interface builder 
* Use *Poetry* to install required thirdparty packages
* Use *yapf* and *isort* to format python codes
* Use logging package to do output. Never use ``print`` for log output. 

# OCR Streamlit Application

This application performs Optical Character Recognition (OCR) on PDF and image files (PNG, JPG) using `easyocr` and `pdf2image` libraries. The application is built using Streamlit for a user-friendly web interface.

## Features

- Extract text from PDF files.
- Extract text from image files (PNG, JPG).
- Supports verbose logging for detailed processing information.

## Requirements

- Python 3.7+
- Streamlit
- OpenCV
- EasyOCR
- PDF2Image
- Poppler (for PDF support)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/ocr-streamlit-app.git
    cd ocr-streamlit-app
    ```

2. **Set up a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Install Poppler:**

    ### On Windows:
    - Download the latest release from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/).
    - Extract the ZIP file to a directory, e.g., `C:\poppler`.
    - Add the `bin` directory of Poppler to your system PATH.
        - Open the Start Menu and search for "Environment Variables".
        - Select "Edit the system environment variables".
        - Click "Environment Variables...".
        - Under "System variables", find and select the `Path` variable, then click "Edit...".
        - Click "New" and add the path to the `bin` directory, e.g., `C:\poppler\bin`.

    ### On macOS:
    - Install Homebrew if not already installed:
        ```sh
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
    - Install Poppler using Homebrew:
        ```sh
        brew install poppler
        ```

    ### On Linux:
    - For Debian-based systems (Ubuntu):
        ```sh
        sudo apt-get install poppler-utils
        ```
    - For Red Hat-based systems (Fedora):
        ```sh
        sudo dnf install poppler-utils
        ```

## Running the Application

1. **Start the Streamlit app:**

    ```sh
    streamlit run ocr_app.py
    ```

2. **Open your web browser and go to:**

    ```
    http://localhost:8501
    ```

3. **Upload a PDF or image file and extract text.**

## Example

Here's a quick example of how to use the application:

1. Run the Streamlit app.
2. Upload a PDF or image file.
3. Click on the "Process" button.
4. The extracted text will be displayed on the web page.

## Troubleshooting

- **AttributeError: module 'PIL.Image' has no attribute 'Resampling':**
    - Upgrade Pillow to the latest version:
        ```sh
        pip install --upgrade pillow
        ```

- **PDFInfoNotInstalledError: Unable to get page count. Is poppler installed and in PATH?:**
    - Ensure that Poppler is installed and the path to its `bin` directory is added to your system PATH.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.
