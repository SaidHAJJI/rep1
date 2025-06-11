from flask import Flask, request, jsonify
import json
import random # For selecting random exercises
import os # For path handling

app = Flask(__name__)

# Construct path relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXERCISES_FILE_PATH = os.path.join(SCRIPT_DIR, "../../data/evaluation_exercises/sample_evaluation_exercises.json")
exercises = []

def load_exercises():
    global exercises
    try:
        # Normalize the path to handle any ".." components correctly
        normalized_path = os.path.normpath(EXERCISES_FILE_PATH)
        with open(normalized_path, 'r') as f:
            exercises_data = json.load(f)
            if isinstance(exercises_data, list): # Assuming the JSON file contains a list of exercises
                exercises = exercises_data
            else: # If JSON is a dict with a key like "exercises"
                exercises = exercises_data.get("exercises", [])
            print(f"Loaded {len(exercises)} exercises from {normalized_path}.")
    except FileNotFoundError:
        print(f"Warning: Exercise file not found at {EXERCISES_FILE_PATH} (resolved to {os.path.normpath(EXERCISES_FILE_PATH)}). Serving from empty list.")
        exercises = []
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {EXERCISES_FILE_PATH}. Serving from empty list.")
        exercises = []

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    # Placeholder AI response logic
    ai_response = f"Received your message: '{user_message}'. I am a friendly AI. (This is a placeholder response)"

    # Simulate thinking/curiosity (very basic)
    if "?" not in user_message and len(user_message.split()) > 3 : # If it's not a question and somewhat substantial
        if random.random() < 0.3: # 30% chance to ask a clarifying question
            ai_response += " Could you tell me more about that?"

    return jsonify({'response': ai_response})

@app.route('/get_exercise', methods=['GET'])
def get_exercise():
    if not exercises:
        return jsonify({'error': 'No exercises available.'}), 404

    # Serve a random exercise for now
    exercise = random.choice(exercises)
    return jsonify(exercise)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    exercise_id = data.get('exercise_id', '')
    user_answer = data.get('answer', '')

    # Placeholder feedback logic
    # In a real app, you'd look up the exercise_id and check the answer
    found_exercise = next((ex for ex in exercises if ex.get("exercise_id") == exercise_id), None)

    if not found_exercise:
        return jsonify({'feedback': 'Exercise not found.', 'correct': False}), 404

    correct_answer_field = found_exercise.get('correct_answer', '') # For T/F, short_answer
    is_correct = False
    feedback_text = "Your answer has been submitted. (Placeholder feedback - correctness not fully checked)"

    if found_exercise.get("exercise_type") == "multiple_choice":
        correct_option = next((opt for opt in found_exercise.get("options", []) if opt.get("is_correct")), None)
        if correct_option:
            # Assuming user_answer is the option_text for MCQs
            if correct_option.get("option_text") == user_answer:
                is_correct = True
            feedback_text = f"Your answer '{user_answer}' was {'correct' if is_correct else 'incorrect'}. The correct answer is '{correct_option.get('option_text')}'."
        else:
            feedback_text = "Could not determine the correct answer for this MCQ from the data."

    elif found_exercise.get("exercise_type") == "true_false":
        if str(user_answer).strip().lower() == str(correct_answer_field).strip().lower():
            is_correct = True
        feedback_text = f"Your answer '{user_answer}' was {'correct' if is_correct else 'incorrect'}. The correct answer is {correct_answer_field}."

    elif found_exercise.get("exercise_type") == "short_answer":
        # Short answer grading is complex. This is a very basic placeholder.
        # A more robust check might involve keyword matching, semantic similarity, or length checks.
        if user_answer and correct_answer_field and user_answer.strip().lower() in correct_answer_field.strip().lower(): # Simple substring check
            is_correct = True # This is a very lenient 'correct'
        feedback_text = f"Received your short answer. {'It seems to align with some key concepts!' if is_correct else 'Further review might be needed.'} (Model answer hint: {correct_answer_field})"

    return jsonify({'feedback': feedback_text, 'correct': is_correct})

if __name__ == '__main__':
    load_exercises() # Load exercises when the app starts
    app.run(debug=True, port=5000) # Port 5000 for backend
