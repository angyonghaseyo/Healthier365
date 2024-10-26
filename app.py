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
    prompt = "Please provide a detailed nutritional analysis of the food in this image, including Carbohydrates, Proteins, Fats, Vitamins, Minerals, Dietary fibre, and Water."

    response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt,
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

# Update the helper functions to include health considerations
def generate_prompt_with_health_info(base_prompt, health_info=None):
    if health_info:
        health_prompt = (
            f"\n\nAdditional health information to consider:\n"
            f"- Age: {health_info.get('age', 'Not provided')}\n"
            f"- Gender: {health_info.get('gender', 'Not provided')}\n"
            f"- Weight: {health_info.get('weight', 'Not provided')} kg\n"
            f"- Height: {health_info.get('height', 'Not provided')} cm\n"
            f"- Health conditions: {', '.join(health_info.get('health_conditions', [])) if health_info.get('health_conditions') else 'None'}"
        )
        return base_prompt + health_prompt
    return base_prompt

# Update the suggest_meal, provide_dietary_advice, and create_meal_plan functions accordingly
def suggest_meal(preferences, dietary_restrictions, goal, meal_type, cuisine, health_info):
    base_prompt = (
        f"Suggest a {meal_type} based on the following preferences: {preferences}, "
        f"dietary restrictions: {dietary_restrictions}, health goal: {goal}, "
        f"and cuisine preference: {cuisine}."
    )
    prompt = generate_prompt_with_health_info(base_prompt, health_info)
    meal_suggestion = generate_chat_response(prompt, max_tokens=150)
    return meal_suggestion

# Nutritional Analysis Function
def analyze_nutrition(meal):
    prompt = f"Provide a nutritional analysis of the following meal: '{meal}'."
    nutrition_analysis = generate_chat_response(prompt, max_tokens=100)
    return nutrition_analysis

# Dietary Advice Function
def provide_dietary_advice(goal, current_diet, activity_level, preferred_meal_types, allergies, health_info):
    # Create a detailed prompt using all the provided inputs
    base_prompt = (
        f"Provide dietary advice to achieve the health goal: '{goal}' "
        f"given the current diet: '{current_diet}', activity level: '{activity_level}', "
        f"preferred meal types: {', '.join(preferred_meal_types)}, and "
        f"allergies or intolerances: {', '.join(allergies) if allergies else 'None'}."
    )
    
    prompt = generate_prompt_with_health_info(base_prompt, health_info)
    dietary_advice = generate_chat_response(prompt, max_tokens=150)
    return dietary_advice


# Personalized Meal Planning Function
def create_meal_plan(preferences, dietary_restrictions, goal, activity_level, cuisine, meal_types, health_info):
    duration = 1  # Default duration for the meal plan
    # Create a detailed prompt with more specific information, considering location (Singapore) and user preferences
    base_prompt = (
        f"Create a {duration} day meal plan in Singapore with the following details:\n"
        f"- Food preferences: {preferences}\n"
        f"- Dietary restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}\n"
        f"- Health goal: {goal}\n"
        f"- Activity level: {activity_level if activity_level else 'Not specified'}\n"
        f"- Preferred cuisines: {', '.join(cuisine) if cuisine else 'Any'}\n"
        f"- Preferred meal types: {', '.join(meal_types) if meal_types else 'Any'}\n"
        f"Include time, location, date, food items, and detailed nutritional information for each food item."
    )
    
    prompt = generate_prompt_with_health_info(base_prompt, health_info)
    meal_plan = generate_chat_response(prompt, max_tokens=400)
    return meal_plan


# Flask API Endpoints
@app.route('/api/meal_suggestion', methods=['POST'])
def meal_suggestion_api():
    try:
        data = request.get_json()
        preferences = data['preferences']
        dietary_restrictions = data['dietary_restrictions']
        goal = data['goal']
        meal_type = data['meal_type']
        cuisine = data['cuisine']
        health_info = data.get('health_info', {})

        # Pass the new fields to the suggest_meal function
        meal_suggestion = suggest_meal(preferences, dietary_restrictions, goal, meal_type, cuisine, health_info)
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
        activity_level = data.get('activity_level', '')
        preferred_meal_types = data.get('preferred_meal_types', [])
        allergies = data.get('allergies', [])
        health_info = data.get('health_info', {})

        # Pass the new fields to the provide_dietary_advice function
        dietary_advice = provide_dietary_advice(goal, current_diet, activity_level, preferred_meal_types, allergies, health_info)
        return jsonify({'dietary_advice': dietary_advice})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/meal_plan', methods=['POST'])
def meal_plan_api():
    try:
        data = request.get_json()
        preferences = data['plan_preferences']
        dietary_restrictions = data.get('plan_dietary_restrictions', [])
        goal = data['plan_goal']
        activity_level = data.get('activity_level_plan', '')
        cuisine = data.get('plan_cuisine', [])
        meal_types = data.get('meal_types_plan', [])
        health_info = data.get('health_info_plan', {})

        # Pass the new fields to the create_meal_plan function
        meal_plan = create_meal_plan(preferences, dietary_restrictions, goal, activity_level, cuisine, meal_types, health_info)
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
