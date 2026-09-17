# =============================================================================
# Frontend image: build Vue/Vite -> serve sebagai static via nginx
# Nginx di sini JUGA bertugas sebagai reverse proxy ke backend (/api, /socket.io)
# Build context = folder ./frontend, jadi nginx.conf harus ada di dalamnya.
# =============================================================================

# --- Stage 1: build
FROM node:20-bookworm-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# --- Stage 2: runtime (nginx)
FROM nginx:1.27-alpine
# Server block + reverse proxy ke backend
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Hasil build Vite
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
