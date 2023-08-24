from RemoveRepeatUtilits import RemoveRepeatById,AddUrlsInDatabase
from RabbitHandle import RabbitBase

def main(info):
    id=info["id"]
    try:
        unical=RemoveRepeatById(info)
        x=RabbitBase("news_quere")
        for i in unical:
            buf={}
            buf["id"]=id
            buf["payload"]=i
            try:
                x.SendInfo(buf)
            except:
                print("warning error in send info")
        try:
            AddUrlsInDatabase(unical,id)
        except:
            print("error in add unical url in database")
            print("id=",id)
            print("info=",unical)
    except:
        print("error in main remove repeat")
        print("info=",info)

def start_main():
    x = RabbitBase("link_quere")
    x.ListenInfo(main)


if __name__=="__main__":
    x=RabbitBase("link_quere")
    x.ListenInfo(main)