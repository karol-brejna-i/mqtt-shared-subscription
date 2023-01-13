FROM python:3.10

WORKDIR /code

COPY ./requirements.txt ./main.py ./log_config.py /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#COPY ./app /code/app
#COPY ./main.py /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]