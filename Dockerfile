FROM python:3-alpine
WORKDIR /usr/src/app
RUN apk add --no-cache gcc libc-dev
RUN pip install --no-cache-dir requests==2.28.* beautifulsoup4==4.11.* python-telegram-bot==13.* pycryptodome==3.16.*
COPY *.py .token ./
CMD ["python", "main.py"]
