#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 2017年3月15日

@author: debo.zhang
@version: 0.1
'''
import urllib2
import json


class DingTalk(object):
    """dingtalk sender class"""
    
    def __init__(self,token):
        self.__token__ = token
    
    def __netsender(self,datas):
        post_data = json.dumps(datas).encode('utf-8')
        req = urllib2.Request(self.__token__,data=post_data,
                                     headers={'content-type': 'application/json'})
        opener = urllib2.urlopen(req)
        return opener.read().decode("utf-8")
        
    def senderMarkdown(self,title,markdown):
        """
        sender markdown text to dingtalk group
        title: message title
        markdown: markdown format message
        example:
            --markdown "#### 杭州天气
                                > 9度，西北风1级，空气良89，相对温度73%
                                > ![screenshot](http://image.jpg)
                                > ###### 10点20分发布 [天气](http://www.thinkpage.cn/)"
            --title "杭州天气"
        """
        datas = {
                "msgtype": "markdown",
                "markdown": {
                             "title":title,
                             "text":markdown
                            }
             }
        return self.__netsender(datas)
    
    def senderText(self,text):
        """
        sender textpain text to dingtalk group
        text: textpain text
        example:
            --text "我就是我,是不一样的烟火"
        """
        datas = {
                "msgtype":"text",
                "text": {
                             "content":text
                            }
             }
        return self.__netsender(datas)
        
    def senderLink(self,title,text,messageUrl,picUrl):
        """
        send hyperlink message to dingtalk group
        example:
            --title "时代的火车向前开"
            --text  "这个即将发布的新版本，创始人陈航（花名“无招”）称它为“红树林”。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是“红树林”？"
            --messageUrl  "https://mp.weixin.qq.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
            --picUrl "http://www.baidu.com/example.png"
        """
        datas = {
                "msgtype":"link",
                "link": {
                             "title":title,
                             "text":text,
                             "picUrl":picUrl,
                             "messageUrl":messageUrl
                            }
             }
        return self.__netsender(datas)

if __name__ == "__main__":
    dingtalk = DingTalk("https://oapi.dingtalk.com/robot/send?access_token=74eef3052878a2a5f9150a2438dd677ebdb39484593fb39263ea7177878e695d")
    print dingtalk.senderMarkdown("图片测试", " ![screen](http://img.guopan.cn/2017-03-17/1489731921134.jpg)")