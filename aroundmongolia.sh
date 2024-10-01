ENDPOINT_ID="" #Your end point must be in here
PROJECT_ID="" #Your project id must be in here
INPUT_DATA_FILE="gemma-input-hello.json"
OUTPUT_DATA_FILE="gemma-output-hello.json"

curl \
    -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    "https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-central1/endpoints/${ENDPOINT_ID}:predict" \
    -d "@${INPUT_DATA_FILE}" | tee "$OUTPUT_DATA_FILE"

PREDICTION=$(cat "$OUTPUT_DATA_FILE")

echo -en "$PREDICTION\n"