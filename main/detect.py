import numpy as np
import cv2
from paddleocr import PaddleOCR
from sklearn.cluster import DBSCAN

class TextDetector:
    def __init__(self, scale_width = 1.4):
        self.scale_width = scale_width
        self.model = PaddleOCR(use_angle_cls=True, lang='en')
        self.original_image = None
        self.processed_image = None
        self.ocr_results = None
        self.bounding_boxes = None

    def _preprocess_image(self):
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        height, width = gray_image.shape[:2]
        new_width = int(width * self.scale_width)
        return cv2.resize(gray_image, (new_width, height), interpolation=cv2.INTER_LINEAR)

    def _extract_coordinates(self):
        coordinates = {}
        for box, (text, _) in self.ocr_results[0]:
            box = np.array(box).astype(np.int32)
            box[:, 0] = box[:, 0] / self.scale_width
            top_left, bottom_right = box[0], box[2]
            center = tuple((top_left + bottom_right) // 2)
            coordinates[center] = [*top_left, *bottom_right, text]
        return coordinates

    def cluster_text(self, eps_width_percent = 8, min_samples = 1, 
                     min_points = 2, padding = 3):
        coordinates = self._extract_coordinates()
        points = np.array(list(coordinates.keys()))

        eps = int(self.original_image.shape[1] * (eps_width_percent / 100))
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        cluster_labels = dbscan.fit_predict(points)

        self.bounding_boxes = []
        for label in np.unique(cluster_labels):
            cluster_points = points[cluster_labels == label]
            if len(cluster_points) < min_points:
                continue
            
            bbox = self._compute_bounding_box(cluster_points, coordinates, padding)
            if bbox:
                self.bounding_boxes.append(bbox)

    def _compute_bounding_box(self, cluster_points, coordinates, padding):
        x1, y1 = np.inf, np.inf
        x2, y2 = -np.inf, -np.inf
        text = []

        for point in cluster_points:
            coord = coordinates[tuple(point)]
            x1 = min(x1, coord[0])
            y1 = min(y1, coord[1])
            x2 = max(x2, coord[2])
            y2 = max(y2, coord[3])
            text.append(coord[4])

        x1 = max(0, int(x1) - padding)
        y1 = max(0, int(y1) - padding)
        x2 = min(self.original_image.shape[1], int(x2) + padding)
        y2 = min(self.original_image.shape[0], int(y2) + padding)

        return [x1, y1, x2, y2, " ".join(text)]

    def get_ocr_results(self):
        return self.ocr_results

    def get_bounding_boxes(self):
        if self.bounding_boxes is None:
            self.cluster_text()
        return self.bounding_boxes

    def detect_text_from_image(self, image):
        self.original_image = image
        self.processed_image = self._preprocess_image()
        self.ocr_results = self.model.ocr(self.processed_image)
        self.bounding_boxes = None
        return self.get_bounding_boxes()
