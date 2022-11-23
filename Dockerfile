FROM python:3-alpine
WORKDIR /usr/src/app
RUN apk add --no-cache gcc libc-dev
RUN python3 -m pip install --no-cache-dir requests bs4 python-telegram-bot pycryptodome
COPY *.py .token ./
CMD ["python3", "./main.py"]
