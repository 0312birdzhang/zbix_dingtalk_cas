#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年3月17日

@author: debo.zhang
'''
from dingding import DingTalk
from zabbixgraph import ZabbixGraph
from zbxXml import MarkDown
import argparse
import sys



def get_args_parser():
    parser = argparse.ArgumentParser(
        description='This tool is used to sender zabbix alert msg to dingding group.')
    parser.add_argument(
        '-webhook', type=str,
        help='Token url from Dingtalk',
        default='https://oapi.dingtalk.com/robot/send?access_token=74eef3052878a2a5f9150a2438dd677ebdb39484593fb39263ea7177878e695d')
    parser.add_argument(
        '-msg', type=str,
        help='Xml msg from zabbix action')
    return parser


if __name__ == "__main__":
#     args = get_args_parser().parse_args()
#     markdown = MarkDown()
#     mdText = markdown.mdData(args.msg)
#     ding = DingTalk(args.webhook)
#     ding.senderMarkdown("Test xxxx", mdText)
    if len(sys.argv) < 4:
        sys.exit(1)
    token = sys.argv[1]
    subject = sys.argv[2]
    msg = sys.argv[3]
    markdown = MarkDown()
    mdText = markdown.mdData(msg)
    ding = DingTalk(token)
    ding.senderMarkdown(subject, mdText)