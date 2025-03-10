# Base image of Python
FROM python:3.9

# Define working directory
WORKDIR /app

# Copy app files
COPY app/ app/

# Install dependencies
RUN pip install -r app/requirements.txt

# Expose app port
EXPOSE 5000

# Executes Virtual Store app
CMD ["python", "app/main.py"]
