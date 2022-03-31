FROM --platform=linux/amd64 python:3.9.7-slim

COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip3 install --upgrade pip &&  \
    /opt/venv/bin/pip3 install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]