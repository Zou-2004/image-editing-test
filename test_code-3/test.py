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

parser.add_argument('--env','-e', type=str, help='choose environment, provide pic path here if custom', default='white')
# only square and rectangular shaped env is supported now
parser.add_argument('--size', nargs=2, type=int, default=[1000,1000], help='size of env in pixels (width height)')
parser.add_argument('--text',type=str, default='top view of rectangular-shpaed single bed and four red chair surrounding a white desk', help='your description')
args=parser.parse_args()

#ask chatgpt4o
#home 400*400 pixel
#give me a python dictionary of layout of a indoor scene, 
# by giving u the description of a text prompt, you should extract 
# the label, width, height, relative position, and description 
# of each furniture. The room is 400*400 pixel in size. 
# Make sure that you design did not over lap furniture ad the size of furnitures are in proportion. 
# the text is "top view of rectangular-shpaed single 
# bed and four red chair surrounding a white desk'

text_prompt='give me a python dictionary(named layout, without any other text) of the layout of a indoor scene\
, by giving u the description of a text prompt, you should extract\
the label, width, height, relative position, and description. of each furniture.\
The room is ' + str(args.size[0])+'*'+str(args.size[1])+ ' in size,\
. You should have both room_size and furniture (take this as name) in the dictionary.\
Make sure that your design did not overlap furniture and the size of furniture are in proportion to each other.\
The text is' + args.text

#example layout dictionary
layout = {
    "room_size": {"width": 1000, "height": 1000},
    "furniture": [
        {
            "label": "bed",
            "description": "single bed",
            "width": 200,
            "height": 400,
            "position": {"x": 100, "y": 100}
        },
        {
            "label": "desk",
            "description": "desk",
            "width": 150,
            "height": 100,
            "position": {"x": 700, "y": 400}
        },
        {
            "label": "chair1",
            "description": "chair",
            "width": 50,
            "height": 50,
            "position": {"x": 650, "y": 350}
        },
        {
            "label": "chair2",
            "description": "chair",
            "width": 50,
            "height": 50,
            "position": {"x": 850, "y": 350}
        },
        {
            "label": "chair3",
            "description": "chair",
            "width": 50,
            "height": 50,
            "position": {"x": 650, "y": 500}
        },
        {
            "label": "chair4",
            "description": "chair",
            "width": 50,
            "height": 50,
            "position": {"x": 850, "y": 500}
        }
    ]
}
#create folder for image processing

if os.path.isdir('images')==False: 
    os.makedirs('images')
os.chdir('images')

#create a white background 
#defualt image_path= images/white.png

if args.env =='white':
    
    if os.path.exists('white.png')==False: 
        array_created = np.full((int(args.size[0]), int(args.size[1]), 3),  255, dtype = np.uint8)
        output_image = Image.fromarray(array_created)
        output_image.save('white.png')
        
    home_image_path='white.png'
    

else: #customize image in images folder and resize it

    image=Image.open(args.env)
    image.resize(int(args.size[0]), int(args.size[1]))
    if os.path.exists('custom.png'):
        print("custom.png founded, will be covered later")
    custom_image_path=image.save('custom.png')
    home_image_path= custom_image_path
    


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


