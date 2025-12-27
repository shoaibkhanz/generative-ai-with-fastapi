from contextlib import asynccontextmanager

from basics.text.load_generate_tinyllama import generate_text, load_text_model
from basics.type_safety.pydantic_utils import TextModelRequest, TextModelResponse
from fastapi import Body, Depends, FastAPI, Request
from loguru import logger

from .dependencies import get_urls_content

models = {}


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("loading model")
    models["text"] = load_text_model()
    logger.info("model loaded successfully")

    yield

    logger.info("clearing model")
    models.clear()


app = FastAPI(lifespan=lifespan)


@app.post("/generate/text", response_model_exclude_defaults=True)
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),
) -> TextModelResponse:
    prompt = body.prompt + " " + urls_content
    output = generate_text(models["text"], prompt, body.temperature)
    tokens = len(output)
    return TextModelResponse(content=output, ip=request.client.host, tokens=tokens)
