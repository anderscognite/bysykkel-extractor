FROM python:3

RUN mkdir /app
ADD bysykkelsdk.py /app
ADD sample.py /app
WORKDIR /app
RUN pip install cognite-sdk
CMD ["python", "sample.py"]