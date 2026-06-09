from dotenv import load_dotenv
import os
from groq import Groq
import logging
    
logger = logging.getLogger(__name__)

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_roast(prompt):
    try:
        logger.info("Calling Groq API to generate roast...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a funny github roaster."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        logger.info("Roast generated successfully")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling Groq API: {type(e).__name__}: {str(e)}")
        raise