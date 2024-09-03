from detect import TextDetector
from translator import TextTranslator
import cv2
class MangaTranslator:
    min_H = 1200
    def __init__(self,scale_width: float = 1.4, font_path: str = "font.ttf"):
        self.text_detector = TextDetector(scale_width)
        self.text_translator = TextTranslator(font_path)

    def get_result(self, image):
        h, w = image.shape[:2]
        print(h, w)
        if h < self.min_H:
            scale = max(self.min_H / h, 1)
            new_w, new_h = int(w * scale), int(h * scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

        bboxes_cluster = self.text_detector.detect_text_from_image(image)
        if not bboxes_cluster:
            return image
        image_with_text = self.text_translator.add_text_trans_to_image(bboxes_cluster, image)
        return image_with_text