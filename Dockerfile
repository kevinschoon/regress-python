FROM python:3.5.1

COPY regress/ /app/regress/
COPY requirements.txt setup.py /app/

RUN pip install -r /app/requirements.txt && \
    cd /app && \
    python setup.py develop

ENTRYPOINT [ "gunicorn" ]
