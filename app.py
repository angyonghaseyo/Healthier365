from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os

# Allow CORS to all
app = Flask(__name__)
CORS(app)

# Load env file
load_dotenv()

# Set your OpenAI API key
api_key = os.getenv('API_KEY')

openai.api_key = api_key

# ... (Your predictive code below here)

# Helper function to interact with OpenAI API
def generate_chat_response(prompt, system_message="You are a nutrition and meal planning assistant.", max_tokens=100):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content'].strip()

# Helper function to encode the image and interact with OpenAI API
def analyze_food_image(base64_image):
    # Creating a prompt to send to OpenAI for analysis
    prompt = "Analyze the nutritional content of the food in this image."

    response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Please provide a detailed nutritional analysis of the food in this image, including Carbohydrates, Proteins, Fats, Vitamins, Minerals, Dietary fibre, and Water.",
            },
            {
            "type": "image_url",
            "image_url": {
                "url":  f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
)
    return response['choices'][0]['message']['content'].strip()


# Meal Suggestion Function
def suggest_meal(preferences, dietary_restrictions, goal):
    prompt = f"Suggest a meal based on the following preferences: {preferences}, dietary restrictions: {dietary_restrictions}, and health goal: {goal}."
    meal_suggestion = generate_chat_response(prompt, max_tokens=150)
    return meal_suggestion

# Nutritional Analysis Function
def analyze_nutrition(meal):
    prompt = f"Provide a nutritional analysis of the following meal: '{meal}'."
    nutrition_analysis = generate_chat_response(prompt, max_tokens=100)
    return nutrition_analysis

# Dietary Advice Function
def provide_dietary_advice(goal, current_diet):
    prompt = f"Provide dietary advice to achieve the health goal: '{goal}' given the current diet: '{current_diet}'."
    dietary_advice = generate_chat_response(prompt, max_tokens=150)
    return dietary_advice

# Personalized Meal Planning Function
def create_meal_plan(preferences, dietary_restrictions, goal, duration='7 days'):
    prompt = f"Create a {duration} meal plan based on the following preferences: {preferences}, dietary restrictions: {dietary_restrictions}, and health goal: {goal}."
    meal_plan = generate_chat_response(prompt, max_tokens=200)
    return meal_plan

# Flask API Endpoints
@app.route('/api/meal_suggestion', methods=['POST'])
def meal_suggestion_api():
    try:
        data = request.get_json()
        preferences = data['preferences']
        dietary_restrictions = data['dietary_restrictions']
        goal = data['goal']
        meal_suggestion = suggest_meal(preferences, dietary_restrictions, goal)
        return jsonify({'meal_suggestion': meal_suggestion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nutrition_analysis', methods=['POST'])
def nutrition_analysis_api():
    try:
        data = request.get_json()
        meal = data['meal']
        nutrition_analysis = analyze_nutrition(meal)
        return jsonify({'nutrition_analysis': nutrition_analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dietary_advice', methods=['POST'])
def dietary_advice_api():
    try:
        data = request.get_json()
        goal = data['advice_goal']
        current_diet = data['current_diet']
        dietary_advice = provide_dietary_advice(goal, current_diet)
        return jsonify({'dietary_advice': dietary_advice})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meal_plan', methods=['POST'])
def meal_plan_api():
    try:
        data = request.get_json()
        preferences = data['plan_preferences']
        dietary_restrictions = data['plan_dietary_restrictions']
        goal = data['plan_goal']
        duration = data.get('duration', '7 days')
        meal_plan = create_meal_plan(preferences, dietary_restrictions, goal, duration)
        return jsonify({'meal_plan': meal_plan})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Flask API endpoint for food image analysis
@app.route('/api/image_analysis', methods=['POST'])
def image_analysis_api():
    try:
        data = request.get_json()
        base64_image = data['image']
        analysis_result = analyze_food_image(base64_image)
        return jsonify({'nutritional_facts': analysis_result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# HTML rendering endpoints (for demo user interface)
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
