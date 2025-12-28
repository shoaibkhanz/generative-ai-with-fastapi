# AGENTS.md - Development Guide for AI Coding Agents

## Project Overview

This is a Python 3.12+ project focused on Generative AI with FastAPI. The project uses `uv` for package management and follows a monorepo structure with workspace members.

**Key Technologies:**
- FastAPI for API development
- PyTorch & Transformers for ML models
- AWS Bedrock for cloud-based LLM access
- Pydantic for data validation and type safety
- Loguru for structured logging
- Async/await patterns for concurrency

**Project Structure:**
```
.
├── basics/              # Core examples and utilities
│   ├── audio/          # Text-to-speech models (Bark)
│   ├── text/           # Text generation (TinyLlama)
│   ├── concurrency/    # Async/sync examples
│   └── type_safety/    # Pydantic schemas and type utils
├── async_tutorial/     # Comprehensive async/sync tutorials
├── web_scraper/        # Workspace member for web scraping
└── test_*.py          # Standalone test scripts
```

## Package Management & Environment

**Package Manager:** `uv` (fast Python package installer and resolver)

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package-name>

# Run commands in the virtual environment
uv run python <script.py>
uv run fastapi dev <app_file.py>
```

## Build, Lint & Test Commands

### Running Tests

The project uses standalone test scripts rather than pytest framework:

```bash
# Run a single test file
uv run python test_bedrock.py
uv run python test_model_access.py
uv run python test_logprobs.py

# Run async tutorial tests
uv run python async_tutorial/test_tutorial.py

# Run all tutorial lessons
uv run python async_tutorial/run_all_lessons.py
```

### Running FastAPI Applications

```bash
# Run main text generation server
uv run fastapi dev basics/text/single_file_fastapi_app.py

# Run audio generation server
uv run fastapi dev basics/audio/main.py

# Run web scraper app
cd web_scraper
uv run fastapi dev main.py

# Production mode with uvicorn
uv run uvicorn basics.text.single_file_fastapi_app:app --reload
```

### Linting & Formatting

No explicit linting configuration found in the project. Recommend using:

```bash
# If adding linting tools
uv add --dev ruff black mypy
uv run ruff check .
uv run black .
uv run mypy .
```

## Code Style Guidelines

### Import Organization

Follow this order with blank lines between groups:

```python
# 1. Standard library imports
import asyncio
import os
from typing import Annotated, Literal

# 2. Third-party imports
import boto3
import torch
from fastapi import Body, Depends, FastAPI, Request
from loguru import logger
from pydantic import BaseModel, Field

# 3. Local application imports
from .dependencies import get_urls_content
from .models import generate_audio, load_auto_model
from .schemas import VoicePresets
```

### Type Hints & Annotations

**Always use type hints** for function parameters and return types:

```python
from typing import Annotated, Literal
from pydantic import Field

# Function signatures
def load_text_model() -> Pipeline:
    ...

def generate_text(pipe: Pipeline, prompt: str, temperature: float = 0.7) -> str:
    ...

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    ...

# Pydantic with Annotated
class TextModelRequest(BaseModel):
    prompt: Annotated[str, Field(min_length=0, max_length=10000)]
    temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.0)]
    model: Annotated[Literal["gpt-4o"], "Supported Models"]

# Type aliases
VoicePresets = Literal["v2/en_speaker_1", "v2/en_speaker_9"]
ImageSize = Annotated[tuple[int, int], "width and height of an image in pixels"]
```

### Naming Conventions

- **Functions/Variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **FastAPI Controllers:** Suffix with `_controller` (e.g., `chat_controller`, `serve_text_to_audio_model_controller`)
- **Async functions:** Use descriptive names; prefix not required (async keyword is sufficient)

### FastAPI Patterns

**Lifespan Context Managers:**

```python
from contextlib import asynccontextmanager

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
```

**Dependency Injection:**

```python
from fastapi import Body, Depends

async def get_urls_content(body: TextModelRequest = Body(...)) -> str:
    urls = extract_urls(body.prompt)
    if urls:
        return await fetch_all(urls)
    return ""

@app.post("/generate/text")
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),
) -> TextModelResponse:
    ...
```

**Response Models:**

```python
@app.post("/generate/text", response_model_exclude_defaults=True)
async def controller(...) -> TextModelResponse:
    ...

@app.get("/generate/audio", responses={status.HTTP_200_OK: {"content": {"audio/wav": {}}}})
def serve_audio(...):
    return StreamingResponse(audio_buffer, media_type="audio/wav")
```

### Error Handling & Logging

Use `loguru` for all logging:

```python
from loguru import logger

# Info logging
logger.info("loading model")
logger.info(f"Response: {response_text}")

# Warning logging
logger.warning("Could not parse the HTML content")
logger.warning(f"Failed to fetch some urls, Error {e}")

# Exception handling
try:
    urls_content = await fetch_all(urls)
    return urls_content
except Exception as e:
    logger.warning(f"Failed to fetch some urls, Error {e}")
    return ""
```

### Async Patterns

**Always use async for I/O-bound operations:**

```python
# Async context managers
async with aiohttp.ClientSession() as session:
    results = await asyncio.gather(*tasks)

# Gathering multiple operations
async def fetch_all(urls: list[str]) -> str:
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls], 
            return_exceptions=True
        )
        return " ".join([r for r in results if isinstance(r, str)])

