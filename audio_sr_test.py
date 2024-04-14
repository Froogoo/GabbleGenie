import json
from pathlib import Path
import speech_recognition as sr
from datetime import datetime
from pynput import keyboard
import logging
CHUNK_SIZE = 10240

logging.basicConfig(level=logging.INFO)
recording = True

def on_press(key):
    global recording
    try:
        if hasattr(key, 'char') and key.char == 'q':
            recording = False
            logging.info("Recording stopped by user.")
            return False  # Stop listener
    except Exception as e:
        logging.error(f"Error in key press handling: {e}")

class AudioDataManager:
    def __init__(self, filename='conversation_data.json'):
        self.filename = Path(filename)
        self.data = self.load_data()

    def load_data(self):
        if self.filename.exists():
            with open(self.filename, 'r') as file:
                return json.load(file)
        else:
            return {'conversations': []}
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
            r.adjust_for_ambient_noise(source)
            print("Recording... Press 'q' to stop.")
            audio_data = []
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
    
            try:
                while recording:
                    chunk = source.stream.read(CHUNK_SIZE)
                    audio_data.append(chunk)
            except KeyboardInterrupt:
                print("Recording manually stopped (KeyboardInterrupt).")
            finally:
                listener.stop()
                print("Listener stopped.")
    
            audio = sr.AudioData(b''.join(audio_data), source.SAMPLE_RATE, source.SAMPLE_WIDTH)
            audio_file_path = Path('temp_audio.wav')
            audio_file_path.write_bytes(audio.get_wav_data())
            text = self.transcribe_audio(audio_file_path)
            return audio_file_path.as_posix(), text
    
    def transcribe_audio(self, audio_file_path):
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            logging.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None

    def show_current_data(self):
        print("\nCurrent Data:")
        print(json.dumps(self.data, indent=4))

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
