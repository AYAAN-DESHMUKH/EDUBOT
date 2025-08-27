#!/bin/bash
export MSYS_NO_PATHCONV=1

# Prompt the user for the model URL
read -p "Please enter the model URL: " model_url

# Extract the model filename from the URL
model_filename=$(basename "$model_url")

# Create a directory to store the model
mkdir -p ./model

# Download the model if it doesn't already exist
if [ ! -f "./model/$model_filename" ]; then
    echo "Downloading model..."
    curl -L -o "./model/$model_filename" "$model_url"
else
    echo "Model already exists."
fi

# Build the Docker image
echo "Building Docker image..."
docker build --no-cache -t llamafile_image .

# Run the Docker container, mounting the model directory
echo "Running Docker container..."

# For debugging
echo "Model filename: $model_filename"
echo "Current directory: $(pwd)"
echo "Running Docker container with the following command:"
echo "docker run -p 8080:8080 -v \"$(pwd)/model:/usr/src/app/model\" llamafile_image --server --host 0.0.0.0 -m \"/usr/src/app/model/$model_filename\""

docker run -p 8080:8080 \
    -v "$(pwd)/model:/usr/src/app/model" \
    llamafile_image \
    --server \
    --host 0.0.0.0 \
    -m "/usr/src/app/model/$model_filename"