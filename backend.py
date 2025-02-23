from fastapi import FastAPI, File, UploadFile
import requests
import io
from PIL import Image
from google.cloud import vision
from ultralytics import YOLO

app = FastAPI()

# Load YOLO model (download the weights if needed)
model = YOLO("yolov8n.pt")

# USDA API Credentials (Replace with your own)
USDA_API_KEY = "GPbednp3OWf2B4YNQ4XIYnpZK6cUo6hKIvz3GTBQ"

# Initialize Google Vision Client
vision_client = vision.ImageAnnotatorClient()

@app.get("/")
def home():
    return {"message": "AI Calorie Counter Backend is Running!"}

@app.post("/analyze")
async def analyze_food(file: UploadFile = File(...)):
    image_bytes = await file.read()

    # Detect food using Google Vision API
    detected_food = detect_food_google_vision(image_bytes)

    # If Google Vision fails, fallback to YOLO
    if not detected_food:
        detected_food = detect_food_yolo(image_bytes)

    # Fetch nutrition data from USDA API
    nutrition_data = get_nutrition_data(detected_food)

    return {
        "food_name": detected_food,
        "nutrition": nutrition_data
    }

def detect_food_google_vision(image_bytes):
    """Detects food name using Google Vision API"""
    image = vision.Image(content=image_bytes)
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations

    # Extract most relevant food label
    for label in labels:
        if "food" in label.description.lower():
            return label.description.lower()
    return None

def detect_food_yolo(image_bytes):
    """Detects food using YOLO model"""
    image = Image.open(io.BytesIO(image_bytes))
    results = model(image)
    
    for result in results:
        for label in result.names.values():
            return label.lower()  # Return first detected object
    return "unknown food"

def get_nutrition_data(food_name):
    """Fetches nutrition data from USDA API"""
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={USDA_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "foods" in data and len(data["foods"]) > 0:
            nutrients = data["foods"][0]["foodNutrients"]
            return {
                "calories": next((n["value"] for n in nutrients if n["nutrientName"] == "Energy"), "N/A"),
                "protein": next((n["value"] for n in nutrients if n["nutrientName"] == "Protein"), "N/A"),
                "carbs": next((n["value"] for n in nutrients if n["nutrientName"] == "Carbohydrate, by difference"), "N/A"),
                "fat": next((n["value"] for n in nutrients if n["nutrientName"] == "Total lipid (fat)"), "N/A")
            }
    return None