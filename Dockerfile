# Use an official Python 3.11 runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pipenv
RUN pip install pipenv

# Modify the Pipfile.lock to update the torch wheel URL
RUN sed -i 's|https://download.pytorch.org/whl/cpu/torch-2.0.0%2Bcpu-cp311-cp311-win_amd64.whl|https://download.pytorch.org/whl/cpu/torch-2.0.0%2Bcpu-cp311-cp311-linux_x86_64.whl|' Pipfile.lock

# Then proceed with your existing steps
RUN pipenv install --system --deploy

# Make port 8080 available to the world outside this container
EXPOSE 8080


# Run gunicorn when the container launches
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
