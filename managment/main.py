from Clickhouse_handle import create_table
from RabbitHandle import RabbitBase


def create_link_base_table():
    column_names=["link_main","link_news"]
    column_types=["String","String"]
    create_table("link_base",column_names,column_types)

def create_already_parsed_links_table():
    column_names=["id_main_link", "link"]
    culumn_types=["String","String"]
    create_table("already_parsed_links",column_names,culumn_types)
    pass

def create_finished_news_table():
    column_names = ["id_main_link", "link", "title", "data_zapros", "data_news", "time_news", "text"]
    column_types = [ "String", "String","String","String","String","String","String"]
    create_table("finished_news",column_names,column_types)

    pass
def test(a):
    print(a)

if __name__=="__main__":
    print("started")
    x=RabbitBase("test")
    b={}
    b["id"]="http://asdas/"
    b["payload"]="asdadasdasd"
    print("do paket")
    x.SendInfo(b)
    print("paker is send")
    x.ListenInfo(test)
    #create_finished_news_table()
    #create_already_parsed_links_table()
    #create_link_base_table()

