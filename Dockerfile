# Use a base Python image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (if any)
#ENV DB_HOST=db
#ENV DB_PORT=5432
#ENV DB_NAME=your_db_name
#ENV DB_USER=your_db_user
#ENV DB_PASSWORD=your_db_password

# Command to run your app
#CMD ["python", "run.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]
