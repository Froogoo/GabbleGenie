import json
from datetime import datetime
from pathlib import Path

class DataManager:
    def __init__(self, filename='conversation_data.json'):
        self.filename = Path(filename)
        self.data = self.load_data()

    def load_data(self):
        if self.filename.exists():
            with open(self.filename, 'r') as file:
                return json.load(file)
        else:
            return {
                'users': [],
                'environment': None,
                'conversation_goals': [],
                'conversations': []
            }

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    # def update_user_info(self, user_info):
    #     for user in self.data['users']:
    #         if user['name'] == user_info['name']:
    #             user.update(user_info)
    #             return
    #     self.data['users'].append(user_info]
    def add_or_update_user_info(self):
        name = input("Enter user's name: ")
        bio = input("Enter a short bio (you can include age, profession, interests): ")
        for user in self.data['users']:
            if user['name'] == name:
                user['bio'] = bio
                print("User info updated.")
                return
        self.data['users'].append({'name': name, 'bio': bio})
        print("New user added.")

    def set_environment(self, environment):
        self.data['environment'] = environment

    def add_conversation_goal(self, goal):
        if goal not in self.data['conversation_goals']:
            self.data['conversation_goals'].append(goal)

    def add_conversation_record(self, speaker, text):
        record = {
            'date': str(datetime.now()),
            'speaker': speaker,
            'text': text
        }
        self.data['conversations'].append(record)

    def show_current_data(self):
        print("\nCurrent Data:")
        print(json.dumps(self.data, indent=4))

def get_input(prompt):
    return input(prompt)

# def main():
#     dm = DataManager()
#     while True:
#         dm.show_current_data()
#         print("\n1. Update User Info")
#         print("2. Set Environment")
#         print("3. Add Conversation Goal")
#         print("4. Add Conversation Record")
#         print("5. Save and Exit")
#         choice = get_input("Choose an option: ")

#         if choice == '1':
#             name = get_input("Enter user's name: ")
#             age = get_input("Enter user's age: ")
#             interests = get_input("Enter user's short des: ").split(',')
#             dm.update_user_info({'name': name, 'age': age, 'interests': interests})
#         elif choice == '2':
#             environment = get_input("Enter conversation environment: ")
#             dm.set_environment(environment)
#         elif choice == '3':
#             goal = get_input("Enter conversation goal: ")
#             dm.add_conversation_goal(goal)
#         elif choice == '4':
#             speaker = get_input("Enter speaker's name: ")
#             text = get_input("Enter conversation text: ")
#             dm.add_conversation_record(speaker, text)
#         # elif choice == '4':
#         #     record = get_input("Enter conversation text: ")
#         #     dm.add_conversation_record({'date': str(datetime.now()), 'text': record})
#         elif choice == '5':
#             dm.save_data()
#             print("All updates have been saved.")
#             break
#         else:
#             print("Invalid option. Please try again.")

# if __name__ == '__main__':
#     main()
####################################different input structure##########################
##################
##################
# def main():
#     dm = DataManager()
#     action_list = [
#         ("Update User Info", dm.update_user_info),
#         ("Set Environment", dm.set_environment),
#         ("Add Conversation Goal", dm.add_conversation_goal),
#         ("Add Conversation Record", dm.add_conversation_record)
#     ]
    
#     for description, action in action_list:
#         dm.show_current_data()
#         if get_input(f"Do you want to {description}? (yes/no): ").lower() == 'yes':
#             if description == "Add Conversation Record":
#                 speaker = get_input("Enter speaker's name: ")
#                 text = get_input("Enter conversation text: ")
#                 action(speaker, text)
#             else:
#                 data = get_input(f"Enter {description.lower()}: ")
#                 action(data)
#         else:
#             if get_input("Do you want to exit? (yes/no): ").lower() == 'yes':
#                 break

#     dm.save_data()
#     print("All updates have been saved.")

# if __name__ == '__main__':
#     main()
####################################different input structure##########################
##################
##################
def main():
    dm = DataManager()
    while True:
        print("\n1. Add/Update User Info")
        print("2. Set Environment")
        print("3. Add Conversation Goal")
        print("4. Add Conversation Record")
        print("5. Save and Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            while True:
                dm.add_or_update_user_info()
                if input("Add another user? (yes/no): ").lower() != 'yes':
                    break
        elif choice == '2':
            environment = input("Enter the environment: ")
            dm.set_environment(environment)
        elif choice == '3':
            goal = input("Enter the goal: ")
            dm.add_conversation_goal(goal)
        elif choice == '4':
            speaker = input("Enter speaker's name: ")
            text = input("Enter the conversation text: ")
            dm.add_conversation_record(speaker, text)
        elif choice == '5':
            dm.save_data()
            print("All updates have been saved.")
            break
        else:
            print("Invalid option. Please try again.")
        dm.show_current_data()

if __name__ == '__main__':
    main()









