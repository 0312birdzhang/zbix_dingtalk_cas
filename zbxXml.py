#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年3月17日

@author: debo.zhang
'''
import xml.sax
import xml.sax.handler  
from zabbixgraph import ZabbixGraph
import time
import datetime
from fastdfs import FastDFS

class XMLHandler(xml.sax.handler.ContentHandler):  
    def __init__(self):
        self.buffer = ""                    
        self.mapping = {}                  

    def startElement(self, name, attributes):  
        self.buffer = ""                    

    def characters(self, data):  
        self.buffer += data                      

    def endElement(self, name):  
        self.mapping[name] = self.buffer           

    def getDict(self):  
        return self.mapping
    

class MarkDown(object):
    def __init__(self):
        self.xh = XMLHandler()
        self.zabbix = ZabbixGraph()
        self.htime = datetime.datetime.now() - datetime.timedelta(days=-1*365,hours=-1)
        self.time = time.localtime(time.mktime(self.htime.timetuple()))
        self.timestamp = time.strftime('%Y%m%d%H%M%S',self.time)
        
    def getXmlData(self,data): 
        xml.sax.parseString(data, self.xh)
        ret = self.xh.getDict()
        return ret
    
    def mdData(self,data):
        xmlMap = self.getXmlData(data)
        title = xmlMap.get("name")
        level = xmlMap.get("level")
        time = xmlMap.get("time")
        age = xmlMap.get("age")
        ip = xmlMap.get("ip")
        key = xmlMap.get("key")
        value = xmlMap.get("value")
        itemid = xmlMap.get("itemid")
        url = xmlMap.get("url")
        host = xmlMap.get("from")
        eventid = xmlMap.get("id")
        status = xmlMap.get("status")
        #![zbximg](data:image/png;base64,%s)
        graph = self.zabbix.getGraph(itemid, self.timestamp,based=False)
        fastdfs = FastDFS(eventid,status)
        fastdfs.mkfile(graph)
        graph_url = fastdfs.upload()
        mdStyle = u"""##### %s
        
###### 告警级别：%s

###### 故障时间：%s

###### 故障时长：%s

###### IP地址：%s

###### 检测项：%s

值：**%s**

###### [%s·%s ([%s](%s))]

![zbximg](%s)

"""  % (
               title,
               level,
               time,
               age,
               ip,
               key,
               value,
               host,
               status,
               eventid,url,
               graph_url
               )
        print mdStyle
        return mdStyle

if __name__ == "__main__":
    #data = '''<?xml version="1.0" encoding="UTF-8"?><note><to>World</to><from>Linvo</from><heading>Hi</heading><body>Hello World!</body></note>'''
    data = """<?xml version="1.0" encoding="utf-8"?> 
<root> 
<from>pxxzsassapi01.rmz.flamingo-inc.com</from> 
<time>2017.03.17 09:51:47</time> 
<level>Average</level> 
<name>PROBLEM:Nginx Error great than 50 twices in 3 mins on pxxzsassapi01.rmz.flamingo-inc.com</name> 
<key>ngx_errors</key> 
<value>575</value> 
<now>575</now> 
<id>3801845</id> 
<ip>10.8.8.87</ip> 
<url>http://zabbix.corp.flamingo-inc.com/tr_events.php?triggerid=23004&amp;eventid=3801845</url> 
<age>0m</age> 
<itemid>37082</itemid>
<status>PROBLEM</status> 
<acknowledgement>No</acknowledgement> 
<acknowledgementhistory></acknowledgementhistory> 
</root>"""
    markdown = MarkDown()
    print markdown.mdData(data)
    