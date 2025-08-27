# Llamafile: Simplified LLM Deployment

## Overview
Llamafile is a revolutionary tool that converts Large Language Models (LLMs) into standalone executable files. This transformation offers several significant advantages:

- **Enhanced Performance**: Achieve 30% to 500% performance improvement compared to Ollama
- **CPU-Based Inference**: Run models efficiently on CPU architecture
- **Streamlined Deployment**: Simple deployment process using this repository

## Prerequisites
- Docker (installed and running)
- Git
- Unix-based terminal (Git Bash for Windows users)

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/brainqub3/llamafile_chat.git
   ```

2. Navigate to the project directory and execute the build script:
   ```bash
   ./build_file.sh
   ```

## Usage Options

### 1. Web Interface
Access the built-in interface through your web browser:
```
http://127.0.0.1:8080
```

### 2. API Integration
Interact with the model programmatically via the API endpoint:
```
http://172.17.0.2:8080
```

For terminal-based interactions, we provide a Python script:
```bash
python chat.py
```
This script facilitates direct communication with your model through the command line.

## Additional Resources

- [Llamafile Technical Deep Dive](https://justine.lol/matmul/) - Comprehensive blog post explaining the technology
- [Official GitHub Repository](https://github.com/Mozilla-Ocho/llamafile) - Source code and documentation