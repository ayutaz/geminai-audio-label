import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.environ["geminai_api"])

# Initialize a Gemini model appropriate for your use case.
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Your transcription text
transcription = "また、東寺のように、五大明王と呼ばれる、主要な明王の中央に配されることも多い。"  # ここに実際の文字起こしテキストを入力してください

# Create the prompt in English
prompt = f"""Analyze the following text and determine the speaker's emotion by selecting the most appropriate label from the list below:

- Angry
- Disgusted
- Embarrassed
- Fearful
- Happy
- Sad
- Surprised
- Neutral
- Sexual1  # aegi voices
- Sexual2  # chupa voices

Please provide your answer by selecting only one emotion label from the list.

Text content:
{transcription}
"""

# Pass the prompt to Gemini.
response = model.generate_content([prompt])

# Print the response.
print(response.text.strip())