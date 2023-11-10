from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import logging
from eng_thai_romanized import NameMatcher, MatchingMode
from qr_decoder import QRDecoder

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
matcher = NameMatcher(confidence=50, mode=MatchingMode.LEVENSHTEIN)

@app.post("/name-checker/")
async def check_romanized(name1: str = Form(...), name2: str=Form(...)):
    """
    If the same language check confidence only such as THAI-THAI, ENG-ENG
    """
    try:
        logger.info("Receiving name checking payload")
        result = matcher.compare_names(name1, name2)
        return result
    except Exception as e:
        logger.error(f"Error in name checking: {str(e)}")
        return JSONResponse(content={"detail": str(e)}, status_code=500)

@app.post("/decode-qr/")
async def decode_qr(file: UploadFile = UploadFile(...)):
    try:
        # Read the image from the received file
        logger.info("Receiving QR code decoding payload")
        image_contents = await file.read()
        decoded_value = QRDecoder.decode(image_contents)

        if decoded_value is None:
            logger.error("Failed to decode QR code or no QR code found.")
            raise HTTPException(status_code=400, detail="No QR code found or error in decoding.")
        
        return {"decoded_value": decoded_value}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in QR code decoding: {str(e)}")
        return {"detail": str(e)}, 500