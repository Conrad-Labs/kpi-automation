from openai import OpenAI
from config import OPENAI

# OpenAI setup
client = OpenAI(api_key=OPENAI['api_key'])
model = OPENAI['model']
