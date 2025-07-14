# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Install pipx and create a virtual environment
RUN apt-get update && apt-get install -y pipx && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt


# Pre-download Docling models during build
RUN /venv/bin/python -c "from docling.document_converter import DocumentConverter; DocumentConverter()"

COPY . /src

# Use the virtual environment's Python and pip
ENV PATH="/venv/bin:$PATH"

ENTRYPOINT ["bash"]