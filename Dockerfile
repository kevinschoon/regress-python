FROM python:3.5.1

COPY . /app

RUN pip install -r /app/requirements.txt && \
    cd /app && \
    python setup.py develop && \
    regress --init

ENTRYPOINT [ "gunicorn", "--workers=2", "-b 0.0.0.0:8000", "regress.main:app"]
