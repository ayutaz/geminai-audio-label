import google.generativeai as genai
import os
from dotenv import load_dotenv
import pathlib
import json
import time

# .env ファイルから環境変数を読み込む
load_dotenv()
genai.configure(api_key=os.environ["geminai_api"])

# Gemini モデルを初期化
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ルートディレクトリのパス
root_dir = './Data'  # 必要に応じて実際のパスに変更してください

# 感情ラベルのリストを英語で定義
emotion_labels = [
    "Angry",
    "Disgusted",
    "Embarrassed",
    "Fearful",
    "Happy",
    "Sad",
    "Surprised",
    "Neutral",
    "Sexual1",  # aegi voices
    "Sexual2"   # chupa voices
]

# ルートディレクトリからすべての index.json ファイルを再帰的に検索
index_files = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'index.json':
            index_files.append(os.path.join(root, file))

# 各 index.json ファイルを処理
for index_file_path in index_files:
    print(f"処理中のファイル: {index_file_path}")
    # index.json を読み込み
    with open(index_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # ベースとなるオーディオファイルのディレクトリパス
    base_audio_dir = os.path.dirname(index_file_path)

    # エントリ数を取得
    total_entries = len(data)

    # テストとして最初の100個のエントリのみ処理
    # ただし、まだ処理されていないエントリに限る
    processed_count = 0
    for i, entry in enumerate(data):
        if processed_count >= 100:
            break  # 100個処理したらループを抜ける

        speaker = entry["Speaker"]
        text = entry["Text"]
        audio_rel_path = entry["FilePath"]
        audio_file_path = os.path.join(base_audio_dir, audio_rel_path)

        # 既にEmotionLabelが存在する場合はスキップ（オプション）
        if "EmotionLabel" in entry and entry["EmotionLabel"]:
            print(f"[{i+1}/{total_entries}] 既に処理済み: {audio_rel_path}")
            continue

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
{text}
"""

        # 音声データを読み込む
        try:
            # ファイルの存在をチェック
            if not os.path.exists(audio_file_path):
                print(f"音声ファイルが見つかりません: {audio_file_path}")
                continue

            # 音声データを読み込み
            audio_data = {
                "mime_type": "audio/ogg",
                "data": pathlib.Path(audio_file_path).read_bytes()
            }
        except Exception as e:
            print(f"音声ファイルの読み込み中にエラーが発生しました: {e}")
            continue

        # プロンプトと音声データを Gemini に渡す
        try:
            response = model.generate_content([prompt, audio_data])
        except Exception as e:
            print(f"APIリクエスト中にエラーが発生しました: {e}")
            continue

        # レスポンスのテキストを取得し、スペースや改行を削除
        emotion_label = response.text.strip()

        # エントリにEmotionLabelを追加
        entry["EmotionLabel"] = emotion_label

        # 結果を表示（オプション）
        print(f"[{i+1}/{total_entries}] プロセス済み: {audio_rel_path}, 判定された感情: {emotion_label}")

        # レスポンスが返ってきたタイミングで index.json を更新
        with open(index_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 処理したエントリのカウントを増やす
        processed_count += 1

        # 次のリクエストまで1分間待機
        time.sleep(60)

    print(f"ファイルの処理が完了しました（{processed_count}件処理済み）: {index_file_path}")
    print("-" * 50)

print("全てのindex.jsonファイルの処理が完了しました（テストとして各ファイル100件まで処理）。")