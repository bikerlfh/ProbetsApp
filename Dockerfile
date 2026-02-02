FROM python:3.10.19-bookworm


# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm -rf /var/lib/apt/lists/*

# Install chromedriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') \
    && CHROMEDRIVER_VERSION=$(wget -qO- "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION%.*.*}") \
    && wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver*


RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/info_pages/flash
RUN mkdir -p /opt/app/datasets

COPY ./probetspp /opt/app/probetspp
COPY ./requirements /opt/app/requirements
COPY ./config /opt/app/config

WORKDIR /opt/app
RUN chmod +x /opt/app/config/*
#RUN mkdir -p /opt/app/probetspp/static
#RUN useradd -ms /bin/bash user
#RUN chown -R user:user /opt/app/probetspp/static
#RUN chmod -R 755 /opt/app/probetspp/static

ENV VIRTUAL_ENV=/usr/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install uv

RUN uv pip install -r /opt/app/requirements/production.txt
#USER user

RUN mkdir -p /tmp/probetspp/static
RUN chmod -R 775 /tmp/probetspp/static
ENV ALLOWED_HOSTS='*'
CMD ["sh", "config/entrypoint.sh"]