from __future__ import print_function 
import sys, re, urlparse
import oauth2 as oauth
from plurk_oauth import PlurkAPI
from HTMLParser import HTMLParser
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-u", dest="user", default="")
parser.add_argument("-f", dest="friends_n", default=0)
parser.add_argument("-n", dest="plurks_n", default=0)
parser.add_argument("-k", dest="keyword", default="")
args = parser.parse_args()

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

def get_friends_data(friends_list):
    for i in friends_list:
        all_plurks = ""
        last_t = "2030-1-1T05:08:44"
        try:
            about = plurk.callAPI("/APP/Profile/getPublicProfile", options={"user_id": i[0]})["user_info"]["about"]
            about = strip_tags(about)
        except:
            pass
        for j in range((int(args.plurks_n)//5)+1):
            if j == int(args.plurks_n)//5: 
                limit = int(args.plurks_n)%5
            else:
                limit = 5
            plurks = plurk.callAPI("/APP/Timeline/getPublicPlurks", options={"user_id": i[0], "limit": limit, "offset": last_t})["plurks"]
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
        tmp = all_plurks
        all_plurks = strip_tags(all_plurks)
        all_plurks = re.sub("\n[A-Za-z0-9_]*:", "\n", all_plurks)
        with open(i[1]+"_about.txt", "w") as f:
            f.write(about.encode("utf-8"))
        with open(i[1]+"_content.txt", "w") as f:
            f.write(all_plurks.encode("utf-8"))
        

OAUTH_REQUEST_TOKEN = "https://www.plurk.com/OAuth/request_token"
OAUTH_kCCESS_TOKEN = "https://www.plurk.com/OAuth/access_token"
key = "TYt8Fv77oT5p"
secret = "3lzEavllllxZokBVgaEoBtcJfgZXaG3p"
token = "5Lacy8zM8F3k"
token_secret = "c8UjUr20XuandOzp5gIXMV1AGfc9mPsx" 

plurk = PlurkAPI(key, secret)
plurk.authorize(token, token_secret)

my_Profile = plurk.callAPI("/APP/Profile/getPublicProfile", options={"user_id": args.user})
my_id = my_Profile["user_info"]["id"]
friends_list = [(my_id, args.user)]

if args.user == "":
    print("GG")
    exit()

if(args.keyword == ""):
    if int(args.friends_n) == 0:
        print("GG")
        exit()
    if int(args.plurks_n) == 0:
        print("GG")
        exit()
    my_friends_id = plurk.callAPI("/APP/FriendsFans/getFriendsByOffset", options={"user_id": my_id, "limit": 100})
    my_friends_id = [(i["id"], i["nick_name"]) for i in my_friends_id]
    friends_list = [(my_id, args.user)]
    for i in my_friends_id:
        friend_id = plurk.callAPI("/APP/FriendsFans/getFriendsByOffset", options={"user_id": i[0], "limit": int(args.friends_n)})
        friend_id = [(j["id"], j["nick_name"]) for j in friend_id]
        for j in friend_id:
            friends_list.append(j)
    get_friends_data(friends_list)
else:
    if int(args.friends_n) != 0:
        print("GG")
        exit()
    if int(args.plurks_n) != 0:
        print("GG")
        exit()
    plurks = plurk.callAPI("/APP/PlurkSearch/search", options={"query": args.keyword})
    for user_id, user_info in plurks["users"].iteritems():
        friends_list.append((int(user_id), user_info["nick_name"]))
    get_friends_data(friends_list)
