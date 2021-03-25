FROM python:3.7-buster

RUN mkdir -p /opt/app

COPY . /opt/app

WORKDIR /opt/app
RUN chmod +x /opt/app/config/*
#RUN mkdir -p /opt/app/probetspp/static
#RUN useradd -ms /bin/bash user
#RUN chown -R user:user /opt/app/probetspp/static
#RUN chmod -R 755 /opt/app/probetspp/static
RUN pip install -r /opt/app/requirements/production.txt
#USER user

RUN mkdir -p /tmp/probetspp/static
RUN chmod -R 775 /tmp/probetspp/static
ENV ALLOWED_HOSTS='*'
CMD ["sh", "config/entrypoint.sh"]