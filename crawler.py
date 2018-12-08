import sys
import oauth2 as oauth
import urlparse
from plurk_oauth import PlurkAPI
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def time_formating(timestamp):
    month = timestamp[8:11]
    month_no = 0
    if month == "Jan":
       month_no = 1
    if month == "Feb":
       month_no = 2
    if month == "Mar":
       month_no = 3
    if month == "Apr":
       month_no = 4
    if month == "May":
       month_no = 5
    if month == "Jun":
       month_no = 6
    if month == "Jul":
       month_no = 7
    if month == "Aug":
       month_no = 8
    if month == "Sep":
       month_no = 9
    if month == "Oct":
       month_no = 10
    if month == "Nov":
       month_no = 11
    if month == "Dec":
       month_no = 12
    return timestamp[12:16]+"-"+str(month_no)+"-"+timestamp[5:7]+"T"+timestamp[17:25]

OAUTH_REQUEST_TOKEN = "https://www.plurk.com/OAuth/request_token"
OAUTH_kCCESS_TOKEN = "https://www.plurk.com/OAuth/access_token"
key = "TYt8Fv77oT5p"
secret = "3lzEavllllxZokBVgaEoBtcJfgZXaG3p"
token = "5Lacy8zM8F3k"
token_secret = "c8UjUr20XuandOzp5gIXMV1AGfc9mPsx" 

plurk = PlurkAPI(key, secret)
plurk.authorize(token, token_secret)



my_Profile = plurk.callAPI("/APP/Profile/getPublicProfile", options={"user_id": sys.argv[1]})
my_id = my_Profile["user_info"]["id"]
my_friends_id = plurk.callAPI("/APP/FriendsFans/getFriendsByOffset", options={"user_id": my_id, "limit": str(sys.argv[2])})
my_friends_id = [(i["id"], i["nick_name"]) for i in my_friends_id]
friends_id_list = [(my_id, sys.argv[1])]
for i in my_friends_id:
    friend_id = plurk.callAPI("/APP/FriendsFans/getFriendsByOffset", options={"user_id": i[0], "limit": str(sys.argv[2])})
    friend_id = [(j["id"], j["nick_name"]) for j in friend_id]
    for j in friend_id:
        friends_id_list.append(j)
for i in friends_id_list:
    all_plurks = ""
    #i[0] = my_id
    #i[1] = sys_argv[1]
    try:
        about = plurk.callAPI("/APP/Profile/getPublicProfile", options={"user_id": i[0]})["user_info"]["about"]
        friends_about_list[i[0]] = about
    except:
        pass
    last_t = "2030-1-1T05:08:44"

    for j in range(int(sys.argv[2])):
        plurks = plurk.callAPI("/APP/Timeline/getPublicPlurks", options={"user_id": i[0], "offset": last_t})["plurks"]
        for k in plurks:
            all_plurks += k["content"]
            all_plurks += "\n"
            comment = plurk.callAPI("/APP/Responses/get", options={"plurk_id": k["plurk_id"]})
            try:
                for l in comment["responses"]:
                    if l["user_id"] == i[0]:
                        all_plurks += l["content"]
                        all_plurks += "\n"
            except:
                pass
            last_t = time_formating(k["posted"])
    with open(i[1]+"_about.txt", "w") as f:
        f.write(strip_tags(about).encode("utf-8"))
    with open(i[1]+"_content.txt", "w") as f:
        f.write(strip_tags(all_plurks).encode("utf-8"))
