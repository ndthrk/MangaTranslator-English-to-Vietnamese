from MangaTrans import MangaTranslator
import cv2
import os
from utlis import display

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_dir = os.path.join(project_dir, "data", "wistoria")
output_dir = os.path.join(project_dir, "data", "output", "wistoria")


img_path = os.path.join(input_dir, "42","41.png")
image = cv2.imread("test.png")
font_path = 'font.ttf'
trans = MangaTranslator(scale_width=1.3, font_path = font_path)
rs = trans.get_result(image)
display(rs, 0.4)

# detection = TextDetector(1.35)
# translator = TextTranslator()

# def get_result(img_path):
#     image = cv2.imread(img_path)
#     if image is None:
#         raise ValueError("Failed to load image")
#     bboxes_cluster = detection.detect_text_from_image(image)
#     if not bboxes_cluster:
#         return image
#     image_with_text = translator.add_text_trans_to_image(bboxes_cluster, image)
#     return image_with_text

# display(get_result(img_path=img_path), 0.6)

# for chapter in os.listdir(input_dir):
#     chapter_input_path = os.path.join(input_dir, chapter)
#     chapter_output_path = os.path.join(output_dir, chapter)
#     print(f"Translating chapter {chapter}")
#     if not os.path.exists(chapter_output_path):
#         os.makedirs(chapter_output_path)
    
#     for image_file in os.listdir(chapter_input_path):
#         if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
#             img_path = os.path.join(chapter_input_path, image_file)
#             output_path = os.path.join(chapter_output_path, image_file)

#             rs = trans.get_result(cv2.imread(img_path))
            
#             cv2.imwrite(output_path, rs)

