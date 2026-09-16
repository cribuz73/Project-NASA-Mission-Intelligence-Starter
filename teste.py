from dotenv import load_dotenv
import os

#import os

#username = os.environ.get("MY_USERNAME")
#password = os.environ.get("MY_PASSWORD")
#print(f"username: {username}, password: {password}")
#print(os.environ.get("PYTHONPATH"))

#api_key = os.getenv("OPENAI_API_KEY")
    
#if not api_key:
#        raise ValueError("OpenAI API key is required.")

#from llm_client import generate_response
#response = generate_response(api_key, "What was Apollo 11?", "", [])
#print(response)

#from rag_client import discover_chroma_backends
#backends = discover_chroma_backends()
#print(backends)

from ragas_evaluator import evaluate_response_quality
scores = evaluate_response_quality("question", "answer", ["context"])
print(scores)