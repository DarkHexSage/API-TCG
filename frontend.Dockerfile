FROM node:18-alpine AS builder

WORKDIR /app

COPY TCG-API/tcg-frontend/package*.json ./
RUN npm install --no-optional

COPY TCG-API/tcg-frontend/public ./public
COPY TCG-API/tcg-frontend/src ./src

# ⭐ ADD THIS LINE
ENV PUBLIC_URL=/tcg

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html/
COPY TCG-API/tcg-frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]