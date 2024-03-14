FROM python:3.9

WORKDIR /app/

RUN apt-get update \
    && apt-get install -y \
        ffmpeg \
        libsm6 \
        libxext6 \
        gcc \
        python3-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

WORKDIR /app/transcriber_project

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
