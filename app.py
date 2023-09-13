from flask import Flask, request, jsonify
from flask_cors import CORS  # <- Add this import
import openai
import json
import io
import os
app = Flask(__name__)
CORS(app)  # <- Add this to enable CORS for all routes

# Ideally, store this securely using environment variables
OPENAI_API_KEY = OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


@app.route('/divide/', methods=['POST'])
def divide_text():
    data = request.json
    print(data)
    datas = data['fullstory']
    divided_text = datas + \
        f"Divide this story into {data['number']} substories. Do not include the title of each substory, also do not include any label or header that indicate the order of the substory. Only the substory should be a completed paragraph. The response should be a JSON string that stands for one key-value pair; the key is 'scene', the value is an array containing the substories."
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": divided_text}
            ]
        )
        response_message = response.choices[0].message['content']
        scene_content = json.loads(response_message)['scene']
        return jsonify({'scene': scene_content})

    except Exception as e:
        return jsonify({'message': 'Error occurred. Please try again.'}), 500


if __name__ == '__main__':
    app.run()
