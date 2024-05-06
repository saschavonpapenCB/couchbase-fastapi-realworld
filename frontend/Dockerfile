FROM node:alpine AS build

WORKDIR /app

COPY angular-conduit-signals/package*.json ./

RUN npm install

RUN npx ngcc --properties es2023 browser module main --first-only --create-ivy-entry-points

COPY ./angular-conduit-signals .

RUN npm run build


FROM nginx:stable

COPY ./default.conf /etc/nginx/conf.d

COPY --from=build /app/dist/angular-conduit-signals/ usr/share/nginx/html

EXPOSE 80
