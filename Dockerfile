FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir requests bs4 python-telegram-bot
COPY *.py .token ./
CMD ["python", "./main.py"]
