"""
Test script to check which models support logprobs (log probabilities)
"""
import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")

print("=" * 80)
print("TESTING LOGPROBS SUPPORT IN AWS BEDROCK MODELS")
print("=" * 80)
print()

# Test models you have access to
test_cases = [
    {
        "name": "Meta Llama 3.1 8B (Native API)",
        "model_id": "meta.llama3-1-8b-instruct-v1:0",
        "api": "native",
        "body": json.dumps({
            "prompt": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>Say hi<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
            "max_gen_len": 10,
            "temperature": 0.1,
        })
    },
    {
        "name": "Claude 3.5 Sonnet v2 (Converse API)",
        "model_id": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "api": "converse",
    },
    {
        "name": "Amazon Titan (Native API)",
        "model_id": "amazon.titan-text-express-v1",
        "api": "native",
        "body": json.dumps({
            "inputText": "Say hi",
            "textGenerationConfig": {
                "maxTokenCount": 10,
                "temperature": 0.1,
            }
        })
    }
]

for test in test_cases:
    print(f"\n{'='*80}")
    print(f"Testing: {test['name']}")
    print(f"Model ID: {test['model_id']}")
    print(f"API: {test['api']}")
    print("-" * 80)
    
    try:
        if test['api'] == 'native':
            # Test Native InvokeModel API
            response = bedrock.invoke_model(
                modelId=test['model_id'],
                body=test['body']
            )
            response_body = json.loads(response['body'].read())
            
            print("✅ Model invoked successfully")
            print("\nResponse structure:")
            print(json.dumps(response_body, indent=2)[:500])
            
            # Check for logprobs in response
            has_logprobs = any(key for key in response_body.keys() if 'logprob' in key.lower())
            if has_logprobs:
                print("\n🎯 LOGPROBS FOUND!")
            else:
                print("\n❌ No logprobs in response")
                print("Available fields:", list(response_body.keys()))
                
        elif test['api'] == 'converse':
            # Test Converse API
            response = bedrock.converse(
                modelId=test['model_id'],
                messages=[{"role": "user", "content": [{"text": "Say hi"}]}],
                inferenceConfig={"maxTokens": 10, "temperature": 0.1}
            )
            
            print("✅ Model invoked successfully")
            print("\nResponse structure:")
            response_preview = {k: v for k, v in response.items() if k != 'ResponseMetadata'}
            print(json.dumps(response_preview, indent=2, default=str)[:500])
            
            # Check for logprobs
            has_logprobs = any(key for key in response.keys() if 'logprob' in key.lower())
            if has_logprobs:
                print("\n🎯 LOGPROBS FOUND!")
            else:
                print("\n❌ No logprobs in response")
                print("Available top-level fields:", [k for k in response.keys() if k != 'ResponseMetadata'])
                
    except Exception as e:
        print(f"❌ Error: {str(e)[:200]}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("""
Based on AWS Bedrock documentation:

❌ Claude models (Anthropic): NO logprobs support
❌ Meta Llama models: NO logprobs support in AWS Bedrock
❌ Amazon Titan: NO logprobs support
✅ Cohere models: YES - Support logprobs (but you don't have SCP access)
✅ Custom models: May support logprobs depending on implementation

Unfortunately, NONE of the models you have SCP access to support logprobs:
- Anthropic Claude (all versions): No logprobs
- Meta Llama (all versions): No logprobs  
- Amazon Titan: No logprobs

The only models in AWS Bedrock that support logprobs are:
- Cohere Command models (BLOCKED by SCP in your account)
- Custom fine-tuned models (if configured to return logprobs)
""")
