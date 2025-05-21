FROM nvidia/cuda:12.4.1-base-ubuntu22.04 AS gpu
ARG PLATFORM
RUN echo "Using GPU image"


#COPY --from=ghcr.io/astral-sh/uv:0.5.8 /uv /uvx /bin/

RUN apt-get update && \
   apt-get install -y  --no-install-recommends  \
      nano curl

RUN apt-get install -y python3.11 python3.11-venv python3-pip

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --set python3 /usr/bin/python3.11 && \
    update-alternatives --set python /usr/bin/python3.11

RUN pip install --upgrade -r requirements.txt

# Dep
RUN apt-get update && apt-get install poppler-utils ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools

# Define the build argument with a default value of an empty string (optional)

#RUN uv sync --frozen ${UV_ARGUMENTS}

# make uv's python the default python for the image
#ENV PATH="/app/.venv/bin:$PATH"

#ENV DASK_DISTRIBUTED__WORKER__DAEMON=False

#ENTRYPOINT ["/bin/bash"]
#RUN python /open-pulse-graph-classifier/main.py
