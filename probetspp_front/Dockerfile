FROM node:15.12.0

RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN chmod +x /app/entrypoint.sh
#RUN yarn
#RUN yarn build
CMD ["sh", "entrypoint.sh"]