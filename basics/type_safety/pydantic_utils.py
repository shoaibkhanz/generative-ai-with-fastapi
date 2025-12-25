from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel

# We re define it below with encapsulating the code
# class TextModelRequest(BaseModel):
#     model: Annotated[Literal["gpt-4o"], "supported models"]
#     prompt: str
#     temperature: float = 0.0


class ModelRequest(BaseModel):
    prompt: str


class ModelResponse(BaseModel):
    request_id: str
    ip: str | None
    content: str | None
    created_at: datetime = datetime.now()


class TextModelRequest(ModelRequest):
    model: Annotated[Literal["gpt-4o"], "Supported Models"]
    temperature: float = 0.0


class TextModelResponse(ModelResponse):
    tokens: int


ImageSize = Annotated[tuple[int, int], "width and height of an image in pixels"]


class ImageModelRequest(ModelRequest):
    model: Literal["tinysd", "sd1.5"]
    output_size: ImageSize
    num_inference_steps: int = 200


class ImageModelResponse(ModelResponse):
    size: ImageSize
    url: str
