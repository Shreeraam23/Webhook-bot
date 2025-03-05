FROM node:18
     RUN apt-get update && apt-get install -y curl
     COPY . .
     RUN npm install
     RUN chmod +x sethook.sh
     CMD [ "npm", "start" ]
