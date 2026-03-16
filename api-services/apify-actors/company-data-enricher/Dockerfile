FROM apify/actor-node:20

COPY package*.json ./
RUN npm install --omit=dev --prefer-offline
COPY . ./
CMD npm start
