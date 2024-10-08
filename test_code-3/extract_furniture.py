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
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)

    # Prepare image for SAM
    predictor.set_image(image_np)

    # Generate multiple masks with different input points
    masks = []
    scores = []
    input_points = [
        np.array([[image_np.shape[1] // 2, image_np.shape[0] // 2]]),  # Center
        np.array([[image_np.shape[1] // 4, image_np.shape[0] // 4]]),  # Top-left
        np.array([[3 * image_np.shape[1] // 4, image_np.shape[0] // 4]]),  # Top-right
        np.array([[image_np.shape[1] // 4, 3 * image_np.shape[0] // 4]]),  # Bottom-left
        np.array([[3 * image_np.shape[1] // 4, 3 * image_np.shape[0] // 4]])  # Bottom-right
    ]

    for input_point in input_points:
        mask, score, _ = predictor.predict(
            point_coords=input_point,
            point_labels=np.array([1]),
            multimask_output=True
        )
        masks.extend(mask)
        scores.extend(score)

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

    # Add padding to the bounding box
    padding = 10
    x_min = max(0, x_min - padding)
    y_min = max(0, y_min - padding)
    x_max = min(rgba.shape[1], x_max + padding)
    y_max = min(rgba.shape[0], y_max + padding)

    # Crop the image to the bounding box
    shaped_image = rgba[y_min:y_max+1, x_min:x_max+1]

    # Save the shaped image
    output_image = Image.fromarray(shaped_image)
    output_path = f"{label}.png"
    output_image.save(output_path)

    print(f"Shaped image saved as {output_path}")
    #return best_score

def extract(generate_path, label):
    #score = segment_and_shape_image(generate_path, label)
    segment_and_shape_image(generate_path, label)
    #print(f"Extraction confidence: {score:.4f}")
    #return score
