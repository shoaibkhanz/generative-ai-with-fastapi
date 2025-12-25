import boto3
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

# Initialize FastAPI app
app = FastAPI(title="FastAPI with AWS Bedrock Claude")

# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",  # Change to your preferred region
)

# Set the model ID, e.g., Command R.
# model_id = "cohere.command-r-v1:0"  # logprobs available but blocked
model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"


# @app.get("/")
# def root_controller():
#     return {"status": "healthy"}
#


@app.get("/", include_in_schema=False)
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=HTTP_303_SEE_OTHER)


@app.get("/chat")
def chat_controller(prompt: str = "inspire me"):
    response = bedrock_client.converse(
        modelId=model_id,
        messages=[
            {"role": "user", "content": [{"text": "You are a helpful assistant"}]},
            {"role": "assistant", "content": [{"text": prompt}]},
        ],
        inferenceConfig={
            "maxTokens": 20,
            "temperature": 0,
        },
    )
    response_text = response["output"]["message"]["content"]
    return {"response": response_text}
