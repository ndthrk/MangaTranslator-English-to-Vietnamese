from deep_translator import GoogleTranslator
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import wordninja
import re
import utlis

class TextTranslator:
    def __init__(self, font_path='font.ttf'):
        self.bboxes_cluster = None
        self.image = None
        self.font_path = font_path
        self.translator = GoogleTranslator(source='en', target='vi')

    def correction_text(self):
        for bbox in self.bboxes_cluster:
            text = utlis.apply_corrections(bbox[4]).lower()
            sentences = re.split(r'([!?.,])', text)
            processed_sentences = [
                " ".join(wordninja.split(sentences[i].strip())) + (sentences[i + 1] if i + 1 < len(sentences) else '')
                for i in range(0, len(sentences), 2)
            ]
            final_text = " ".join(processed_sentences)
            # print(text, final_text, sep='\n-')
            bbox[4] = final_text
    def translation(self, text):
        trans_text = self.translator.translate(text=text)
        return trans_text

    def fit_text_to_bbox(self, image, font_path):
        result_image = image.copy()
        image_pil = Image.fromarray(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)
            
        for bbox in self.bboxes_cluster:
            x1, y1, x2, y2, src_text = bbox
            trans_text = self.translation(src_text)
            
            padding = 5
            x1, y1, x2, y2 = x1 + padding, y1 + padding, x2 - padding, y2 - padding

            bbox_width = int(x2 - x1)
            bbox_height = int(y2 - y1)

            optimal_font_size = utlis.find_optimal_font_size([x1, y1, x2, y2], trans_text, font_path)
            font = ImageFont.truetype(font_path, optimal_font_size)
            lines = utlis.wrap_text(trans_text, font, bbox_width)
            text_width, text_height = utlis.calculate_text_dimensions('\n'.join(lines), font)

            x0 = x1 + (bbox_width - text_width) // 2
            y0 = y1 + (bbox_height - text_height) // 2

            draw.rectangle([x1-padding, y1-padding, x2+padding, y2+padding], fill=(255, 255, 255), outline=None)

            for line in lines:
                draw.text((x0, y0), line, font=font, fill=(0, 0, 0))
                y0 += font.getbbox(line)[3] - font.getbbox(line)[1] + 2

        result_image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        return result_image

    def add_text_trans_to_image(self, bboxes, image):
        self.bboxes_cluster = bboxes
        self.image = image
        return self.process()

    def process(self):
        # src_text = self.get_text().lower()
        self.correction_text()
        image_with_text = self.fit_text_to_bbox(self.image, self.font_path)
        return image_with_text

