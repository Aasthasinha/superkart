# Base Image
FROM python:3.10-slim
# Set working directory
WORKDIR /app
#Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
#Copy requirement file and install depandencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Code Code and Model
COPY app.py .
COPY superkart_model.joblib .

#Expose the API
EXPOSE 7860

#Run the application with 3 workers and binds the server to port 7860
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:7860", "app:superkart_api"]

