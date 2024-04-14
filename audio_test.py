import json
from pathlib import Path
import speech_recognition as sr
from datetime import datetime
import google.generativeai as genai
from pynput import keyboard
import logging

CHUNK_SIZE = 10584000

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
      json.dump(self.data, file)

  def add_conversation_record(self, speaker, text=None, audio_path=None):
    record = {
      'date': str(datetime.now()),
      'speaker': speaker,
      'text': text,
      'audio_path': audio_path
    }
    if not audio_path:
      record['audio_path'], record['text'] = self.cache_and_transcribe_audio()
    self.data['conversations'].append(record)

  def cache_and_transcribe_audio(self):
    global recording
    r = sr.Recognizer()
    with sr.Microphone() as source:
      print("Recording... Press 'q' to stop.")
      audio_data = []

      listener = keyboard.Listener(on_press=on_press)
      listener.start()
      try:
        while recording:
          chunk = source.stream.read(10584000)
          audio_data.append(chunk)
      except KeyboardInterrupt:
        print("Recording stopped (KeyboardInterrupt).")
        pass
      listener.stop()
      print("Listener stopped.")

      audio = sr.AudioData(b''.join(audio_data), source.SAMPLE_RATE, source.SAMPLE_WIDTH)
      audio_file_path = Path('temp_audio.mp3')
      audio_file_path.write_bytes(audio.get_wav_data())

      summary = summarize_audio(audio_file_path)
      if summary:
        print("Summary:")
        print(summary)
      else:
        print("Failed to generate summary.")
      return audio_file_path.as_posix(), summary

  def show_current_data(self):
    print("\nCurrent Data:")
    print(json.dumps(self.data, indent=4))

# def summarize_audio(audio_file_path):
#   logging.info(f"Starting audio summarization for: {audio_file_path}")
#   try:
#     uploaded_file = genai.upload_file(path=audio_file_path)
#     prompt = "Transcribe the audio and identify different speakers. Use markdown formatting with '>' for each speaker's dialogue."
#     model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
#     response = model.generate_content([prompt, uploaded_file])

#     if response.status.code == genai.StatusCode.OK:
#       summary = response.result.text
#       logging.info(f"Summarization successful: {summary}")
#       return summary
#     else:
#       logging.error(f"Summarization failed: {response.status.message}")
#       return None

#   except Exception as e:
#     logging.exception(f"An error occurred during summarization: {e}")
#     return None

def summarize_audio(audio_file_path):
    logging.info(f"Starting audio summarization for: {audio_file_path}")
    try:
        uploaded_file = genai.upload_file(path=audio_file_path)
        prompt = "Transcribe the audio and identify different speakers. Use markdown formatting with '>' for each speaker's dialogue."
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        response = model.generate_content([prompt, uploaded_file])
        if hasattr(response, 'result') and response.result.text:
            summary = response.result.text
            logging.info(f"Summarization successful: {summary}")
            return summary
        else:
            logging.error("Summarization failed: No result text provided.")
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