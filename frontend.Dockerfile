FROM node:18-alpine AS builder

WORKDIR /app

COPY TCG-API/tcg-frontend/package*.json ./
RUN npm install

ARG PUBLIC_URL=/
COPY TCG-API/tcg-frontend/ .
RUN npm run build -- --public-url=$PUBLIC_URL

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

RUN echo 'server { listen 80; root /usr/share/nginx/html; index index.html; location / { try_files $uri $uri/ /index.html; } location /api/ { proxy_pass http://api:8000/api/; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto $scheme; } }' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
