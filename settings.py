import os
import google.generativeai as genai
GOOGLE_API_KEY = os.environ['APIKEY']
genai.configure(api_key=GOOGLE_API_KEY)