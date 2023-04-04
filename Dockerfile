# Start from python:3.8-alpine base image
FROM python:3.10-alpine

# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
RUN apk update && apk upgrade && \
    apk add --no-cache libressl-dev openssl curl bash git openssh && \
    apk add make automake gcc g++ subversion python3-dev

RUN pip3 install --upgrade pip

# Make dir app
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt

# Install python libraries 
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080