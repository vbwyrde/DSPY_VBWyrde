from flask import Flask, request, jsonify
import traceback
import sys
import dspy
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
 
API_KEY = os.getenv("API_KEY")

# ------------------------------------------
# mixtral-8x22b-instruct    stop: /n/n
# llama-v3-70b-instruct     stop: Eot_id
# ------------------------------------------

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Hello, world!'}), 200

import fireworks.client
from fireworks.client.image import ImageInference, Answer

import io
import base64
from PIL import Image

@app.route('/GetImage', methods=['POST'])
def GetImage():
    fireworks.client.api_key = API_KEY
    inference_client = ImageInference(model="SSD-1B")
    
    print("Executing the /GetImage endpoint")
    try:
        data = request.get_json()
        print("Request data:", data)    
        description = data['description']
   
        # Generate an image using the text_to_image method
        answer : Answer = inference_client.text_to_image(
            prompt=description,
            cfg_scale=7,
            height=1024,
            width=1024,
            sampler=None,
            steps=30,
            seed=1,
            safety_check=False,
            output_image_format="JPG",
            # Add additional parameters here
        )
        
        if answer.image is None:
            raise RuntimeError(f"No return image, {answer.finish_reason}")
        else:
            # Convert the image to a base64-encoded string
            buffered = io.BytesIO()
            answer.image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            return jsonify({'image': img_str})
    except Exception as e:
        print("Error in /GetImage endpoint:", e)
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
    
@app.route('/execute', methods=['POST'])
def execute():
    print("Executing the /execute endpoint")
    data = request.get_json()
    print("Request data:", data)    
    data = request.get_json()
 
    context = data['context']
    information = data['information']
    model = "accounts/fireworks/models/" + data['model']
    temperature = data['temperature']
    stop = data['stop']
    max_tokens = data['max_tokens']
    print("Model parameters:")
    print("  model:", model)
    print("  temperature:", temperature)
    print("  stop:", stop)
    print("  max_tokens:", max_tokens)
   
    try:
        MyLM = dspy.OpenAI(
            api_base = "https://api.fireworks.ai/inference/v1/",
            api_key = API_KEY,
            model = model,
            temperature = temperature,            
            stop = stop,
            max_tokens = max_tokens,
        )
        
        dspy.settings.configure(lm=MyLM, timeout=30)
        print("Model is loaded...")
        
        Pred = dspy.Predict("context, information -> description")
        result = Pred(context=context, information=information)
        print("Prediction result:")
        print("  description:", result.description)
        return jsonify({'description': result.description})

    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({'error': str(e), 'traceback': tb}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
