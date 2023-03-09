# Start from python:3.8-alpine base image
FROM python:3.8-alpine

# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
RUN apk update && apk upgrade && \
    apk add --no-cache libressl-dev openssl curl bash git openssh && \
    apk add make automake gcc g++ subversion python3-dev

# install Rust (dependency to compile llama-index library)
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Make dir app
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt

# Install python libraries 
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080