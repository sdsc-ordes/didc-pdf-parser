# didc-pdf-parser

> [!WARNING]
> ⚠️ This component is under development and may be unstable. Feel free to open an issue if you find any error. 

PDF-parser for blood samples used for the SwissHeart project.

This project uses Pydantic AI and LLM models to extract structured data from medical laboratory reports in PDF format. It supports two main report types: IKC and AKH blood analysis reports.

## Features

- **PDF Text Extraction**: Convert PDF reports to structured data
- **Multiple Report Types**: Support for IKC and AKH laboratory formats
- **Flexible LLM Integration**: Works with local Ollama models and cloud APIs
    - We encourage to deploy a loca Ollama model provided in `/ollama/Modelfile`. This configuration of`qwen3b:14b` has been tested on a `RTX3090`.
- **Structured Output**: Validates and outputs JSON data matching Pydantic schemas
- **CLI Interface**: Easy-to-use command-line tool

## Usage

### Docker Deployment

The easier way to deploy the tool is via docker. You will need to create a data volume where to place the pdfs to parse. 

#### Build the container:

```bash
docker build -t didc-pdf-parser .
```

#### Run with GPU support:

```bash
docker run -it --entrypoint bash --gpus all -v /path/to/data:/app/data --env-file .env didc-pdf-parser
```

#### Run CPU only:

```bash
docker run -it --entrypoint bash -v /path/to/data:/app --env-file .env didc-pdf-parser
```

### Command Line Interface

#### Basic Usage

Please see the section below to pull or create Ollama models. We tested the tool with the model available in `ollama/Modelfile`.

```bash
# IKC report with local Ollama
python didc-pdf-parser/main.py /path/to/report.pdf -a IKC -m "qwen3-14b-32k" -u "http://localhost:11434/v1" --save-txt --verbose

# AKH report with local Ollama
python didc-pdf-parser/main.py /path/to/report.pdf -a AKH -m "qwen3-14b-32k" -u "http://localhost:11434/v1" --save-txt --verbose
```

#### Cloud API Usage

```bash
# Using OpenRouter API
python didc-pdf-parser/main.py /path/to/report.pdf -a IKC -m "qwen/qwen3-14b" -u "https://openrouter.ai/api/v1" -k "your-api-key" --save-txt --verbose

# Using environment variables for API key
export API_KEY="your-api-key"
python didc-pdf-parser/main.py /path/to/report.pdf -a AKH -m "qwen/qwen3-14b" -u "https://openrouter.ai/api/v1" --save-txt --verbose
```

#### Batch Usage

The tool supports batch processing of multiple PDF files in a directory. Analysis types (IKC/AKH) are automatically detected from filename patterns.

```bash
# Process all PDFs in a directory with auto-detection
python main.py /path/to/pdf/directory -m "qwen3-14b-32k" -u "http://localhost:11434/v1" --save-txt --verbose

# Process directory with forced analysis type (overrides auto-detection)
python main.py /path/to/pdf/directory -a IKC -m "qwen3-14b-32k" -u "http://localhost:11434/v1"

# Process directory with custom output location
python main.py /path/to/pdf/directory -o /path/to/output -m "qwen3-14b-32k" -u "http://localhost:11434/v1"
```

**Filename Pattern Detection:**
- Files containing `IKC_` (case-insensitive) → Detected as IKC analysis
- Files containing `AKH_` (case-insensitive) → Detected as AKH analysis
- Files without patterns → Default to IKC analysis (with warning)

**Example filenames:**
- `IKC_patient_001.pdf` → IKC analysis
- `AKH_bloodwork_2024.pdf` → AKH analysis
- `regular_report.pdf` → IKC analysis (default)

**Batch Processing Features:**
- Progress bar showing processing status
- Individual file error handling (failures don't stop the batch)
- Summary statistics at completion
- Automatic output file naming based on input filenames


### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--analysis-type` | `-a` | Report type: IKC or AKH | IKC |
| `--output-dir` | `-o` | Output directory for generated files | PDF directory |
| `--save-txt` | `-t` | Save intermediate raw text file | False |
| `--verbose` | `-v` | Enable verbose logging | False |
| `--model-name` | `-m` | LLM model name | From env: MODEL_NAME |
| `--base-url` | `-u` | Base URL for LLM API | From env: BASE_URL |
| `--api-key` | `-k` | API key for LLM service | From env: API_KEY |

### Environment Variables

Create a `.env` file in the project root:

```bash
MODEL_NAME=qwen3:14b-q8_0
BASE_URL=http://localhost:11434/v1
API_KEY=your-api-key-if-needed
```

### Setting Up Local Models with Ollama

1. **Install Ollama**:
   ``` bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Download and serve models**:
   ``` bash
   # Create model
   ollama create -f ollama/Modelfile qwen3-14b-32k
   
   # Start Ollama server
   ollama serve
   ```

3. **Verify setup**:
   ```bash
   # Check available models
   curl http://localhost:11434/v1/api/tags
   
   # Test model
   curl http://localhost:11434/v1/api/generate -d '{
     "model": "qwen2.5:14b",
     "prompt": "Hello, world!"
   }'
   ```

4. **Use the model with the model we just created**

    ```bash
    python main.py /path/to/report.pdf -a IKC -m "qwen3:14b-q8_0" -u "http://localhost:11434/v1" --save-txt --verbose
    ```

### Supported Report Types

The data model can be found in `didc-pdf-parser/models.py`.

#### IKC Reports

- Electrolyte and Water Balance
- Kidney Function
- Proteins
- Enzymes
- Inflammation Markers
- Heart and Muscle
- Diabetes and Energy Metabolism
- Lipid and Arteriosclerosis
- Iron Metabolism
- Vitamins
- Thyroid Function
- Sexual Hormones

#### AKH Reports

- Hematological Examinations
  - Blood Status
  - Blood Count (Absolute/Relative)
- Hemostasis Examinations
  - Coagulation Factors
 
## Contributing

SOON. 

## Acknowledgements and Funding
The development of the DIDC PDF Parser is being funded by the Personalized Health and Related Technologies (PHRT), the Eidgenössische Technische Hochschule Zürich (ETH Zürich), and the Swiss Data Science Center (SDSC). 


## Copyright
Copyright © 2025 Swiss Data Science Center (SDSC), www.datascience.ch. All rights reserved. The SDSC is jointly established and legally represented by the École Polytechnique Fédérale de Lausanne (EPFL) and the Eidgenössische Technische Hochschule Zürich (ETH Zürich). This copyright encompasses all materials, software, documentation, and other content created and developed by the SDSC in the context of the Swiss Heart project.
