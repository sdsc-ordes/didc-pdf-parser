# didc-pdf-parser
PDF-parser for blood samples in the DIDC project

This project make use of the 

## Use

### Use as a cli tool

``` bash
python main.py /app/data/IKC_3725689.pdf -o /app/data -m "qwen3:14b-q8_0" -u "http://100.85.0.121:11434/v1" --save-txt --verbose
```



``` bash
python main.py /app/data/IKC_3725689.pdf -o /app/data -m "qwen/qwen3-14b" -u "https://openrouter.ai/api/v1"  --save-txt --verbose
```



## Development

Pydantic doesn't provide compatibility with HF models. You need first to deploy them using Ollama.

``` bash
ollama create -f Modelfile qwen3-14b-32k

ollama serve
```

0.0.0.0:11434
Verify the model is running with `curl http://localhost:11434/api/tags`.

``` bash
docker build -t didc-pdf-parser . 
```

With GPU:

``` bash
docker run -it --entrypoint bash --gpus all -v .:/app --env-file .env didc-pdf-parser 
```

``` powershell
docker run -it --entrypoint bash --gpus all -v ${pwd}:/app --env-file .env didc-pdf-parser 
```

Only CPU:

``` bash
docker run -it --entrypoint bash -v .:/app --env-file .env didc-pdf-parser 
```

``` powershell
docker run -it --entrypoint bash -v ${pwd}:/app --env-file .env didc-pdf-parser 

```

## Deploying the Model in local with Ollama

``` bash

```