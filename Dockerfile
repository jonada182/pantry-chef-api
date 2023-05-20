# Use an official Python runtime as a parent image
FROM python:alpine3.17

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip \
    pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port ${PORT} for Flask
EXPOSE $PORT

# Run the command to start Flask
CMD flask run -h 0.0.0.0 -p $PORT