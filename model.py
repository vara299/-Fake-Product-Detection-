# Simple heuristic "model" for demo purposes.
# It loads an image, computes average brightness and uses filename heuristics.
from PIL import Image, ImageStat
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def compute_brightness(image_path):
    with Image.open(image_path).convert('L') as im:
        stat = ImageStat.Stat(im)
        return stat.mean[0]  # average pixel brightness 0..255

def predict_image(image_path):
    '''
    Returns a dictionary:
    {
        "label": "Fake" or "Genuine",
        "confidence": float (0..1),
        "reason": str
    }
    Heuristic:
     - If filename contains "fake" or "counterfeit" -> mark Fake (high confidence)
     - Else if brightness < 40 or > 220 -> suspicious -> Fake (medium confidence)
     - Else Genuine (confidence based on brightness distance)
    '''
    filename = os.path.basename(image_path).lower()
    brightness = compute_brightness(image_path)
    reason = []
    # filename heuristic
    if any(tok in filename for tok in ('fake', 'counterfeit', 'replica')):
        reason.append('filename indicates fake')
        return {"label": "Fake", "confidence": 0.92, "reason": ', '.join(reason)}
    # brightness heuristic
    if brightness < 40 or brightness > 220:
        reason.append(f'brightness={brightness:.1f} out of normal range')
        return {"label": "Fake", "confidence": 0.75, "reason": ', '.join(reason)}
    # Otherwise genuine with confidence scaled
    # confidence = 1 - normalized distance from center brightness 128
    conf = 1.0 - (abs(brightness - 128) / 128.0) * 0.6  # scaled to (0.4,1.0)
    conf = max(0.4, min(0.99, conf))
    reason.append(f'brightness={brightness:.1f} within normal range')
    return {"label": "Genuine", "confidence": round(conf, 2), "reason": ', '.join(reason)}
