import cv2
from PIL import ImageFont
import re
import wordninja

def display(image, display_ratio = 1, time_s = 0):
    display_image = image
    if display_ratio != 1:
        w, h = int(image.shape[1] * display_ratio),  int(image.shape[0] * display_ratio)
        display_image = cv2.resize(image, (w, h))
    cv2.imshow('Image', display_image)
    cv2.waitKey(time_s*1000)
    cv2.destroyAllWindows()

def apply_corrections(text):
    corrections = {
        '|': 'I',
        '/': 'I',
        '1': 'I',
        '@': 'a',
        '#': 'o',
        '$': 's',
        '5': 's',
        '0': 'o',
        '3': 'e',
        '6': 'g',
        '1o': 'to',
        '- ': '',
        ' - ':''
    }
    for key, value in corrections.items():
        text = text.replace(key, value)
    return text

def process_text(text):
    sentences = re.split(r'([!?.,])', text)
    processed_sentences = []
    for i in range(0, len(sentences), 2):
        sentence = sentences[i].strip()
        if sentence:
            separated_words = wordninja.split(sentence)
            processed_sentence = " ".join(separated_words)
            if i + 1 < len(sentences):
                processed_sentence += sentences[i + 1]
            processed_sentences.append(processed_sentence)    
    return "".join(processed_sentences)

def calculate_text_dimensions(text, font):
    lines = text.split('\n')
    max_width = 0
    total_height = 0
    for line in lines:
        bbox = font.getbbox(line)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        max_width = max(max_width, width)
        total_height += height
    return max_width, total_height

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        bbox = font.getbbox(word)
        word_width = bbox[2] - bbox[0]
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + (font.getbbox(' ')[2] - font.getbbox(' ')[0])
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width

    if current_line:
        lines.append(' '.join(current_line))
    return lines

def find_optimal_font_size(bbox, text, font_path, max_font_size=60, min_font_size=6):
    x1, y1, x2, y2 = bbox
    bbox_width = x2 - x1
    bbox_height = y2 - y1

    for font_size in range(max_font_size, min_font_size - 1, -1):
        font = ImageFont.truetype(font_path, font_size)
        wrapped_text = wrap_text(text, font, bbox_width)
        text_width, text_height = calculate_text_dimensions('\n'.join(wrapped_text), font)

        if text_width <= bbox_width and text_height <= bbox_height:
            return font_size

    return min_font_size