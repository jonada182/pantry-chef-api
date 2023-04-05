# Use an official Python runtime as a parent image
FROM python:alpine3.17

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variables
ENV FLASK_APP=api/app.py

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port ${PORT} for Flask
EXPOSE $FLASK_PORT

# Run the command to start Flask
CMD flask run -h 0.0.0.0 -p $FLASK_PORT