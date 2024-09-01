# Set the python version as a build-time argument
# with Python 3.12 as the default
# ARG PYTHON_VERSION=3.12-slim-bullseye
# FROM python:${PYTHON_VERSION}
FROM tensorflow/tensorflow:latest

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    netcat \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code
COPY ./requirements.txt /code/backend/requirements.txt
# Copy the requirements file into the container
# COPY ./requirements.txt /tmp/requirements.txt

# copy the project code into the container's working directory
COPY ./backend /code/backend

# Install the Python project requirements
RUN pip install -r /code/backend/requirements.txt

ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# database isn't available during build
# run any other commands that do not need the database
# such as:
# RUN python manage.py vendor_pull
# RUN python manage.py collectstatic --noinput
#whitenoise

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


# make the bash script executable
# RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV CUDA_VISIBLE_DEVICES=-1
ENV TF_CPP_MIN_LOG_LEVEL=2
WORKDIR /code/backend
# Run the Django project via the runtime script
# when the container starts
ARG PORT=8000
ENV PORT=${PORT}
CMD ["/entrypoint.sh"] 
