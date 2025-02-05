from .deepseek import DeepSeekClient
from dotenv import load_dotenv
import os

load_dotenv()

deepseek = DeepSeekClient(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    context=open('context.txt').read()
)