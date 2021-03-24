FROM node:latest

RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN chmod +x /app/entrypoint.sh
RUN yarn
RUN yarn build
# CMD ["sh", "entrypoint.sh"]