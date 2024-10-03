from flask import Flask, request, jsonify, after_this_request, render_template
from flask_cors import CORS
import os
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    print('home')
    rendered = render_template('index.html')
    return rendered


@app.route('/test', methods=['POST'])
def test():
    # Get user input from the request
    data = request.json
    user_input = data.get('input', '')
    
    # Prepare JSON input for Gemma
    gemma_input = {
        "instances": [{
            "prompt": user_input,
            "max_tokens": 1000
        }]
    }

    # Write the input to gemma-input-hello.json
    with open('gemma-input.json', 'w') as input_file:
        json.dump(gemma_input, input_file)
    
    # Run aroundmongolia.sh
    try:
        subprocess.run(['bash', 'aroundmongolia.sh'], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'response': 'Error running the model'}), 500

    # Read the response from gemma-output-hello.json
    try:
        with open('gemma-output.json', 'r') as output_file:
            gemma_output_string = output_file.read()

        # Debugging: Print the raw content for verification
        print("Raw JSON content:", gemma_output_string)

        # Parse the JSON string correctly
        gemma_output = json.loads(gemma_output_string)

        # Extract the first prediction text from the parsed JSON
        full_prediction_text = gemma_output.get('predictions', ['No response'])[0]
        
        # Find and extract content after "Output:" in the string
        output_index = full_prediction_text.find("Output:")
        if output_index != -1:
            response_text = full_prediction_text[output_index + len("Output:"):].strip()
        else:
            response_text = full_prediction_text

    except FileNotFoundError:
        print("Error: gemma-output-hello.json file not found.")
        response_text = 'Error: Output file not found.'

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        response_text = 'Error: Invalid JSON format in output file.'

    except Exception as e:
        # Catch all other exceptions
        print(f"Unexpected error: {e}")
        response_text = 'Error: An unexpected error occurred.'

    # Return the response to the client
    return jsonify({'response': response_text})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) #Choose your preferred portt