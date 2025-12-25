#!/usr/bin/env python3
"""
Quick test script to verify AWS Bedrock access with Claude 3.5 Sonnet v2
"""

import boto3
import json

print("Testing AWS Bedrock access...")
print("-" * 60)

# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
)

model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"

print(f"Region: us-west-2")
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

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Make sure your AWS profile 'ai' has Bedrock access")
    print("2. Check that Claude models are enabled in AWS Bedrock Console")
    print("3. Verify you're using the correct region (us-west-2)")
