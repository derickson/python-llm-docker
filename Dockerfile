# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt /app
RUN pip install  -r requirements.txt

# Copy the current directory contents into the container at /app
COPY *.py /app

# Expose the port the app will listen on
EXPOSE 80

VOLUME ./cache:/app/cache

# Run the command to start the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
