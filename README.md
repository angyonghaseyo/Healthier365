# Nutri365 - SG AI Meal Planner (Healthy365 Extension)

Nutri365 is an intelligent meal planning extension of the Healthy365 app, designed to promote healthier eating habits with the help of advanced AI technology. This AI-powered solution offers personalized meal suggestions, nutritional analysis, dietary advice, and customizable meal plans tailored to individual health goals, preferences, and dietary restrictions. Nutri365 is not just about food, it's about creating a balanced, healthy way of living that supports long-term well-being, perfectly complementing the Healthy365 app ecosystem.

## Project Overview

Nutri365, a 24/25 Sem 1 SMU IS215 Project by DBTT Group 2, is designed to revolutionize daily nutrition and promote a healthier lifestyle through AI-powered meal planning. This project aims to provide personalized meal suggestions, in-depth nutritional insights, and tailored dietary advice, making healthy eating accessible and convenient for everyone. 

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Contributing](#contributing)

## Getting Started

### Prerequisites

Before you start, make sure you have the following installed:

- [Python](https://www.python.org/downloads/) (version x.x or higher)
- [Pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)

### Installation

```bash
# Clone the repository
git clone https://github.com/bransome/ClientClutch](https://github.com/bransometan/DBTT_AIMealPlanner.git
cd DBTT_AIMealPlanner

# Install dependencies
pip install -r requirements.txt
```
### Setting up the .env file
1) Create a .env file in the root of your project.
2) Add the following configurations to the .env file:
```bash
# Example .env file
# API_KEY: A secret key for securing your application. The secret key can be obtained from https://platform.openai.com/api-keys.
API_KEY=your_secret_key
```
3) Replace your_secret_key with appropriate values.

Note: Make sure to add .env to your .gitignore file to avoid pushing sensitive information to your repository.

## Usage
To run the application locally:

```bash
python app.py
Visit http://localhost:3000 in your browser.
```

## Tech Stack
Python with Flask

## Features
- AI-Powered Meal Suggestions: Generate personalized meal recommendations based on user preferences, dietary restrictions, and health goals using advanced AI algorithms.
- Nutritional Analysis & Tracking: Provide real-time nutritional breakdowns and track daily intake, helping users maintain balanced diets and monitor nutrient consumption.
- AI-Based Dietary Advice: Offer tailored dietary guidance to users based on their current eating habits and health goals, fostering sustainable lifestyle changes.
- Personalized Meal Plans: Create customizable meal plans for users, offering weekly or monthly plans that adapt to their specific health objectives and preferences.

## Contributing
We welcome contributions! If you find a bug or have suggestions for improvement, please open an issue or submit a pull request.
