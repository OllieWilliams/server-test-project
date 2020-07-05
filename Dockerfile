FROM python:3
ADD . /app
WORKDIR /app
RUN pip install requirements.txt
CMD ["python", "src/main.py"]
