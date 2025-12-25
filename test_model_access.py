import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")

# Models to test
test_models = [
    ("Anthropic Claude 3.5 Sonnet v2", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
    ("Anthropic Claude 3 Opus", "anthropic.claude-3-opus-20240229-v1:0"),
    ("Cohere Command R", "cohere.command-r-v1:0"),
    ("Cohere Command R+", "cohere.command-r-plus-v1:0"),
    ("Meta Llama 3.1 8B", "meta.llama3-1-8b-instruct-v1:0"),
    ("Mistral 7B", "mistral.mistral-7b-instruct-v0:2"),
    ("Amazon Titan", "amazon.titan-text-express-v1"),
]

print("Testing Model Access Permissions")
print("=" * 80)
print()

allowed = []
denied = []

for name, model_id in test_models:
    try:
        print(f"Testing: {name}...", end=" ")
        
        # Try to invoke the model with minimal request
        response = bedrock.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": "Hi"}]}],
            inferenceConfig={"maxTokens": 10, "temperature": 0},
        )
        
        print("✅ ALLOWED")
        allowed.append((name, model_id))
        
    except bedrock.exceptions.AccessDeniedException as e:
        print("❌ DENIED (SCP)")
        denied.append((name, model_id, "SCP Deny"))
        
    except Exception as e:
        error_type = type(e).__name__
        print(f"❌ DENIED ({error_type})")
        denied.append((name, model_id, error_type))

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

print(f"✅ ALLOWED MODELS ({len(allowed)}):")
for name, model_id in allowed:
    print(f"  - {name}")
    print(f"    {model_id}")
print()

print(f"❌ DENIED MODELS ({len(denied)}):")
for name, model_id, reason in denied:
    print(f"  - {name} ({reason})")
    print(f"    {model_id}")
print()

print("=" * 80)
print("RECOMMENDATION")
print("=" * 80)
print()
if allowed:
    print("Your organization allows the following model providers:")
    providers = set([model_id.split('.')[0] for _, model_id in allowed])
    for provider in providers:
        print(f"  ✓ {provider}")
    print()
    print("Stick with these models for your FastAPI application.")
else:
    print("No models are accessible. Contact your AWS administrator.")
