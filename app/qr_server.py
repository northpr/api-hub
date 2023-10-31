from fastapi import FastAPI, UploadFile, HTTPException, Form
import cv2
import numpy as np
import logging
from eng_thai_romanized import NameMatcher

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
matcher = NameMatcher(confidence=50)

@app.post("/name-checker/")
async def check_romanized(to_check_name: str = Form(...), true_name: str=Form(...)):
    """
    If the same language check confidence only such as THAI-THAI, ENG-ENG
    """
    try:
        print("Receiving payload")
        result = matcher.compare_names(to_check_name, true_name)
        print(result)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decode-qr/")
async def decode_qr(file: UploadFile = UploadFile(...)):
    try:
        # Read the image from the received file
        image_contents = await file.read()
        image = np.frombuffer(image_contents, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # If image decoding fails, it's not a image
        if image is None:
            logger.error("Failed to decoded the image.")
            raise HTTPException(status_code=400, detail="Invalid file format. Ensure you're sending a valid JPEG or PNG")

        # Decode the QR code using OpenCV
        qr_code_detector = cv2.QRCodeDetector()
        retval, decoded_info, _ = qr_code_detector.detectAndDecode(image)

        if retval:
            return {"decoded_value": retval}
        else:
            logger.warning("No QR code found in the uploaded image.")
            raise HTTPException(status_code=400, detail="No QR code found or error in decoding.")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

