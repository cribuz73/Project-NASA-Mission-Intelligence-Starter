from pyexpat.errors import messages
from typing import Dict, List
from xml.parsers.expat import model
from xmlrpc import client
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    # TODO: Define system prompt
    system_prompt = ("You are a NASA expert that provides information about NASA missions. "
              "Use only the context provided to answer the user's question."
              "If you don't know the answer, say you don't know.\n\n")

    # TODO: Set context in messages

    messages = [
        {"role": "system", "content": system_prompt}
        ]
    if context:
            messages.append({"role": "system", "content": f"Context: {context}"})

    # TODO: Add chat history

    if conversation_history:
        for message in conversation_history:
             if isinstance(message, dict) and "role" in message and "content" in message:
                messages.append(message)
    
    messages.append({"role": "user", "content": user_message})
    # TODO: Creaet OpenAI Client

    client = OpenAI(api_key=openai_key, base_url="https://openai.vocareum.com/v1") 

    # TODO: Send request to OpenAI

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1400,
        temperature=0.7,
    )

    # TODO: Return response

    return response.choices[0].message.content.strip()