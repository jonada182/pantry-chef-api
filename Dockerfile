# Use an official Python runtime as a parent image
FROM python:alpine3.17

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set the FLASK_APP environment variable
ENV FLASK_APP=api/app.py

# Expose port 5000 for Flask
EXPOSE 5000

# Run the command to start Flask
CMD ["flask", "run", "--host=0.0.0.0"]
