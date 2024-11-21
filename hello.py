import google.generativeai as genai
import os
from dotenv import load_dotenv
import pathlib

# .env ファイルから環境変数を読み込む
load_dotenv()
genai.configure(api_key=os.environ["geminai_api"])

# Gemini モデルを初期化
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 文字起こしテキスト
transcription = "また、東寺のように、五大明王と呼ばれる、主要な明王の中央に配されることも多い。"  # 実際の文字起こしテキストを入力してください

# 音声ファイルのパスを指定
audio_file_path = 'input.wav'  # 実際の音声ファイルのパスに置き換えてください

# プロンプトを英語で作成
prompt = f"""Analyze the following audio and transcription text, and determine the speaker's emotion by selecting the most appropriate label from the list below:

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

Transcription text:
{transcription}
"""

# 音声データを読み込む
audio_data = {
    "mime_type": "audio/wav",
    "data": pathlib.Path(audio_file_path).read_bytes()
}

# プロンプトと音声データを Gemini に渡す
response = model.generate_content([prompt, audio_data])

# 結果を表示
print(response.text.strip())