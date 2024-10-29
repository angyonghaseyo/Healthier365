from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# Set OpenAI API key
api_key = os.getenv('API_KEY')
openai.api_key = api_key

# Helper Functions for OpenAI API Interaction
def generate_chat_response(prompt, system_message="You are a nutrition and meal planning assistant.", max_tokens=100):
    """Generate a response using OpenAI's ChatCompletion API"""
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

def analyze_food_image(base64_image):
    """Analyze food image using OpenAI's Vision API"""
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
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    )
    return response['choices'][0]['message']['content'].strip()

# Helper Functions for Prompt Generation
def generate_prompt_with_health_info(base_prompt, health_info=None):
    """Generate a prompt that includes health information if available"""
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

# Core Feature Functions
def suggest_meal(preferences, dietary_restrictions, goal, meal_type, cuisine, health_info):
    """Generate a meal suggestion based on user preferences and health information"""
    base_prompt = (
        f"Please provide a detailed meal suggestion with the following structure:\n"
        f"1. Recommended Meal: Suggest a {meal_type} that fits {preferences} preferences\n"
        f"2. Main Ingredients: List the key ingredients\n"
        f"3. Nutritional Highlights: Provide key nutritional benefits\n"
        f"4. Preparation Tips: Include basic preparation guidance\n\n"
        f"Consider these parameters:\n"
        f"- Dietary restrictions: {dietary_restrictions}\n"
        f"- Health goal: {goal}\n"
        f"- Cuisine preference: {cuisine}"
    )
    prompt = generate_prompt_with_health_info(base_prompt, health_info)
    return generate_chat_response(prompt, max_tokens=300)

def analyze_nutrition(meal):
    """Provide nutritional analysis for a given meal"""
    prompt = f"""Please provide a comprehensive nutritional analysis of '{meal}' with the following structure:

1. Macronutrients:
   - Proteins: Content and benefits
   - Carbohydrates: Content and benefits
   - Fats: Content and types present

2. Micronutrients:
   - Vitamins: Key vitamins present
   - Minerals: Important minerals
   
3. Caloric Information:
   - Approximate calories per serving
   - Portion size reference
   
4. Health Benefits:
   - Key nutritional advantages
   - Dietary considerations
   - Recommendations for balanced consumption

Please provide detailed information for each section."""

    return generate_chat_response(prompt, max_tokens=600)

def provide_dietary_advice(goal, current_diet, activity_level, preferred_meal_types, allergies, health_info):
    """Generate personalized dietary advice"""
    base_prompt = (
        f"Please provide specific dietary advice with the following structure:\n"
        f"1. Main Recommendations\n"
        f"2. Foods to Include\n"
        f"3. Foods to Limit\n"
        f"4. Lifestyle Tips\n\n"
        f"Consider these factors:\n"
        f"- Health goal: {goal}\n"
        f"- Current diet: {current_diet}\n"
        f"- Activity level: {activity_level}\n"
        f"- Preferred meal types: {', '.join(preferred_meal_types)}\n"
        f"- Allergies/Intolerances: {', '.join(allergies) if allergies else 'None'}"
    )
    prompt = generate_prompt_with_health_info(base_prompt, health_info)
    return generate_chat_response(prompt, max_tokens=400)

def create_meal_plan(preferences, dietary_restrictions, goal, activity_level, cuisine, meal_types, health_info):
    """Generate a personalized meal plan"""
    base_prompt = (
        f"Create a detailed one-day meal plan in Singapore with this structure:\n"
        f"Breakfast (8:00 AM - ABC Food Court):\n"
        f"- Main dish\n"
        f"- Side items\n"
        f"- Nutritional highlights\n\n"
        f"Lunch (12:30 PM - XYZ Hawker Centre):\n"
        f"- Main dish\n"
        f"- Side items\n"
        f"- Nutritional highlights\n\n"
        f"Dinner (7:00 PM - Local Restaurant):\n"
        f"- Main dish\n"
        f"- Side items\n"
        f"- Nutritional highlights\n\n"
        f"Consider these parameters:\n"
        f"- Food preferences: {preferences}\n"
        f"- Dietary restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}\n"
        f"- Health goal: {goal}\n"
        f"- Activity level: {activity_level}\n"
        f"- Preferred cuisines: {', '.join(cuisine) if cuisine else 'Any'}\n"
        f"- Preferred meal types: {', '.join(meal_types) if meal_types else 'Any'}"
    )
    prompt = generate_prompt_with_health_info(base_prompt, health_info)
    return generate_chat_response(prompt, max_tokens=800)

