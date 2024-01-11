from flask import Flask, render_template, request, jsonify

import openai

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']

    # Check if the user's message contains medical terms
    if contains_medical_terms(user_message):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical chatbot restricted to answering questions only about medical and healthcare."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=100
        )
        ai_response = response['choices'][0]['message']['content']
    else:
        ai_response = "I can only answer questions related to medical and healthcare topics."

    return jsonify({'ai_response': ai_response})

def contains_medical_terms(user_message):
    # Implement a more sophisticated check for medical terms based on your specific needs
    medical_terms = ['health', 'medical', 'doctor', 'hospital', 'symptoms', 'diagnosis', 'treatment']
    return any(term in user_message.lower() for term in medical_terms)

if __name__ == '__main__':
    app.run(debug=True)
