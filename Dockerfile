FROM python:3

RUN groupadd -g 1000 enzo && \
    useradd -u 1000 -g enzo enzo

RUN pip install flask

USER enzovn

WORKDIR /home/enzo/app

EXPOSE 5000:5000
