# Use an official Python image as the base image
FROM python:3.12

# Set working directory for the backend
WORKDIR /app

# Install Node.js and dependencies for the frontend
RUN apt-get update && apt-get install -y nodejs npm

# Install frontend dependencies
COPY ./frontend/package.json ./frontend/package-lock.json /app/frontend/
WORKDIR /app/frontend
RUN npm install

# Install backend dependencies
WORKDIR /app
COPY ./backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy both frontend and backend files into the image
COPY ./frontend /app/frontend
COPY ./backend /app/backend

# Expose the required ports
EXPOSE 3000 5000

# Create a script to start both services
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run both frontend and backend services in the background
CMD ["/start.sh"]
