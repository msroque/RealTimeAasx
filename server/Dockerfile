FROM python:3.12-slim
WORKDIR /app
COPY OpcUaServer.py .
RUN pip install basyx-python-sdk
RUN pip install opcua
RUN pip install cryptography
RUN pip install docker
EXPOSE 4840
CMD ["python", "OpcUaServer.py"]