from diffusers import StableDiffusionXLPipeline
import torch

def generate(text_prompt, label):
    model_id = "stabilityai/stable-diffusion-xl-base-1.0"
    
    # Create the pipeline
    pipe = StableDiffusionXLPipeline.from_pretrained(
        model_id, 
        torch_dtype=torch.float16, 
        use_safetensors=True, 
        variant="fp16"
    )
    
    # Enable optimizations
    pipe.enable_sequential_cpu_offload()
    pipe.enable_attention_slicing()
    
    # Generate the image
    generator = torch.Generator("cuda").manual_seed(0)
    image = pipe(text_prompt, generator=generator).images[0]
    
    # Save the image
    save_image_path = label + '.png'
    image.save(label+"1.png")
    image.save(save_image_path, format="PNG")
    
    return save_image_path



