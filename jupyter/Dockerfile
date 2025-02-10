# Use the latest stable Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app
COPY . /app

# Install system dependencies and clean up after
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    tini python3-dev build-essential libatlas-base-dev \
    gfortran liblapack-dev && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install necessary Python packages
RUN pip install --no-cache-dir --upgrade pip setuptools cython && \
    pip install --no-cache-dir numpy prophet jupyter jupyterlab plotly \
    pyppeteer requests pandas argparse

# Set Entrypoint with Tini for process handling
ENTRYPOINT ["tini", "--"]

# Expose Jupyter Lab port
EXPOSE 8888

# Default command to run Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]
