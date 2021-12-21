FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir requests bs4 python-telegram-bot
COPY main.py main.py
CMD ["python", "./main.py"]
