FROM python:3.12.4-alpine

WORKDIR /source

COPY . .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 9380

CMD python3.12 main.py
