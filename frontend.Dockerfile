FROM node:18-alpine AS builder

WORKDIR /app

COPY TCG-API/tcg-frontend/package*.json ./
RUN npm install --no-optional

COPY TCG-API/tcg-frontend/public ./public
COPY TCG-API/tcg-frontend/src ./src

# DO NOT set PUBLIC_URL - let Caddy handle path stripping
# Files will be served from /static/... not /tcg/static/...

RUN npm run build

# Nginx
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html/
COPY TCG-API/tcg-frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]