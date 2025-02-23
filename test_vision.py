from google.cloud import vision

client = vision.ImageAnnotatorClient()

# Local image test
with open("test_image.png", "rb") as image_file:
    content = image_file.read()
image = vision.Image(content=content)

response = client.label_detection(image=image)
labels = response.label_annotations

print("Labels detected:")
for label in labels:
    print(label.description, label.score)

