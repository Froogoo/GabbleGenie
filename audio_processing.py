# def audio_to_text(audio_data):
#     # Process audio data and return text
#     pass

#!pip install SpeechRecognition
import json
from pathlib import Path
import speech_recognition as sr
from datetime import datetime
import google.generativeai as genai
import time
from pynput import keyboard
import logging

CHUNK_SIZE = 102400


now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

recording = True

def on_press(key):
    global recording
    print(f"Key pressed: {key}")
    if key.char == 'q':
        recording = False
        return False

class AudioDataManager:
    def __init__(self, filename='conversation_data.json'):
        self.filename = Path(filename)
        self.data = self.load_data()

    def load_data(self):
        if self.filename.exists():
            with open(self.filename, 'r') as file:
                return json.load(file)
        else:
            return {
                'conversations': []
            }

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_conversation_record(self, speaker, text=None, audio_path=None):
        record = {
            'date': str(datetime.now()),
            'speaker': speaker,
            'text': text,
            'audio_path': audio_path
        }
        if not audio_path:
            record['audio_path'] = self.cache_and_transcribe_audio()
        self.data['conversations'].append(record)

    # def cache_and_transcribe_audio(self):
    #     r = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         print("Recording... Press 'q' to stop.")
    #         audio_data = []

    #         def on_press(key):
    #             print(f"Key pressed: {key}")
    #             if key.char == 'q':
    #                 return False
    #         listener = keyboard.Listener(on_press=on_press)
    #         listener.start()

    #         try:
    #             while True:
    #                 chunk = source.stream.read(CHUNK_SIZE)
    #                 audio_data.append(chunk)
    #         except KeyboardInterrupt:
    #             print("Recording stopped.")
    #             pass
    #         listener.stop()
    #         print("Listener stopped.")
    def cache_and_transcribe_audio(self):
        global recording  # Access the global flag variable
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Recording... Press 'q' to stop.")
            audio_data = []

            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            try:
                while recording:
                    chunk = source.stream.read(1024)
                    audio_data.append(chunk)
            except KeyboardInterrupt:
                print("Recording stopped (KeyboardInterrupt).")
                pass
            listener.stop()
            print("Listener stopped.")

            # audio = sr.AudioData(b''.join(audio_data), source.SAMPLE_RATE, source.SAMPLE_WIDTH)
            # audio_file_path = Path('temp_audio.wav')
            # audio_file_path.write_bytes(audio.get_wav_data())
            audio = sr.AudioData(b''.join(audio_data), source.SAMPLE_RATE, source.SAMPLE_WIDTH)
            audio_file_path = Path('temp_audio.wav')
            audio_file_path.write_bytes(audio.get_wav_data())
            summary = summarize_audio(audio_file_path)
            if summary:
                print("Summary:")
                print(summary)
            else:
                print("Failed to generate summary.")
            text = summarize_audio(audio_file_path)
            return audio_file_path, text

    def show_current_data(self):
        print("\nCurrent Data:")
        print(json.dumps(self.data, indent=4))

# def transcribe_audio_with_speaker_id(audio_file_path):
#     logging.info(f"Starting transcription for audio file: {audio_file_path}")

#     try:
#         with open(audio_file_path, "rb") as f:
#             audio_data = f.read()

#         request = genai.AudioRequest(
#             audio=audio_data.hex(),
#             config=genai.AudioConfig(
#                 encoding="LINEAR16",
#                 sample_rate_hertz=16000,
#                 language_code="en-US"
#             )
#         )
#         prompt = "Transcribe the audio and identify different speakers. Use markdown formatting with '>' for each speaker's dialogue."

#         response = genai.transcribe(request, prompt=prompt)

#         if response.status.code == genai.StatusCode.OK:
#             transcription = response.result.text
#             logging.info(f"Transcription successful: {transcription}")
#             return transcription
#         else:
#             logging.error(f"Transcription failed: {response.status.message}")
#             return None

#     except Exception as e:
#         logging.exception(f"An error occurred during transcription: {e}")
#         return None
def summarize_audio(audio_file_path):
    """Generates a summary of the given audio file using Gemini."""

    logging.info(f"Starting audio summarization for: {audio_file_path}")

    try:
        uploaded_file = genai.upload_file(path=audio_file_path)
        prompt = "Listen carefully to the following audio file. Provide a brief summary."
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        response = model.generate_content([prompt, uploaded_file])

        if response.status.code == genai.StatusCode.OK:
            summary = response.result.text
            logging.info(f"Summarization successful: {summary}")
            return summary
        else:
            logging.error(f"Summarization failed: {response.status.message}")
            return None

    except Exception as e:
        logging.exception(f"An error occurred during summarization: {e}")
        return None

def main():
    dm = AudioDataManager()
    while True:
        print("\n1. Add Conversation Record")
        print("2. Save and Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            speaker = input("Enter speaker's name: ")
            dm.add_conversation_record(speaker)
        elif choice == '2':
            dm.save_data()
            print("All updates have been saved.")
            break
        else:
            print("Invalid option. Please try again.")
        dm.show_current_data()

if __name__ == '__main__':
    main()