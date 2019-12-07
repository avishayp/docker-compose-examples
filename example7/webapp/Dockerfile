FROM node:10-alpine

WORKDIR /web

COPY package.json .
RUN npm install

COPY . .

EXPOSE 9000
CMD ["npm", "start"]