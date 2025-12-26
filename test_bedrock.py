#!/usr/bin/env python3
"""
Quick test script to verify AWS Bedrock access with Cohere Command R Plus
"""

import json

import boto3

print("Testing AWS Bedrock access...")
print("-" * 60)

# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

# Available models (no access form required):
model_id = "cohere.command-r-plus-v1:0"  # Cohere's most capable model
# model_id = "cohere.command-r-v1:0"  # Faster, more cost-effective Cohere model
# model_id = "amazon.nova-pro-v1:0"  # Amazon's high-capability model
# model_id = "amazon.nova-lite-v1:0"  # Amazon's fast, cost-effective model
# model_id = "amazon.nova-micro-v1:0"  # Amazon's ultra-fast, minimal cost model

# Claude models (requires Anthropic use case form in AWS Console):
# model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

print(f"Region: us-east-1")
print(f"Model: {model_id}")
print("-" * 60)

try:
    print("\nSending test request to Bedrock...")
    response = bedrock_client.converse(
        modelId=model_id,
        messages=[
            {"role": "user", "content": [{"text": "Say hello in exactly 5 words"}]},
        ],
        system=[{"text": "You are a helpful assistant"}],
        inferenceConfig={
            "maxTokens": 100,
            "temperature": 0.7,
        },
    )

    response_text = response["output"]["message"]["content"][0]["text"]
    usage = response.get("usage", {})

    print("\n✅ SUCCESS! Bedrock is working correctly.")
    print("-" * 60)
    print(f"Response: {response_text}")
    print("-" * 60)
    print(f"Input tokens: {usage.get('inputTokens', 0)}")
    print(f"Output tokens: {usage.get('outputTokens', 0)}")
    print("-" * 60)
    print("\n✨ Your FastAPI app should now work correctly!")
    print("\nℹ️  Note: Token likelihoods (logprobs) are not available in AWS Bedrock.")
    print("   See test_bedrock_logprobs.py for details and alternatives.")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Make sure your AWS credentials have Bedrock access")
    print("2. Check that the model is enabled in AWS Bedrock Console (Model access)")
    print("3. Verify you're using the correct region (us-east-1)")
    print(
        "4. For Claude models, you need to fill out the Anthropic use case form first"
    )