# Response Formatting Functions
def format_meal_suggestion(meal_suggestion):
    """Format the meal suggestion into a structured response"""
    sections = [
        "Recommended Meal:",
        "Main Ingredients:",
        "Nutritional Highlights:",
        "Preparation Tips:"
    ]
    
    formatted_text = meal_suggestion
    for section in sections:
        if section.lower() not in formatted_text.lower():
            formatted_text = formatted_text.replace(". ", ".\n")
    
    return formatted_text

def format_dietary_advice(advice):
    """Format the dietary advice into bullet points"""
    points = advice.split(". ")
    formatted_points = [point.strip() + "." for point in points if point.strip()]
    return "\n".join(formatted_points)

def format_meal_plan(plan):
    """Format the meal plan into a structured daily schedule"""
    formatted_plan = []
    current_section = []
    
    for line in plan.split('\n'):
        line = line.strip()
        if not line:
            if current_section:
                formatted_plan.append('\n'.join(current_section))
                current_section = []
        else:
            if any(time_marker in line.lower() for time_marker in ['breakfast', 'lunch', 'dinner', 'snack']):
                if current_section:
                    formatted_plan.append('\n'.join(current_section))
                    current_section = []
            current_section.append(line)
    
    if current_section:
        formatted_plan.append('\n'.join(current_section))
    
    return '\n\n'.join(formatted_plan)

# API Endpoints
@app.route('/api/meal_suggestion', methods=['POST'])
def meal_suggestion_api():
    """API endpoint for meal suggestions"""
    try:
        data = request.get_json()
        meal_suggestion = suggest_meal(
            data['preferences'],
            data['dietary_restrictions'],
            data['goal'],
            data['meal_type'],
            data['cuisine'],
            data.get('health_info', {})
        )
        formatted_suggestion = format_meal_suggestion(meal_suggestion)
        return jsonify({'meal_suggestion': formatted_suggestion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nutrition_analysis', methods=['POST'])
def nutrition_analysis_api():
    """API endpoint for nutritional analysis"""
    try:
        data = request.get_json()
        nutrition_analysis = analyze_nutrition(data['meal'])
        return jsonify({'nutrition_analysis': nutrition_analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dietary_advice', methods=['POST'])
def dietary_advice_api():
    """API endpoint for dietary advice"""
    try:
        data = request.get_json()
        dietary_advice = provide_dietary_advice(
            data['advice_goal'],
            data['current_diet'],
            data.get('activity_level', ''),
            data.get('preferred_meal_types', []),
            data.get('allergies', []),
            data.get('health_info', {})
        )
        formatted_advice = format_dietary_advice(dietary_advice)
        return jsonify({'dietary_advice': formatted_advice})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meal_plan', methods=['POST'])
def meal_plan_api():
    """API endpoint for meal planning"""
    try:
        data = request.get_json()
        meal_plan = create_meal_plan(
            data['plan_preferences'],
            data.get('plan_dietary_restrictions', []),
            data['plan_goal'],
            data.get('activity_level_plan', ''),
            data.get('plan_cuisine', []),
            data.get('meal_types_plan', []),
            data.get('health_info_plan', {})
        )
        formatted_plan = format_meal_plan(meal_plan)
        return jsonify({'meal_plan': formatted_plan})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/image_analysis', methods=['POST'])
def image_analysis_api():
    """API endpoint for food image analysis"""
    try:
        data = request.get_json()
        analysis_result = analyze_food_image(data['image'])
        return jsonify({'nutritional_facts': analysis_result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Web Interface Routes
@app.route('/')
def index():
    """Route for the main application interface"""
    return render_template('index.html')

# Main Application Entry Point
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5005)