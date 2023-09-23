# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Command to run the application
CMD ["python", "./update_ip.py"]
