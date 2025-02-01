from dotenv import load_dotenv
import os
from openai import OpenAI
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

api_key = os.getenv('OPENAI_API_KEY')
print(f"Using API key: {api_key[:10]}...")

try:
    client = OpenAI(api_key=api_key)
    
    # Try to make a simple API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using gpt-3.5-turbo as specified in your .env
        messages=[
            {"role": "user", "content": "Say 'Hello, this is a test!'"}
        ]
    )
    
    print("\nAPI Test Successful!")
    print("Response:", response.choices[0].message.content)
    
except Exception as e:
    print("\nError testing OpenAI API:")
    print(str(e))
