from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
import torch
import os
import gc

gc.collect()
torch.cuda.empty_cache()

# Set the environment variable for memory management
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

# Load Stable Diffusion XL base pipeline with efficient memory handling
pipeline = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", 
    torch_dtype=torch.float16, 
    variant="fp16", 
    use_safetensors=True
)

# Move pipeline directly to GPU
pipeline.to("cuda")

# Clear CUDA cache to prevent memory issues
torch.cuda.empty_cache()

# Load Stable Diffusion XL refiner pipeline
refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    variant="fp16"
)

# Move refiner to GPU
refiner.to("cuda")

# Clear CUDA cache again
torch.cuda.empty_cache()

# Example of running inference with the pipeline
prompt ="The chair features a sturdy frame and a comfortable seat cushion, providing excellent support for the user. The chair is available in multiple colors, allowing users to choose the one that best fits their interior design. It is a symbol of sophistication and elegance, adding a touch of luxury to any setting."
image = pipeline(prompt, height=768, width=768).images[0]

# Create the directory if it doesn't exist
output_dir = "./outputs"
os.makedirs(output_dir, exist_ok=True)

# Get the list of existing files and find the highest number
existing_files = os.listdir(output_dir)
existing_numbers = [int(f.split('_')[-1].split('.')[0]) for f in existing_files if f.startswith("output_")]
new_number = max(existing_numbers, default=0) + 1

# Generate the new filename using the next available number
filename = os.path.join(output_dir, f"output_{new_number}.png")

# Save the generated image with the new unique filename
image.save(filename)

# Save the generated image with the new unique filename
image.save(filename)
# Clear memory after inference to ensure GPU is free for other tasks
torch.cuda.empty_cache()
