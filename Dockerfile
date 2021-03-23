FROM python:3.7-slim-buster

LABEL maintainer="kenneth.kabiru@dej-technology.de"
LABEL description="Python 3 service for supplier qualification"

COPY ./requirements.txt ./