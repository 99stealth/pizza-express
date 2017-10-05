FROM node

WORKDIR /pizza-express

COPY lib /pizza-express/lib
COPY test /pizza-express/test
COPY views /pizza-express/views
COPY package.json /pizza-express/package.json
COPY server.js /pizza-express/server.js

RUN npm i --production
EXPOSE 3000

CMD ["node", "server.js"]
