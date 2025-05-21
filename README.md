# didc-pdf-parser
PDF-parser for blood samples in the DIDC project

This project make use of the 

## Use

### Use as a cli tool

### Use as a python package

### Use as an API



## Development

Pydantic doesn't provide compatibility with HF models. You need first to deploy them using Ollama. 

``` bash 
ollama run phi4:14b
```

```bash 
docker build -t didc-pdf-parser . 
```

```powershell
docker run -it --entrypoint bash --gpus all -v ${pwd}:/app --env-file .env didc-pdf-parser 
```

## Deploying the Model in local with Ollama

```bash

```