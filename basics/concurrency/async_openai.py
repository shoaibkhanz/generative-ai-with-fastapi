import os

from fastapi import Body, FastAPI
from openai import AsyncOpenAI, OpenAI

app = FastAPI()

sync_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
async_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.post("/sync")
def sync_generate_text(prompt: str = Body(...)):
    completion = sync_client.responses.create(
        model="gpt-4o", input=[{"role": "user", "content": prompt}]
    )
    return completion.output[0].content[0].text


@app.post("/async")
async def async_generate_text(prompt: str = Body(...)):
    completion = await async_client.responses.create(
        model="gpt-4o", input=[{"role": "user", "content": prompt}]
    )
    return completion.output[0].content[0].text
