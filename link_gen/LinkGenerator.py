import threading
from ProsExt import ProcessExt
from LinkGeneratorUtilits import LinkGen
from Clickhouse_handle import LinkBase
from time import sleep
from functools import partial
from threading import Thread
from RabbitHandle import RabbitBase
max_thread_in_generator=10

def thread_funktion_parser(url,UseJs,id,buf):
    parserr = LinkGen()
    links=parserr.generate_links_no_abstract(url,UseJs)
    buf["id"] = id
    buf["payload"] = links
    x = RabbitBase("link_quere")
    x.SendInfo(buf)
    print("id=", id, " успешно отправил в очередь")


def ParseNewsSections(delay_thread=2,UseJs=False):#должно парсить все сайты из базы данных однако предполагается вызов фунции ParseNewsSectionsById в for с нужными айди
    x = LinkBase()
    infos = x.get_links()

    mas_threads = []
    max_id = -1
    mas_ret_thread = []
    mass_funk = []
    for info in infos:
        if info["links"] != "":
            urls = info["links"].split("|||")
            for url in urls:
                ur = url.replace(" ", "")
                if ur.startswith("http"):
                    buf = {}
                    buf["id"] = None
                    buf["payload"] = None

                    mass_funk.append(partial(thread_funktion_parser, ur, UseJs, info["id"], buf))
                    if len(mass_funk) >= max_thread_in_generator:
                        x = ProcessExt(mass_funk, delay_thread, 50)
                        x.start()
                        x.join()
                        mass_funk.clear()
    if len(mass_funk) > 0:
        x = ProcessExt(mass_funk, delay_thread, 50)
        x.start()
        x.join()
        mass_funk.clear()

    print("Выполнено")


def ParseNewsSectionsById(id,delay_thread=2,UseJs=False):#парсит базу данных по определенной ссылке(которая айди)
    x=LinkBase()
    infos=x.get_links_by_id(id)
    mas_threads=[]
    max_id=-1
    mas_ret_thread=[]
    mass_funk=[]
    for info in infos:
        if info["links"]!="":
            urls=info["links"].split("|||")
            for url in urls:
                ur=url.replace(" ","")
                if ur.startswith("http"):
                    buf={}
                    buf["id"]=None
                    buf["payload"]=None

                    mass_funk.append(partial(thread_funktion_parser,ur,UseJs,info["id"],buf))
                    if len(mass_funk)>=max_thread_in_generator:
                        x=ProcessExt(mass_funk,delay_thread,50)
                        x.start()
                        x.join()
                        mass_funk.clear()
    if len(mass_funk)>0:
        x = ProcessExt(mass_funk, delay_thread, 50)
        x.start()
        x.join()
        mass_funk.clear()

    print("Выполнено")