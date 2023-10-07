FROM node:18-alpine

WORKDIR /
# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json .

# install bash to attch
RUN apk update && apk add bash

RUN apk update && apk add curl

# install project dependencies
RUN npm install

ENV PATH="$PATH:/node_modules/.bin"

# make the 'app' folder the current working directory
WORKDIR /app
