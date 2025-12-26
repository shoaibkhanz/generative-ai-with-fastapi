#!/usr/bin/env python
"""
❌ NO LONGER WORKS: Cohere Legacy Model Removed from Bedrock

ISSUE: The old Cohere Command v14 model (cohere.command-text-v14:7) that supported
       'return_likelihoods' parameter for logprobs is NO LONGER AVAILABLE in AWS Bedrock.

CURRENT STATUS:
  - Only Command R (cohere.command-r-v1:0) and Command R+ (cohere.command-r-plus-v1:0)
    are available
  - These models DO NOT support the 'return_likelihoods' parameter
  - They use a different API schema (Converse API with messages, not text completion)

ALTERNATIVES FOR LOGPROBS:
  1. Use Amazon Bedrock Converse API with other models (Claude, Llama, Mistral)
  2. Use OpenAI API directly (supports logprobs)
  3. Use Anthropic API directly (Claude supports logprobs via API)

This script is kept for historical reference only.
"""

import json

import boto3
import botocore.exceptions

# 1. Configuration
# ⚠️ WARNING: This model ID is no longer valid!
MODEL_ID = "cohere.command-text-v14:7"  # ❌ DEPRECATED - Not available anymore
REGION = "us-east-1"


def main():
    print(f"Connecting to Bedrock in {REGION}...")
    print(f"Targeting Model: {MODEL_ID} (Legacy Mode)")
    print("-" * 60)

    client = boto3.client("bedrock-runtime", region_name=REGION)

    # 2. The Legacy Payload
    # This schema is specific to Command v14.
    # It allows 'return_likelihoods', which Command R+ blocks.
    payload = {
        "prompt": "Explain Quantum Entanglement in one sentence.",
        "max_tokens": 100,
        "temperature": 0.5,
        "p": 0.99,  # Must be < 1.0 for this model
        "k": 0,
        "return_likelihoods": "GENERATION",  # <--- The Magic Parameter
        "num_generations": 1,
    }

    try:
        # 3. Direct Invocation
        response = client.invoke_model(modelId=MODEL_ID, body=json.dumps(payload))

        # 4. Parsing the "Text Completion" Response
        result = json.loads(response["body"].read())

        # The legacy response is a list of 'generations'
        generation = result["generations"][0]
        text = generation["text"]
        likelihoods = generation["token_likelihoods"]

        print("\n✅ SUCCESS: Logprobs Retrieved")
        print("=" * 60)
        print(f"Output: {text.strip()}")
        print("-" * 60)

        # 5. Displaying the Confidence Data
        print(f"{'TOKEN':<15} | {'LOGPROB':<10} | {'CONFIDENCE':<10}")
        print("-" * 40)

        for item in likelihoods[:5]:  # Show first 5 for brevity
            token_str = item.get("token").strip()
            # Logprob is usually negative (e.g., -0.05)
            lp = item.get("likelihood")
            # Convert to rough % confidence: e^lp
            confidence = float(2.71828**lp) * 100

            print(f"{token_str:<15} | {lp: .4f}    | {confidence:.1f}%")

        print(f"... ({len(likelihoods)} tokens total)")

    except botocore.exceptions.ClientError as e:
        err_msg = e.response["Error"]["Message"]
        if "extraneous key" in err_msg:
            print("\n❌ SCHEMA ERROR: You are likely using the wrong Model ID.")
            print("   Command R+ (v1) does not support this payload.")
            print("   Ensure you are using 'cohere.command-text-v14:7'.")
        else:
            print(f"\n❌ AWS ERROR: {err_msg}")

    except Exception as e:
        print(f"\n❌ SYSTEM ERROR: {str(e)}")


if __name__ == "__main__":
    main()
