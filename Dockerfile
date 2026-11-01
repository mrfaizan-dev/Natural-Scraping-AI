FROM python:3.12.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    g++ \
    libgomp1 \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    xvfb \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install playwright==1.62.0
RUN playwright install chromium --with-deps


COPY requirements.txt .
RUN pip install --default-timeout=1000 --prefer-binary -r requirements.txt

COPY . .

EXPOSE 8800

CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8800"]
