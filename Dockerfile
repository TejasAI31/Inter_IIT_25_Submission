
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*


COPY requirements_pathway.txt .
RUN pip install --no-cache-dir "setuptools<81" && \
    pip install --no-cache-dir -r requirements_pathway.txt

COPY . .


RUN mkdir -p /app/data

CMD ["python", "pathway_pipeline.py"]
