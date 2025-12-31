FROM node:18-alpine AS builder

WORKDIR /app

COPY TCG-API/tcg-frontend/package*.json ./
RUN npm ci

COPY TCG-API/tcg-frontend/src ./src
COPY TCG-API/tcg-frontend/public ./public

# Build with PUBLIC_URL
ARG PUBLIC_URL=/tcg
RUN npm run build -- --public-url=$PUBLIC_URL

# Nginx stage
FROM nginx:alpine

# Copy built app
COPY --from=builder /app/build /usr/share/nginx/html/

# Copy nginx config
COPY TCG-API/tcg-frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]