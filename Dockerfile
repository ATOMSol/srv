# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /vmsh

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput



# Expose port for WebSocket
EXPOSE 4002

# # Run Gunicorn (WSGI Server)
# CMD ["gunicorn", "--bind", "0.0.0.0:4002", "AppointmentServer.wsgi:application"]

# # Run Daphne (ASGI Server)
CMD ["daphne", "-b", "0.0.0.0", "-p", "4002", "AppointmentServer.asgi:application"]