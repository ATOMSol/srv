
# Base image
FROM python:3.11-slim-buster

# Install git
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .


# Expose the port the app runs on
EXPOSE 8000


# Run the Django development server
CMD python manage.py runserver 0.0.0.0:8000