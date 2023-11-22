import numpy as np
from ultralytics import YOLO

from . import TOMLConfig


class YOLOv8:
    instance = None

    def __init__(self, model_path: str):
        """
        :param model_path: 模型檔案路徑
        """
        self.instance = self

        self.yolo_env = TOMLConfig.instance.env["yolo"]
        self.model = YOLO(model_path)

    def detect_objects(self, img: np.ndarray):
        """
        預測圖片中的物件
        :param img: 圖片
        """

        return self.model.predict(
            img,
            agnostic_nms=True,
            conf=self.yolo_env["confidence_threshold"],
        )
