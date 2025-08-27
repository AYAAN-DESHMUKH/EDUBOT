#!/bin/bash
export MSYS_NO_PATHCONV=1

# List models in ./model folder
echo "Available models:"
ls ./model/

# Prompt user to enter model filename (just the name, not full URL)
read -p "Enter model filename (e.g. Llama-3.2-3B-Instruct-Q4_K_M.gguf): " model_filename

# Validate file exists
if [ ! -f "./model/$model_filename" ]; then
    echo "❌ Error: Model file './model/$model_filename' not found!"
    exit 1
fi

# Run the Docker container (reuse existing image)
echo "🚀 Starting Llamafile server..."
docker run -d \
    --name llamafile-server \
    --restart unless-stopped \
    -p 8080:8080 \
    -v "$(pwd)/model:/usr/src/app/model" \
    llamafile_image \
    --server \
    --host 0.0.0.0 \
    -m "/usr/src/app/model/$model_filename"

echo "✅ Server started! Connect your chatbot to http://localhost:8080"
echo "💡 Check logs: docker logs -f llamafile-server"
echo "🛑 Stop server: docker stop llamafile-server"