import torch
import numpy as np
from PIL import Image
import open_clip

# Load model once
model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-B-32',
    pretrained='openai'
)

tokenizer = open_clip.get_tokenizer('ViT-B-32')


def encode_image(img):
    """
    Accepts either:
    - PIL.Image.Image
    - numpy.ndarray (H, W, 3)

    Converts to PIL → preprocess → encodes using CLIP.
    """

    # If image is numpy array → convert to PIL
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img.astype("uint8"))

    # Preprocess for CLIP
    img_tensor = preprocess(img).unsqueeze(0)

    # Encode using CLIP
    with torch.no_grad():
        image_features = model.encode_image(img_tensor)

    # Normalize vector
    image_features /= image_features.norm(dim=-1, keepdim=True)

    return image_features.cpu().numpy()[0]
