FROM python:3.8.5

RUN mkdir /app
RUN pip install flask google-cloud-pubsub==2.0.0 gunicorn
ENV THREADS=8
COPY relay_to_pubsub.py /app
WORKDIR /app
CMD ["/bin/bash", "-c", "gunicorn -t ${THREADS} relay_to_pubsub.py app"]
