from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os
import cv2
import numpy as np
'''
src: https://wistoriaswandandsword.com/ 
Thank you so muchhhhh
'''
class CrawlerWistoria:
    def __init__(self, chapter, path_to_save=None, is_new_folder=True):
        self.url = f"https://wistoriaswandandsword.com/manga/wistorias-wand-and-sword-chapter-{chapter}/"
        if path_to_save is None:
            self.path_to_save = os.path.join('..', 'data', 'wistoria', f'{chapter}')
        else:
            self.path_to_save = path_to_save
            if is_new_folder:
                self.path_to_save = os.path.join(path_to_save, f'{chapter}')

    def crawl(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            containers = soup.find(id="content").find_all(class_='separator')

            images_url = self._extract_image_urls(containers)
            
            os.makedirs(self.path_to_save, exist_ok=True)

            for i, url in enumerate(images_url):

                save_path_png = os.path.join(self.path_to_save, f'{i}.png')
                self._save_image(url, save_path_png)

        except Exception as e:
            print(f"Error crawling {self.url}: {e}")

    def _extract_image_urls(self, containers):
        images_url = []
        for container in containers:
            img_tag = container.find('img')
            if img_tag and img_tag.get('data-lazy-src'):
                images_url.append(img_tag.get('data-lazy-src'))
            elif img_tag:
                noscript_tag = container.find('noscript')
                if noscript_tag:
                    noscript_img = noscript_tag.find('img')
                    if noscript_img and noscript_img.get('src'):
                        images_url.append(noscript_img.get('src'))
        return images_url

    def _save_image(self, img_url, path):
        try:
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) 
            cv2.imwrite(path, img_cv)
        except Exception as e:
            print(f"Error saving image from {img_url}: {e}")
