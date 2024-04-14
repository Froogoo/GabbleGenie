# GabbleGenie
Google_MHacks_24
# Project Title: Conversation Flow Analysis and Visualization
Description:
Utilize Google's new Gemini API to record your small talk interactions on the fly. You can pre-enter information about the people you're chatting with, such as known bios, as well as input the conversational environment and your desired end goals for the chat. It uses a decision tree to calculate the probability of achieving your conversation goals at each node. If the probability is low, you can backtrack to previous conversation nodes, and it will suggest alternative ways of conversing that are more likely to achieve your goals. It also informs you of the current potential social awkwardness level.
# Features:
Data Preprocessing: Cleansing and formatting raw conversation data.
Conversation Analysis: Utilizes Gemini1.5 Pro to analyze conversation patterns and structures.
Decision Tree Generation: Constructs decision trees based on conversation analysis results.
(Future development required)
Interactive Visualization: Visualizes decision trees in an interactive and visually appealing manner.
Enhanced User Experience: Optimizes user interaction and experience through frontend development.

# Project Structure:
user_management.py: Handles data cleaning and formatting tasks.
conversation_manager.py: Generates decision trees based on conversation analysis.
user_flow.py: Implements interactive visualization of decision trees.
(require further fix)audio_preprocessing.py: Transcribe audio wav to scripts.
(future step)frontend_development.py: Develops frontend components for enhanced user experience.
(future step)user_interaction.py: Orchestrates the entire workflow and provides user interaction.
# Usage:
Prepare conversation data in a suitable format, prefer wav.
Use audio_preprocessing.py to analyze conversation patterns.
Generate decision trees in json with conversation_manager.py.
Visualize decision trees interactively using user_flow.py.
(future step)Enhance user experience with frontend_development.py.

# Contributors:
Congxiao Wang, 
Ziyi Jiang
