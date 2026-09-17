# =============================================================================
# Backend image: Node (Express + Socket.io) + Python (Scrapy + Playwright)
# -----------------------------------------------------------------------------
# Backend memanggil `python3 -m scrapy crawl ...` lewat child_process.spawn,
# jadi Python & Scrapy HARUS ada di dalam container yang sama dengan Node.
# =============================================================================
FROM node:20-bookworm

# --- System deps: Python, pip, dan library yang dibutuhkan Chromium/Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
      python3-venv \
      ca-certificates \
      curl \
      build-essential \
      fonts-liberation \
      libasound2 \
      libatk-bridge2.0-0 \
      libatk1.0-0 \
      libcups2 \
      libdbus-1-3 \
      libdrm2 \
      libgbm1 \
      libgtk-3-0 \
      libnspr4 \
      libnss3 \
      libx11-xcb1 \
      libxcomposite1 \
      libxdamage1 \
      libxkbcommon0 \
      libxrandr2 \
      xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Pastikan `python` menunjuk ke python3 (scrapers/index.js memakai PYTHON_EXE=python3,
# tapi beberapa toolchain Python internal juga memanggil `python`).
RUN ln -sf /usr/bin/python3 /usr/local/bin/python

# --- Python deps: Scrapy + Playwright (versi di-pin dari requirements.txt)
COPY scrapping-job/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# --- Playwright browser + OS deps (chromium headless saja, hemat ukuran)
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN python3 -m playwright install --with-deps chromium && rm -rf /var/lib/apt/lists/*

# --- Node deps (layer terpisah supaya caching efisien)
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

# --- App source
COPY . .

# Python harus dipanggil sebagai python3 di dalam container Linux.
ENV PYTHON_EXE=python3
ENV NODE_ENV=production
# Batasi heap Node supaya tidak melahap RAM host 4GB saat scraping.
ENV NODE_OPTIONS=--max-old-space-size=384

EXPOSE 3000

CMD ["node", "server.js"]
