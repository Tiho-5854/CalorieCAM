import streamlit as st
import requests
from PIL import Image
import io

# Title
st.title("🍽 AI Calorie Counter")
st.write("Upload a food image to get its calorie and nutrient breakdown.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Food"):
        # Convert image to bytes
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG")
        
        # Send to FastAPI backend
        files = {"file": img_bytes.getvalue()}
        response = requests.post("http://localhost:8000/analyze", files=files)

        if response.status_code == 200:
            data = response.json()
            st.subheader("🍽 Food Analysis Result")
            st.write(f"🍲 *Food Name:* {data['food_name']}")
            st.write(f"🔥 *Calories:* {data['calories']} kcal")
            st.write(f"🥩 *Protein:* {data['protein']} g")
            st.write(f"🍞 *Carbs:* {data['carbs']} g")
            st.write(f"🧈 *Fat:* {data['fat']} g")
        else:
            st.error("❌ Failed to process the image. Try again.")
