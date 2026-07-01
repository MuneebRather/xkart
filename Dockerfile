# Start from official python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Tell Docker which port our app uses
EXPOSE 5000

# Command to run the app
CMD ["python3", "app.py"]