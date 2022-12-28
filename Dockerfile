FROM python:3.8
WORKDIR /FlaskAPP

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "run:app", "-c", "./gunicorn.conf.py"]