#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年3月17日

@author: debo.zhang
'''
import os
import pycurl
import json
import urllib2
import time
import sys

class Response(object):
    def __init__(self):
        self.chuncks = []

    def callback(self, chunck):
        #self.chuncks.append(str(chunck, 'utf8'))
        self.chuncks.append(chunck)
    def content(self):
        return  "".join(self.chuncks)

    def clear(self):
        self.chuncks = []
        
class FastDFS(object):
    def __init__(self,eventid,status):
        self.__appid__ = "8157239032"
        self.__appsecret__ = "quoACsyrHILKKFKFzBDs"
        self.upurl = "http://upload.com/"
        self.uri = "zbx/%s/%s_%s.png" %(time.strftime("%Y%m%d%H"),str(eventid),str(status))
        self.filename = "%s_%s.png" %(eventid,status)
        self.response = Response()
        self.curl = pycurl.Curl()
        
    def upload(self):
        url = self.upurl+"dfs/upload"
        file_size = os.path.getsize(self.filename)
        self.curl.setopt(pycurl.URL, str(url.encode("utf-8")))
        self.curl.setopt(pycurl.WRITEFUNCTION, self.response.callback)
        self.curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.curl.setopt(pycurl.HTTPHEADER, ['Content-Type: multipart/form-data'])
        self.curl.setopt(pycurl.HTTPPOST,[
            ('filename',          (pycurl.FORM_FILE, str(self.filename))),\
            ('filelength',        (pycurl.FORM_CONTENTS, str(file_size))),\
            ('content-type',      (pycurl.FORM_CONTENTS, "image/png")), \
            ('canupdate',             (pycurl.FORM_CONTENTS,"true")), \
            ('appid',             (pycurl.FORM_CONTENTS,str(self.__appid__))), \
            ('description',             (pycurl.FORM_CONTENTS,"")), \
            ('precache',            (pycurl.FORM_CONTENTS,"false")), \
            ('appsecret',             (pycurl.FORM_CONTENTS,str(self.__appsecret__))), \
            ('uri',               (pycurl.FORM_CONTENTS,str(self.uri)))
        ])
        try:
            self.curl.perform()
            resp = self.response.content().decode("utf-8")
            downurl = json.loads(resp).get("message")
            return downurl
        except Exception ,e:
            print e
    
    def mkfile(self,file_cotent):
        with open(self.filename,"w") as f:
            f.write(file_cotent)
            
    def delfile(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
    
if __name__ == "__main__":
    fastdfs = FastDFS("3804337","OK") 
    print fastdfs.upload()
