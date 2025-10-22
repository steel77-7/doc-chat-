from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=API_KEY)


# the request to gemini
def gen_content(context: str, query: str):
    prompt = f"""
    Answer the question based on the following context:

    {context}

    Question: {query}
    Answer:
    """
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text
