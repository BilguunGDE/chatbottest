ENDPOINT_ID="8525491115984420864"
PROJECT_ID="954563389883"
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