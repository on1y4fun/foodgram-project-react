# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
COPY . ./
RUN npm install --legacy-peer-deps
RUN npm run build
CMD cp -r build result_build
