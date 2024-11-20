# Use the official Python 3.10 image as the base
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install tkinter system package
RUN apt update && apt install -y python3-tk

# Copy requirements file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Verify installations
RUN python --version
RUN pip --version

# Expose port 8080 for Tkinter GUI (if needed)
EXPOSE 8080

# Copy application code
COPY . .

# Run command when container launches
CMD ["python", "fc.py"]