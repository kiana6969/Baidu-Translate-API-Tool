

import requests
import random
import hashlib
import json
import time

search_history = {}

class TransLate(object):
        # 初始化
    def __init__(self, word):
        self.word = word
        # 百度API
        self.url = "https://api.fanyi.baidu.com/api/trans/vip/translate"
        # appid和密钥
        self.appid = login_appid
        self.secret_key =  login_key
        # 随机盐值
        self.salt = random.randint(32768, 65536)




        # 加密
    def make_sign(self):
        sign = self.appid + self.word + str(self.salt) + self.secret_key
        #签名
        md5 = hashlib.md5()
        md5.update(sign.encode('utf-8'))
        return md5.hexdigest()


    def get_data(self):
        # 参数
        self.params = {
            "q": self.word,
            "from": "auto",
            "to": "auto",
            "appid": self.appid,
            "salt": self.salt,
            "sign": self.make_sign()
        }
        # 请求
        try:
           response = requests.post(self.url, params=self.params,timeout=10)
           return response.content.decode('utf-8')
        except requests.exceptions.RequestException as e:
            print("连接超时",e)


    def run(self):
        response = self.get_data()
        # json操作
        try:
           str_dict_json = json.loads(response)
           if "error_code" in str_dict_json:
               print("\nAPPID或密钥错误，错误信息为",str_dict_json["error_msg"])
               print("\n请重新启动该程序以重置登录信息!\n")
               return
           result = str_dict_json["trans_result"][0]["dst"]
           print("翻译结果是:\n",result)
           search_history[time.strftime("%Y/%m/%d %H:%M:%S")] = result
           with open("history.txt", "a", encoding="utf-8") as f:
               f.write(f"{time.strftime('%Y/%m/%d %H:%M:%S')} | {user_trans} -> {result}\n")
        except Exception as e:
            print("json翻译失败，原因是",e)


if __name__ == '__main__':
    login_appid = input("请输入你的百度appid:\n")
    login_key = input("请输入密钥:\n")
    while True:
        user_input = input("使用翻译功能请输入1\n查看历史翻译请输入2\n结束此程序请输入3\n")
        if user_input == "1":
            user_trans = input("请输入需要翻译的词语或句子(支持英文和简体中文间相互翻译)：\n")
            transLator=TransLate(user_trans)
            # 合法性判断
            if   user_trans.isdigit():
                print("输入了数字，","'",user_trans,"'","不是合法词汇!\n")
            else:
            # 调用
               transLator.run()

        elif user_input == "2":
            print("历史记录:\n")
            # 遍历记录
            for k,v in search_history.items():
                print(k,v,"\n")
            print("历史记录仅包含此次运行时的记录，如需查看更早时的记录，\n请手动打开history.txt文件查看\n")
            # 结束循环
        elif user_input == "3":

            break
        else:
            print("请输入1，2，3,你输入了错误的功能代号！")
