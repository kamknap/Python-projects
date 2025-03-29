# PDF Sign GUI

This project provides a graphical user interface (GUI) application for signing PDF documents. Users can select a PDF file, enter a signature, and apply the signature to the selected document.

## Project Structure

```
pdf-sign-gui
├── src
│   ├── main.py          # Entry point of the application
│   ├── gui
│   │   └── app.py      # GUI implementation
│   └── utils
│       └── pdf_signer.py # Logic for signing PDFs
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Requirements

To run this project, you need to install the following dependencies:

- PyPDF2
- reportlab

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies.
4. Run the application:

```
python src/main.py
```

5. In the GUI, click on the "Select File" button to choose a PDF file.
6. Enter your signature in the text field.
7. Click the "Sign" button to apply the signature to the selected PDF.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.