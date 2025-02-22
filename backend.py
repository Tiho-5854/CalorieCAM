from fastapi import FastAPI, File, UploadFile
import requests
from PIL import Image
import io

app = FastAPI()

# Your Edamam API credentials (replace with your own keys)
EDAMAM_APP_ID = "your_app_id"
EDAMAM_APP_KEY = "your_app_key"

@app.get("/")
def home():
    return {"message": "AI Calorie Counter Backend is Running!"}

@app.post("/analyze")
async def analyze_food(file: UploadFile = File(...)):
    # Convert image file to bytes
    image_bytes = await file.read()
    
    # Send image to Google Vision API for food detection (implement this later)
    detected_food = "pizza"  # Placeholder for now

    # Call Edamam API to get nutrition info
    nutrition_data = get_nutrition_data(detected_food)

    if nutrition_data:
        return nutrition_data
    else:
        return {"error": "Could not fetch nutrition data"}

# Function to get nutrition data from Edamam API
def get_nutrition_data(food_name):
    url = f"https://api.edamam.com/api/food-database/v2/parser?ingr={food_name}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        nutrients = data["hints"][0]["food"]["nutrients"]

        return {
            "food_name": food_name,
            "calories": nutrients.get("ENERC_KCAL", "N/A"),
            "protein": nutrients.get("PROCNT", "N/A"),
            "carbs": nutrients.get("CHOCDF", "N/A"),
            "fat": nutrients.get("FAT", "N/A")
        }
    else:
        return None
