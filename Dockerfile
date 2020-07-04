FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install pip
COPY ./src /app
RUN pip install -r /requirements.txt
CMD ["python3", "src/main.py"]