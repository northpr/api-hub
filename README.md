\
# FastAPI QR Code Decoder
A simple FastAPI application that decodes QR codes from uploaded images, romanized test

## Requirements
- Python 3.7+
- FastAPI
- Uvicorn
- OpenCV
- NumPy
- PyThaiNLP
- Lingua-py

## Running the Application
```univorn main:app --reload```

The application will be `most` available at `http://127.0.0.1:8000`


## Usage
Decode QR Code from an Image

- Endpoint: /decode-qr/
- Method: POST
- Payload: A form with a field named file containing the image file.
- Response: JSON containing the decoded value of the QR code.

Name Checker

- Endpoint: /name-checker/
- Method: POST