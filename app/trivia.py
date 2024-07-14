from flask import Blueprint, jsonify, request
import random
import json

trivia_bp = Blueprint('trivia', __name__)

# Global variable to store trivia questions
trivia_data = None

# Fetching 100 questions from Open Trivia Database (OTDB) API and storing them
def fetch_questions():
    global trivia_data
    api_url = "https://opentdb.com/api.php?amount=100&type=multiple"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise exception for bad status codes

        data = response.json()

        if 'results' in data:
            trivia_questions = []

            for index, question in enumerate(data['results'], start=1):
                options = question['incorrect_answers'] + [question['correct_answer']]
                random.shuffle(options)
                correct_answer = question['correct_answer']
                trivia_questions.append({
                    'id': index,
                    'question': question['question'],
                    'options': options,
                    'answer': correct_answer,
                    'category': question['category']
                })

            trivia_data = trivia_questions
            print(f"Successfully fetched and stored {len(trivia_data)} questions.")
        else:
            print(f"Unexpected API response: {data}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")

# Endpoint to get a random trivia question and check answer in one route
@trivia_bp.route('/random', methods=['GET', 'POST'])
def trivia():
    global trivia_data

    # Ensure trivia questions are loaded
    if not trivia_data:
        fetch_questions()

    if request.method == 'GET':
        # Get a random question
        random_question = random.choice(trivia_data)
        return jsonify({
            'id': random_question['id'],
            'question': random_question['question'],
            'options': random_question['options'],
            'category': random_question['category'],
            'answer': random_question['answer']  # Include the answer in the response
        })

    elif request.method == 'POST':
        # Check answer for a specific question ID
        question_id = request.json.get('id')
        submitted_answer = request.json.get('answer')

        # Find the question by question_id
        question = next((q for q in trivia_data if q['id'] == question_id), None)

        if not question:
            return jsonify({'error': 'Question not found'}), 404

        correct_answer = question['answer']

        # Compare the submitted answer with the correct answer
        if submitted_answer.lower() == correct_answer.lower():
            return jsonify({
                'correct': True,
                'message': 'Correct answer!',
                'answer': correct_answer  # Include the correct answer in the response
            })
        else:
            return jsonify({
                'correct': False,
                'message': 'Incorrect answer.',
                'answer': correct_answer  # Include the correct answer in the response
            })

# Function to initialize the trivia data
def init_trivia_data():
    fetch_questions()

# Initialize trivia data when this module is imported
init_trivia_data()
