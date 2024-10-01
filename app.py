from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# --- Google Cloud AI Platform configuration ---
ENDPOINT_ID = os.environ.get("8525491115984420864") # Get from environment variables
PROJECT_ID = os.environ.get("954563389883") # Get from environment variables
REGION = "us-central1" #Change if necessary


@app.route('/test', methods=['POST'])
def test():
    print('sug')
    return 'sug'


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        message = data.get('message')
        if not message:
            return jsonify({'error': 'No message provided'}), 400
    # error
        #Create temporary input file
        temp_input_file = "temp_input.json"
        with open(temp_input_file, 'w') as f:
            json.dump({"instances": [{"text": message}]}, f) #Adjust to your model's input format

        #Construct the curl command
        command = [
            "curl",
            "-X", "POST",
            "-H", "Authorization: Bearer $(gcloud auth print-access-token)",
            "-H", "Content-Type: application/json",
            f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}:predict",
            "-d", f"@{temp_input_file}"
        ]

        #Execute the curl command and capture output
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0:
            return jsonify({'error': process.stderr}), 500

        #Parse response from the curl command
        response_json = json.loads(process.stdout)
        prediction = response_json['predictions'][0]['text']  # Adapt to your model's output


        os.remove(temp_input_file) #Clean up temporary file
        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) #Choose your preferred port