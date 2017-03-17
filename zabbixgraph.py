#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年3月17日

@author: debo.zhang
'''
import httplib, urllib, urllib2, cookielib
import base64
import time
# 1. Grab the Ticket Granting Ticket (TGT)

class ZabbixGraph(object): 
    def __init__(self):
        
        self.cas_host = "auth.corp.flamingo-inc.com"
        self.rest_endpoint = "/v1/tickets/"
        self.params = urllib.urlencode({'username': 'tsupport', 'password': 'password','token':'Saportal_308sdfllsa'})
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
        self.url = 'http://zabbix.corp.flamingo-inc.com'
        self.service  = self.url +'/index.php'
    
    def getGraph(self,itemid,stime,width=800,height=600,based=True):
        conn = httplib.HTTPSConnection(self.cas_host)
        conn.request("POST", self.rest_endpoint, self.params, self.headers)
        response = conn.getresponse()
        # print response.status, response.reason
        data = response.read()
        location = response.getheader('location')
        #  Pull off the TGT from the end of the location, this works for CAS 3.3-FINAL
        tgt = location[location.rfind('/') + 1:]
        conn.close()

        # print location
        # print tgt
        # print "***"
         
        # 2. Grab a service ticket (ST) for a CAS protected service
        #http://zabbix.corp.flamingo-inc.com/chart2.php?graphid=918&period=3600&stime=20180317090528&updateProfile=1&profileIdx=web.screens&profileIdx2=918&width=1778 
        params = urllib.urlencode({'service': self.service })
        conn = httplib.HTTPSConnection(self.cas_host)
        conn.request("POST", "%s%s" % ( self.rest_endpoint, tgt ), params, self.headers)
        response = conn.getresponse()
        # print response.status, response.reason
        st = response.read()
        conn.close()
         
        # print "service: %s" % (service)
        # print "st     : %s" % (st)
        # print "***"
         
        # 3. Grab the protected document
         
        url  = "%s?ticket=%s" % ( self.service, st )  # Use &ticket if service already has query parameters
        # print "url    : %s" % (url)
         
        cj = cookielib.CookieJar()
        # no proxies please
        no_proxy_support = urllib2.ProxyHandler({})
        # we need to handle session cookies AND redirects
        cookie_handler = urllib2.HTTPCookieProcessor(cj)
         
        opener = urllib2.build_opener(no_proxy_support, cookie_handler, urllib2.HTTPHandler(debuglevel=1))
        urllib2.install_opener(opener)
        urllib2.urlopen(url).read()
        # print protected_data
        #chart.php?period=3600&stime=20170317093144&itemids%5B0%5D=50687&type=0&width=1034
        graph_url = self.url + "/chart.php?period=3600&type=0&updateProfile=1&profileIdx=web.item.graph&profileIdx2=%s&stime=%s&itemids[]=%s&width=%s&height=%s&screenid=&curtime=%s" %(str(itemid),str(stime),str(itemid),str(width),str(height),str(int(time.time())*1000))
#         graph_url = self.url + "/chart.php?period=3600&stime=20180317093144&itemids%5B0%5D=50687&type=0&updateProfile=1&profileIdx=web.item.graph&profileIdx2=50687&width=1034&sid=432984218898ef1d&screenid=&curtime=1489724517810"
        graph_data = urllib2.urlopen(graph_url).read()
        if based:
            return base64.b64encode(graph_data)
        else:
            return graph_data

if __name__ == "__main__":
    zabbixGraph = ZabbixGraph()
    print "base64:%s" % (zabbixGraph.getGraph(50687, 20170317093144),)