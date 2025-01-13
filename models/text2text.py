from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
import torch
from huggingface_hub import login
import gc
from dotenv import load_dotenv
import os

gc.collect()
torch.cuda.empty_cache()

load_dotenv()

token = os.getenv("HUGGING_FACE_TOKEN")

login(token=token)

model_name = "meta-llama/Llama-3.1-8B"
cache_dir = "./.cache"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quant_config,
    cache_dir=cache_dir,    
    device_map="auto"  # Automatically allocate layers across GPU/CPU
)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

blip_caption = "sketch drawing of chair"

prompt = f"""Describe a professional, high quality product image for a {blip_caption} on e commerce market places. The image is set against a clean background featuring a light gradient that transitions from white at the top to soft gray at the bottom, creating a neutral and sophisticated presentation. The lighting is soft but directional. The perspective is an isometric view, slightly elevated, to clearly display the details while ensuring a balanced and aesthetically pleasing composition.Generate a description of the scene as if you were creating a professional listing for a top-tier e-commerce platform. Description: """

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_length=500,
        do_sample=True,
        temperature=0.5,
        top_p=0.9,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )

enhanced_prompt = tokenizer.decode(outputs[0], skip_special_tokens=True)

enhanced_prompt = enhanced_prompt.split("Description: ")[1]

condensed_prompt = summarizer(enhanced_prompt, max_length=75, min_length=60, do_sample=False)

print("Result:\n\n", condensed_prompt[0]['summary_text'])