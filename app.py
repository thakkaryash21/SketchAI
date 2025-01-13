# from flask import Flask, request, jsonify
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from PIL import Image
# import torch

# # Initialize Flask app
# app = Flask(__name__)

# # Load BLIP model and processor
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# @app.route("/caption", methods=["POST"])
# def generate_caption():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image provided"}), 400
    
#     image_file = request.files['image']
#     image = Image.open(image_file).convert("RGB")
    
#     # Process the image
#     inputs = processor(images=image, return_tensors="pt")
#     pixel_values = inputs["pixel_values"]
    
#     # Generate caption
#     generated_ids = model.generate(pixel_values)
#     caption = processor.decode(generated_ids[0], skip_special_tokens=True)
    
#     return jsonify({"caption": caption})

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=5090)

from flask import Flask, request, jsonify
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Initialize Flask app
app = Flask(__name__)

# Load BLIP model and processor inside the 'main' guard
if __name__ == '__main__':
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    @app.route("/caption", methods=["POST"])
    def generate_caption():
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        image = Image.open(image_file).convert("RGB")
        
        # Process the image
        inputs = processor(images=image, return_tensors="pt")
        pixel_values = inputs["pixel_values"]
        
        # Generate caption
        generated_ids = model.generate(pixel_values)
        caption = processor.decode(generated_ids[0], skip_special_tokens=True)
        
        return jsonify({"caption": caption})

    app.run(debug=True, host="0.0.0.0", port=5100)