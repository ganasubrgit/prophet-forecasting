FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Install dependencies
RUN apt-get -y update \
    && apt-get install -y tini python3-dev apt-utils build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade setuptools cython numpy prophet jupyter jupyterlab plotly pyppeteer

# Entrypoint with Tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# CMD ["python","/app/app.py"]
EXPOSE 8888

CMD ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]