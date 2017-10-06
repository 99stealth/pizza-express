FROM node

WORKDIR /pizza-express

COPY lib /pizza-express/lib
COPY test /pizza-express/test
COPY views /pizza-express/views
COPY package.json /pizza-express/package.json
COPY server.js /pizza-express/server.js
COPY docker-entrypoint.sh /pizza-express/docker-entrypoint.sh
RUN chmod +x /pizza-express/docker-entrypoint.sh
RUN sed -ie s/127.0.0.1/redis/g /pizza-express/server.js

#RUN npm i --production
EXPOSE 3000

ENTRYPOINT ["/pizza-express/docker-entrypoint.sh"]
#CMD ["node", "server.js"]
