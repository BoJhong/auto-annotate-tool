import os
import xml.etree.ElementTree as ET

import cv2

from src.core import TOMLConfig
from src.utils.XmlWriter import write_xml

directory = os.fsencode('fix_xml')

for file in os.listdir(directory):

    filename = os.fsdecode(file)
    if not filename.endswith('.xml'):
        continue

    path = f"fix_xml/{filename}"
    print(path)
    tree = ET.parse(path)
    root = tree.getroot()

    img = cv2.imread(f"fix_xml/{filename.split('.')[0]}.jpg")
    height, width, depth = img.shape

    root.find('folder').text = ""
    root.find('filename').text = f"{filename.split('.')[0]}.jpg"
    root.find('path').text = f"{filename.split('.')[0]}.jpg"

    size = root.find('size')
    size.find('width').text = str(height)
    size.find('height').text = str(width)
    size.find('depth').text = str(depth)

    write_xml(tree, path)
