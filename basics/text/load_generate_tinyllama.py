import torch
from transformers import Pipeline, pipeline

sample_prompt = "How to setup fastapi project ?"
system_prompt = """
Your name is Fastapi bot and you are helpful chatbot 
responsible for teaching Fastapi to your users.
Always respond in markdown.
"""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_text_model():
    pipe = pipeline(
        task="text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        dtype=torch.bfloat16,
        device=device,
    )

    return pipe


def generate_text(pipe: Pipeline, prompt: str, temperature: float = 0.7) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    predictions = pipe(
        prompt,
        temperature=temperature,
        max_new_tokens=256,
        do_sample=True,
        top_k=50,
        top_p=0.95,
    )
    output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
    # output = predictions[0]["generated_text"]
    return output
