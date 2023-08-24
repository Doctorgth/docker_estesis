FROM python:3
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD Clickhouse_handle.py app/
ADD RemoveRepeatMain.py app/
ADD RemoveRepeatUtilits.py app/
ADD ProsExt.py app/
ADD proxy.py app/
ADD RabbitHandle.py app/
ADD SqlHandle.py app/
ADD proxy_list.txt app/
ADD main.py app/
CMD [ "python", "./app/main.py" ]