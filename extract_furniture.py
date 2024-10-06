import torch
import clip
from PIL import Image
import numpy as np
from segment_anything import sam_model_registry, SamPredictor
import cv2

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load SAM model
sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)

def get_clip_score(image, text):
    image_input = preprocess(image).unsqueeze(0).to(device)
    text_input = clip.tokenize([text]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_input)

    similarity = torch.nn.functional.cosine_similarity(image_features, text_features)
    return similarity.item()

def segment_and_shape_image(image_path, label):
    # Load image
    image = Image.open(image_path)
    image_np = np.array(image)

    # Prepare image for SAM
    predictor.set_image(image_np)

    # Generate multiple masks
    input_point = np.array([[image_np.shape[1] // 2, image_np.shape[0] // 2]])
    input_label = np.array([1])
    masks, scores, _ = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True
    )

    # Evaluate masks with CLIP
    best_score = -float('inf')
    best_mask = None
    for mask in masks:
        masked_image = image_np.copy()
        masked_image[~mask] = 0
        masked_pil = Image.fromarray(masked_image)
        score = get_clip_score(masked_pil, label)
        if score > best_score:
            best_score = score
            best_mask = mask

    # Create an image with transparent background
    rgba = cv2.cvtColor(image_np, cv2.COLOR_RGB2RGBA)
    
    # Make background transparent
    rgba[:, :, 3] = best_mask.astype(np.uint8) * 255

    # Find bounding box of the segmented object
    y_indices, x_indices = np.where(best_mask)
    x_min, x_max = x_indices.min(), x_indices.max()
    y_min, y_max = y_indices.min(), y_indices.max()

    # Crop the image to the bounding box
    shaped_image = rgba[y_min:y_max+1, x_min:x_max+1]

    # Save the shaped image
    output_image = Image.fromarray(shaped_image)
    output_path = f"{label}.png"
    output_image.save(output_path)

    print(f"Shaped image saved as {output_path}")

def extract(generate_path,label):

    segment_and_shape_image(generate_path,label)