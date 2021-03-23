FROM python:3.7-buster

RUN mkdir -p /opt/app
COPY . /opt/app


#ENV PATH="/scripts:${PATH}"
WORKDIR /opt/app
#RUN chmod +x /scripts/*
RUN mkdir -p /opt/app/probetspp/static
#RUN useradd -ms /bin/bash user
#RUN chown -R user:user /opt/app/probetspp/static
#RUN chmod -R 755 /opt/app/probetspp/static
RUN pip install -r /opt/app/requirements/production.txt
#cd USER user

RUN mkdir -p /tmp/probetspp/static
RUN chmod -R 775 /tmp/probetspp/static

ENV ALLOWED_HOSTS='*'
CMD ["python", "probetspp/manage.py", "collectstatic", "--noinput", "--settings=probetspp.settings.production"]
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "probetspp", "probetspp.wsgi:application"]