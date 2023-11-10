import cv2
import numpy as np
from typing import Optional

class QRDecoder:
    @staticmethod
    def decode(image_contents: bytes) -> Optional[str]:
        image = np.frombuffer(image_contents, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # If image decoding fails, it's not an image.
        if image is None:
            return None
        
        qr_code_detector = cv2.QRCodeDetector()
        retval, decoded_info, _ = qr_code_detector.detectAndDecode(image)
        print(retval)

        if not retval:
            return None
        return retval