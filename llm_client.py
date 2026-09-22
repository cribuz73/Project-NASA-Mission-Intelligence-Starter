from pyexpat.errors import messages
from typing import Dict, List
from xml.parsers.expat import model
from xmlrpc import client
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    # TODO: Define system prompt
    system_prompt = ("You are a NASA mission information assistant"
        "Answer the user's question using ONLY the information contained"
        "in the retrieved context."

        "The retrieved context comes from NASA mission documents."

        "Rules:"
        "1. Use the retrieved context as the primary and authoritative source."
        "2. Do not invent facts that are not supported by the context."
        "3. Do not rely on general NASA knowledge when the retrieved context"
        "does not support the answer."
        "4. Provide a detailed answer when the retrieved documents contain"
        "sufficient information."
        "5. When possible, identify the mission, document source, technical"
        "details, dates, crew members, events, and operational information"
        "contained in the context."
        "6. If the context does not contain enough information to answer the"
        "question, explicitly say that the retrieved documents do not provide"
        "enough information.")

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
    # TODO: Create OpenAI Client

    client = OpenAI(api_key=openai_key, base_url="https://openai.vocareum.com/v1") 

    # TODO: Send request to OpenAI
   
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1400,
        temperature=0,
    )

    # TODO: Return response

    return response.choices[0].message.content.strip()