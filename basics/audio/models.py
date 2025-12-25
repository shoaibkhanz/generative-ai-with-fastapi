import numpy as np
import torch
from transformers import AutoModel, AutoProcessor, BarkModel, BarkProcessor

from .schemas import VoicePresets

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_auto_model() -> tuple[BarkProcessor, BarkModel]:
    processor = AutoProcessor.from_pretrained(
        "suno/bark-small",
    )
    model = AutoModel.from_pretrained("suno/bark-small").to(device)
    return processor, model


def generate_audio(
    processor: BarkProcessor,
    model: BarkModel,
    prompt: str,
    preset: VoicePresets,
) -> tuple[np.array, int]:
    inputs = processor(text=[prompt], voice_preset=preset, return_tensors="pt")
    output = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    return output, sample_rate
