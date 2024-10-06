from extract_furniture import extract
from SD import generate
from edit_image import pic_editing

import os
from html2image import Html2Image
import cv2  
import numpy as np
from PIL import Image


layout = {
    "bed": {
        "label": "single bed",
        "width": 180,
        "height": 80,
        "position": {"x": 20, "y": 20},
        "description": "rectangular-shaped single bed at the center"
    },
    "table": {
        "label": "white desk",
        "width": 100,
        "height": 100,
        "position": {"x": 150, "y": 200},
        "description": "white desk"
    },
    "chair1": {
        "label": "red chair",
        "width": 40,
        "height": 40,
        "position": {"x": 130, "y": 160},
        "description": "red chair"
    },
    "chair2": {
        "label": "red chair",
        "width": 40,
        "height": 40,
        "position": {"x": 230, "y": 160},
        "description": "red chair"
    },
    "chair3": {
        "label": "red chair",
        "width": 40,
        "height": 40,
        "position": {"x": 130, "y": 310},
        "description": "red chair"
    },
    "chair4": {
        "label": "red chair",
        "width": 40,
        "height": 40,
        "position": {"x": 230, "y": 310},
        "description": "red chair"
    }
}

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .room {
            width: 400px;
            height: 400px;
            border: 2px solid #333;
            position: relative;
            margin: 0 auto;
            background-color: #f0f0f0;
        }
        .bed {
            width: 180px;
            height: 80px;
            background-color: #d1c4e9;
            position: absolute;
            top: 20px;
            left: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 2px solid #666;
            writing-mode: vertical-rl;
            text-orientation: upright;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        .table {
            width: 100px;
            height: 100px;
            background-color: #ffcc80;
            position: absolute;
            top: 200px;
            left: 150px;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 2px solid #666;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        .chair {
            width: 40px;
            height: 40px;
            background-color: #a5d6a7;
            position: absolute;
            border: 2px solid #666;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        .chair1 { top: 160px; left: 130px; }
        .chair2 { top: 160px; left: 230px; }
        .chair3 { top: 310px; left: 130px; }
        .chair4 { top: 310px; left: 230px; }
    </style>
</head>
<body>
    <div class="room">
        <div class="bed">Bed</div>
        <div class="table">Table</div>
        <div class="chair chair1">Chair</div>
        <div class="chair chair2">Chair</div>
        <div class="chair chair3">Chair</div>
        <div class="chair chair4">Chair</div>
    </div>
</body>
</html>
"""

def html2image():
    if os.path.exists('home.html'):
        os.remove('home.html')
    with open ('room.html','w') as f:
         f.write(html_content)

    hti = Html2Image()
    hti.screenshot(
    html_file='room.html',
    save_as='room.png'
)

#create folder for image processing

if os.path.isdir('images')==False: 
    os.makedirs('images')
os.chdir('images')


#generate furnitures seperately through SD

for furniture in layout.keys():
    label=layout[furniture]["label"]
    text_prompt="a top view of one single"+layout[furniture]["description"]+"without any other things"
    generate_path=generate(text_prompt,label)
    extract(generate_path,label)


#create a white background 

if os.path.exists('white.png')==False: 

    array_created = np.full((400, 400, 3),  255, dtype = np.uint8)  
    output_image = Image.fromarray(array_created)
    output_image.save('white.png')

#pic editing

for furniture in layout.keys():
    label=layout[furniture]["label"]
    width, height=layout[furniture]["width"], layout[furniture]["height"]
    ab_width, ab_height=layout[furniture]["position"]["x"], layout[furniture]["position"]["y"]
    home_image_path='white.png'
    fur_image_path= label+'.png'
    pic_editing(home_image_path,fur_image_path, width, height, ab_width, ab_height)



#text_prompt="top view of rectangular-shpaed single bed at the center without any other things inside the environment"
#label='single bed'
#generate_path=generate(text_prompt,label)
#extract(generate_path,label)


