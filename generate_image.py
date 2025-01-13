from flask import Flask, request, jsonify
import diffusers
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
import torch
import os

app = Flask(__name__)

# Set the environment variable for memory management
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

# Load Stable Diffusion XL base pipeline with efficient memory handling
pipeline = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", 
    torch_dtype=torch.float16, 
    variant="fp16", 
    use_safetensors=True
)
pipeline.to("cuda")

# Load Stable Diffusion XL refiner pipeline
refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    variant="fp16"
)
refiner.to("cuda")

# Clear CUDA cache to prevent memory issues
torch.cuda.empty_cache()

@app.route('/generate', methods=['POST'])
def generate_image():
    prompt = request.json.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    # Run inference with the pipeline
    image = pipeline(prompt, height=768, width=768).images[0]

    # Save the generated image to a file
    output_dir = "static/outputs"
    os.makedirs(output_dir, exist_ok=True)

    existing_files = os.listdir(output_dir)
    existing_numbers = [int(f.split('_')[-1].split('.')[0]) for f in existing_files if f.startswith("output_")]
    new_number = max(existing_numbers, default=0) + 1

    filename = os.path.join(output_dir, f"output_{new_number}.png")
    image.save(filename)

    return jsonify({'image_url': f"/static/outputs/output_{new_number}.png"})


if __name__ == '__main__':
    app.run(debug=True, port=5002)