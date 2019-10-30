FROM python:3.7
COPY /src /binlist_api
WORKDIR /binlist_api

EXPOSE 8080

RUN pip install -r requirements.txt

CMD python binlist_api/main.py
