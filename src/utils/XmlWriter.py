import xml.etree.cElementTree as ET
from typing import Tuple

from src.core import TOMLConfig


def get_object_name(class_name):
    if class_name == "Dried cranberries":
        return "蔓越莓果乾"
    elif class_name == "Edamames":
        return "毛豆"
    elif class_name == "almond sliver":
        return "杏仁條"
    elif class_name == "black soybeans":
        return "黑豆"
    elif class_name == "cashew":
        return "腰果"
    elif class_name == "dried clove fishes":
        return "小魚乾"
    elif class_name == "walnuts":
        return "核桃"
    elif class_name == "wolfberry":
        return "枸杞"


def generate_xml(results, class_names, resolution: Tuple[int, int], filename):
    width, height = resolution
    sorted = False
    annotations = ET.Element("annotations")
    ET.SubElement(annotations, "folder")
    ET.SubElement(annotations, "filename").text = filename
    ET.SubElement(annotations, "path").text = filename

    source = ET.SubElement(annotations, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(annotations, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"

    for result in results:
        for box in result.boxes:
            bbox = box.xyxy.tolist()[0]
            score = round(float(box.conf) * 100)
            name = get_object_name(class_names[int(box.cls)])
            # print(f"{class_names[int(box.cls)]} {name}: {score}% ({bbox})")
            if (
                not name
                or score < TOMLConfig.instance.env["yolo"]["confidence_threshold"]
            ):
                continue

            sorted = True

            obj = ET.SubElement(annotations, "object")
            ET.SubElement(obj, "name").text = name
            ET.SubElement(obj, "pose").text = "Unspecified"
            ET.SubElement(obj, "truncated").text = "0"
            ET.SubElement(obj, "difficult").text = "0"
            bndbox = ET.SubElement(obj, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(int(bbox[0]))
            ET.SubElement(bndbox, "ymin").text = str(int(bbox[1]))
            ET.SubElement(bndbox, "xmax").text = str(int(bbox[2]))
            ET.SubElement(bndbox, "ymax").text = str(int(bbox[3]))

    return ET.ElementTree(annotations), sorted


def write_xml(tree, output_path: str):
    tree.write(output_path, encoding="utf-8")
    return sorted
