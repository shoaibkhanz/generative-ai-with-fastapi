from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress, PositiveInt

# We re define it below with encapsulating the code
# class TextModelRequest(BaseModel):
#     model: Annotated[Literal["gpt-4o"], "supported models"]
#     prompt: str
#     temperature: float = 0.0


class ModelRequest(BaseModel):
    prompt: Annotated[str, Field(min_legnth=0, max_length=10000)]


class ModelResponse(BaseModel):
    request_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    ip: Annotated[str, IPvAnyAddress]
    content: Annotated[str, Field(min_length=0, max_length=10000)]
    created_at: datetime = datetime.now()


class TextModelRequest(ModelRequest):
    model: Annotated[Literal["gpt-4o"], "Supported Models"]
    temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.0)]


class TextModelResponse(ModelResponse):
    tokens: Annotated[int, PositiveInt]


ImageSize = Annotated[tuple[int, int], "width and height of an image in pixels"]


class ImageModelRequest(ModelRequest):
    model: Literal["tinysd", "sd1.5"]
    output_size: ImageSize
    num_inference_steps: int = 200


class ImageModelResponse(ModelResponse):
    size: ImageSize
    url: str
