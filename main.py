from user_interaction import start_interaction
from data_management import load_data_from_cache, save_data_to_cache
from conversation_manager import guide_conversation, analyze_conversation

def main():
    data = load_data_from_cache()
    start_interaction(data)
    save_data_to_cache(data)

if __name__ == '__main__':
    main()
