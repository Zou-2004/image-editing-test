from extract_furniture import extract
from SD import generate
from edit_image import pic_editing

import os
from html2image import Html2Image
import cv2  
import numpy as np
from PIL import Image

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--env','-e', type=str, help='choose environment', default='white')
parser.add_argument('--size', type=list, default=[400,400],help='size of env in pixel')
parser.add_argument('--text',type=str, default='top view of rectangular-shpaed single bed and four red chair surrounding a white desk', help='your description')
args=parser.parse_args()


#home 400*400 pixel
#give me a python dictionary of layout of a indoor scene, 
# by giving u the description of a text prompt, you should extract 
# the label, width, height, relative position, and description 
# of each furniture. The room is 400*400 pixel in size. 
# Make sure that you design did not over lap furniture ad the size of furnitures are in proportion. 
# the text is "top view of rectangular-shpaed single 
# bed and four red chair surrounding a white desk'

text_prompt='give me a python dictionary named layout of the layout of a indoor scene\
, by giving u the description of a text prompt, you should extract\
the label, width, height, relative position, and description. of each furniture.\
The room is ' + str(args.size[0])+'*'+str(args.size[1])+ ' in size,\
Make sure that your design did not overlap furnitures and the size of furnitures are in proportion to each other.\
The text is' + args.text

#example layout dictionary
layout = {
    "room_size": {"width": 400, "height": 400},
    "furniture": [
        {
            "label": "bed and pillow",
            "description": "single bed",
            "width": 120,
            "height": 70,
            "position": {"x": 40, "y": 40}
        },
        {
            "label": "desk",
            "description": "white empty desk",
            "width": 100,
            "height": 50,
            "position": {"x": 250, "y": 175}
        },
        {
            "label": "sofa",
            "description": "sofa",
            "width": 30,
            "height": 30,
            "position": {"x": 220, "y": 140}
        },
        {
            "label": "sofa",
            "description": "sofa",
            "width": 30,
            "height": 30,
            "position": {"x": 320, "y": 140}
        },
        {
            "label": "sofa",
            "description": "sofa",
            "width": 30,
            "height": 30,
            "position": {"x": 220, "y": 230}
        },
        {
            "label": "sofa",
            "description": "sofa",
            "width": 30,
            "height": 30,
            "position": {"x": 320, "y": 230}
        }
    ]
}
#create folder for image processing

if os.path.isdir('images')==False: 
    os.makedirs('images')
os.chdir('images')

#create a white background 
if args.env =='white' or args.e =='white':
    
    if os.path.exists('white.png')==False: 

        array_created = np.full((400, 400, 3),  255, dtype = np.uint8)  
        output_image = Image.fromarray(array_created)
        output_image.save('white.png')
    home_image_path='white.png' 
else: #customize image in images folder

    home_image_path=args.env
    # change to 400*400


#generate furnitures seperately through SD

for index in range(len(layout["furniture"])):
    
    label=layout["furniture"][index]["label"]
    text_prompt="a top view of one single"+layout["furniture"][index]["description"]+"without any other things"
    generate_path=generate(text_prompt,label)
    extract(generate_path,label)

    #pic editing

    width, height=layout["furniture"][index]["width"], layout["furniture"][index]["height"]
    ab_width, ab_height=layout["furniture"][index]["position"]["x"], layout["furniture"][index]["position"]["y"]
    fur_image_path= label+'.png'
    pic_editing(home_image_path,fur_image_path, width, height, ab_width, ab_height)



#text_prompt="top view of rectangular-shpaed single bed at the center without any other things inside the environment"
#label='single bed'
#generate_path=generate(text_prompt,label)
#extract(generate_path,label)