# Error handling in async
results = await asyncio.gather(*tasks, return_exceptions=True)
success_results = [result for result in results if isinstance(result, str)]
```

## AWS Bedrock Integration

When working with AWS Bedrock:

```python
import boto3

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",  # or us-west-2
)

# Available models (no access form required)
# - cohere.command-r-plus-v1:0
# - cohere.command-r-v1:0
# - amazon.nova-pro-v1:0
# - amazon.nova-lite-v1:0

# Claude models require Anthropic use case form in AWS Console
# - anthropic.claude-3-5-sonnet-20241022-v2:0

response = bedrock_client.converse(
    modelId=model_id,
    messages=[{"role": "user", "content": [{"text": prompt}]}],
    system=[{"text": "You are a helpful assistant"}],
    inferenceConfig={"maxTokens": 100, "temperature": 0.7},
)
```

## Model Loading Patterns

```python
import torch
from transformers import Pipeline, pipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_text_model() -> Pipeline:
    pipe = pipeline(
        task="text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        dtype=torch.bfloat16,
        device=device,
    )
    return pipe
```

## Common Pitfalls to Avoid

### 1. ⚠️ CRITICAL: Blocking the Event Loop in Async Handlers

**The Most Common Mistake in This Codebase:**

When you declare a FastAPI handler as `async def`, FastAPI trusts you to only perform non-blocking operations. If you call **synchronous, CPU-bound functions** (like PyTorch model inference) directly inside an `async def` handler **without proper handling**, you will **BLOCK THE ENTIRE EVENT LOOP** and prevent the server from processing other requests.

**❌ WRONG - This blocks the event loop (found in web_scraper/main.py):**

```python
@app.post("/generate/text")
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),  # ✅ This IS async
) -> TextModelResponse:
    prompt = body.prompt + " " + urls_content
    output = generate_text(models["text"], prompt, body.temperature)  # ❌ BLOCKS EVENT LOOP!
    # generate_text() calls PyTorch/Transformers pipeline synchronously
    return TextModelResponse(content=output, ip=request.client.host)
```

**Why this is wrong:**
- `get_urls_content()` is properly async (uses `aiohttp` and `await fetch_all()`)
- But `generate_text()` from `load_generate_tinyllama.py` is a **synchronous, CPU-bound** function
- Calling it directly in an `async def` handler **blocks the event loop** for seconds/minutes
- Other requests cannot be processed until the blocking operation finishes

**✅ SOLUTION 1: Use `run_in_executor` for CPU-bound operations:**

```python
import asyncio

@app.post("/generate/text")
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),
) -> TextModelResponse:
    prompt = body.prompt + " " + urls_content
    
    # ✅ Run blocking CPU-bound code in thread pool
    loop = asyncio.get_event_loop()
    output = await loop.run_in_executor(
        None,  # Use default ThreadPoolExecutor
        generate_text,
        models["text"],
        prompt,
        body.temperature
    )
    
    return TextModelResponse(content=output, ip=request.client.host)
```

**✅ SOLUTION 2: Externalize model serving (Recommended):**

Convert the blocking function to async by externalizing to a dedicated model server (like vLLM):

```python
# models.py - Convert to async by making HTTP calls
import aiohttp

async def generate_text(prompt: str, temperature: float = 0.7) -> str:
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "http://localhost:8000/v1/chat",
            json={"temperature": temperature, "messages": [...]},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        predictions = await response.json()
        return predictions["choices"][0]["message"]["content"]

# main.py - Now properly async
@app.post("/generate/text")
async def serve_text_to_text_controller(...) -> TextModelResponse:
    output = await generate_text(body.prompt, body.temperature)  # ✅ Now awaited!
    return TextModelResponse(content=output, ip=request.client.host)
```

**✅ SOLUTION 3: Use `def` instead of `async def` for sync handlers:**

If you can't make the operation async, declare the handler as `def` (not `async def`). FastAPI will run it in the thread pool automatically:

```python
@app.post("/generate/text")  # Note: def, not async def
def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),  # Still works with async dependencies
) -> TextModelResponse:
    prompt = body.prompt + " " + urls_content
    output = generate_text(models["text"], prompt, body.temperature)  # ✅ FastAPI handles it
    return TextModelResponse(content=output, ip=request.client.host)
```

**Book Chapter Context:**
- Chapter 5 teaches async I/O (web scraping, RAG) correctly
- But Examples 5-7 through 5-14 demonstrate this anti-pattern
- The book fixes it later with vLLM (Example 5-16)
- The intermediate `run_in_executor` pattern is shown in `async_tutorial/` but not applied to the web scraper

**Reference:** See `async_tutorial/04_threading_vs_async.py` lines 331-340 and `BONUS_fastapi_async.py` for correct `run_in_executor` usage.

### 2. Don't mix sync/async incorrectly

Use `await` for coroutines, not `asyncio.run()` inside async functions

### 3. Always await coroutines

Forgot `await` means the operation won't execute

### 4. Use Pydantic for validation

Don't manually validate request data

### 5. Type hints are mandatory

All new code must include type hints

### 6. Log, don't print

Use `logger.info()` instead of `print()` in production code

### 7. Close resources

Use context managers (`with`, `async with`) for cleanup

### 8. Handle exceptions gracefully

Don't let exceptions crash the server silently

## Quick Reference

```bash
# Setup
uv sync

# Run FastAPI app
uv run fastapi dev basics/text/single_file_fastapi_app.py

# Run tests
uv run python test_bedrock.py

# Run tutorial
uv run python async_tutorial/01_sync_basics.py
```
