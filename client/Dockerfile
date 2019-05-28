FROM node:8.16.0-alpine as angular
RUN npm install -g @angular/cli
WORKDIR /work
COPY . /work
RUN npm i
RUN ng build -c docker

FROM nginx:latest
COPY --from=angular /work/dist/client/ /usr/share/nginx/html
