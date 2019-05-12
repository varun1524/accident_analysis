#FROM python:3.7.1
#
#
#COPY . /app
#WORKDIR /app
#
#RUN cat /app/requirements.txt
#
#RUN pip install -r /app/requirements.txt
#
#RUN pip list
#
#ENTRYPOINT ["python", "/app/app.py"]
#
#EXPOSE 5001

FROM python:3

COPY . /

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "app.py" ]

EXPOSE 5000

