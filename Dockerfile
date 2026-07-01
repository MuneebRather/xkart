# Start from official python image
FROM python:3.11-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Copy Nginx config
COPY nginx.conf /etc/nginx/sites-available/default

# Start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Tell Docker that the container accepts incoming connections on port 80 
# through the Nginx web server.
EXPOSE 80

# Command to run the app
CMD ["/start.sh"]