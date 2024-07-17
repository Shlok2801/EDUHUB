FROM python:3.8-slim

WORKDIR /EDUHUB

COPY ./website/ /EDUHUB/website/
COPY ./requirements.txt /EDUHUB/
COPY ./main.py /EDUHUB/
COPY ./instance/ /EDUHUB/instance/
COPY ./.env /EDUHUB/

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "main:app", "-b", "0.0.0.0:5000", "-w", "4"]
