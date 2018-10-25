FROM python:3

RUN mkdir /app
ADD bergenbysykkelsdk.py /app
ADD oslobysykkelsdk.py /app
ADD trondheimbysykkelsdk.py /app
ADD bysykkel.py /app
ADD sample.py /app
WORKDIR /app
RUN pip install cognite-sdk
CMD ["python", "sample.py"]