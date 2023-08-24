FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD Clickhouse_handle.py /
ADD LinkGenerator.py /
ADD LinkGeneratorUtilits.py /
ADD ProsExt.py /
ADD proxy.py /
ADD RabbitHandle.py /
ADD SqlHandle.py /
ADD proxy_list.txt /
ADD main.py /
CMD [ "python", "./main.py" ]