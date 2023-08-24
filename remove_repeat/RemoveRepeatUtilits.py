from Clickhouse_handle import AlreadyLinks


def RemoveRepeatById(info):
    x = AlreadyLinks()
    already_urls = x.GetLinksById(info["id"])
    input_info = info["payload"]
    urls=input_info.split("|||")
    input_urls=[]
    for i in urls:
        if i is not None:
            if i!="" and i!=" ":
                input_urls.append(i)
    output_urls = list(set(input_urls) - set(already_urls))
    return output_urls


def AddUrlsInDatabase(urls, id):
    x = AlreadyLinks()
    x.AddUrls(urls, id)
    pass
