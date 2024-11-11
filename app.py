from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get the API key from the environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY found in environment variables")

GEMINI_API_URL = os.getenv('GEMINI_API_URL')

@app.route('/process_video', methods=['POST']) 
def process_video():
    data = request.json
    video_url = data.get('videoUrl')
    num_questions = data.get('numQuestions')

    # Extract video ID from the URL
    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    # Fetch transcript
    try:
        transcript = fetch_transcript(video_id)
    except Exception as e:
        return jsonify({'error': f'Error fetching transcript: {str(e)}'}), 400

    # Generate summary using Gemini API
    summary = generate_summary(transcript)

    # Generate quiz questions
    quiz = generate_quiz(transcript, num_questions)

    # Generate flashcards
    flashcards = generate_flashcards(transcript)

    return jsonify({
        'summary': summary,
        'quiz': quiz,
        'flashcards': flashcards
    })

def extract_video_id(url):
    # Simple extraction, you might want to use a more robust method
    if 'youtube.com/watch?v=' in url:
        return url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('/')[-1]
    return None

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        raise Exception(f"Could not retrieve transcript: {str(e)}")

def generate_summary(transcript):
    prompt = f"Summarize this transcript in a concise paragraph: {transcript[:4000]}"  # Limit to 4000 chars to avoid token limit
    return generate_content(prompt)

def generate_quiz(transcript, num_questions):
    prompt = f"Generate {num_questions} multiple-choice quiz questions based on this transcript. For each question, provide 4 options and indicate the correct answer: {transcript[:4000]}"
    quiz_text = generate_content(prompt)
    return parse_quiz(quiz_text, num_questions)

def generate_flashcards(transcript):
    prompt = f"Generate 5 flashcards based on this transcript. For each flashcard, provide a question and its answer: {transcript[:4000]}"
    flashcards_text = generate_content(prompt)
    return parse_flashcards(flashcards_text)

def generate_content(prompt):
    try:
        response = requests.post(
            GEMINI_API_URL,
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            },
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"}
        )
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling Gemini API: {str(e)}")
        logging.error(f"Response content: {e.response.content if e.response else 'No response content'}")
        return f"Error calling Gemini API: {str(e)}"

def parse_quiz(quiz_text, num_questions):
    # This is a simple parser and might need to be adjusted based on the actual output format
    questions = []
    lines = quiz_text.split('\n')
    for i in range(0, len(lines), 6):
        if len(questions) >= num_questions:
            break
        question = {
            'question': lines[i].split('. ', 1)[1] if '. ' in lines[i] else lines[i],
            'options': [
                lines[i+1].strip()[3:] if lines[i+1].strip().startswith('A. ') else lines[i+1].strip(),
                lines[i+2].strip()[3:] if lines[i+2].strip().startswith('B. ') else lines[i+2].strip(),
                lines[i+3].strip()[3:] if lines[i+3].strip().startswith('C. ') else lines[i+3].strip(),
                lines[i+4].strip()[3:] if lines[i+4].strip().startswith('D. ') else lines[i+4].strip()
            ]
        }
        questions.append(question)
    return questions

def parse_flashcards(flashcards_text):
    # This is a simple parser and might need to be adjusted based on the actual output format
    flashcards = []
    lines = flashcards_text.split('\n')
    for i in range(0, len(lines), 3):
        if i + 1 < len(lines):
            question = lines[i].split(': ', 1)[1] if ': ' in lines[i] else lines[i]
            answer = lines[i+1].split(': ', 1)[1] if ': ' in lines[i+1] else lines[i+1]
            flashcards.append({'question': question, 'answer': answer})
    return flashcards

if __name__ == '__main__':
    app.run(debug=True)