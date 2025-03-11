from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model("cnn_tb_model.keras")

def preprocess_image(img):
    img = cv2.imdecode(np.frombuffer(img.read(), np.uint8), 1)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["file"]
    img_array = preprocess_image(file)
    prediction = model.predict(img_array)[0][0]

    confidence = prediction * 100  # Convert to percentage

    if confidence < 70:
        result = "⚠️ This image may not be a chest X-ray. Please upload a valid chest X-ray."
    elif prediction > 0.5:
        result = f"⚠️ Tuberculosis Detected ({confidence:.2f}% confidence)"
    else:
        confidence = (1 - prediction) * 100  # Adjust for 'No TB' case
        result = f"✅ No Tuberculosis Detected ({confidence:.2f}% confidence)"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
