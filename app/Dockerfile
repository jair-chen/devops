# app/Dockerfile

FROM node:18-bullseye-slim

WORKDIR /app

COPY ./ui/package*.json ./

RUN npm install -g @vue/cli &&\
    npm install --legacy-peer-deps

COPY ./ui .

RUN npm run build
