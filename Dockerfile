FROM python:3.8.5

RUN mkdir /app
RUN pip install flask google-cloud-pubsub==2.0.0 gunicorn
ENV WORKERS=8
ENV PORT=8000
COPY relay_to_pubsub.py /app
WORKDIR /app
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:${PORT} -w ${WORKERS} relay_to_pubsub:app"]
