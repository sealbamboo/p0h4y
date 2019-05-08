FROM python:3-onbuild

MAINTAINER Shayne Nguyen

COPY app /app
CMD ["python","server.py"]