# docker run -it --rm -p 8557:8557 -v $PWD/data:/mmqweb/data mmqweb
FROM python:2-alpine

RUN mkdir -p /mmqweb
WORKDIR /mmqweb

COPY requirements.txt /mmqweb
RUN pip install --no-cache-dir -r requirements.txt

COPY . /mmqweb/

ENV PRODUCTION TRUE
EXPOSE 8557
VOLUME /mmqweb/data
CMD ["gunicorn", "mmqweb.wsgi", "-c", "gunicorn_conf.py"]
