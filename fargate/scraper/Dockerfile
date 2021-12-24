FROM python:3.8
WORKDIR /machine
COPY . .
RUN pip install -r requirements.txt
ADD scrap.py .
CMD ["python", "./scrap.py"]

