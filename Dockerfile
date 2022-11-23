FROM ubuntu:latest
WORKDIR /usr/src/app
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN python3 -m pip install --no-cache-dir requests bs4 python-telegram-bot pycryptodome
COPY *.py .token ./
CMD ["python3", "./main.py"]
