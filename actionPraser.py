#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-09-06 14:38:46
# @Last Modified by:   anchen
# @Last Modified time: 2016-09-19 09:46:26
import Mylog
import re 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ParsingXML(object):
    """docstring for ParsingXML"""
    def __init__(self, file_path, apk_md5, output_file, log_file):
        self.file_path = file_path
        self.apk_md5 = apk_md5
        self.output_file = output_file
        self.log_file = log_file
        self.log = Mylog.Mylog(self.log_file).getObject()

    def GetItemListFromXml(self,XmlFile,xx):
        item_list = []
        f=open(XmlFile,'r')
        temp=f.read()
        f.close()
        pattern = re.compile(xx)  
        results = pattern.findall(temp)  
        for ret in results:
            tar = ret.split('\"')
            if tar[1] not in item_list:
                item_list.append(tar[1]) 
        return item_list 

    def getAction(self):
        xxx=r'\<action android:name=.*\/\>'
        return self.GetItemListFromXml(self.file_path,xxx)

    def getPermission(self):
        xx=r'\<uses-permission android:name=.*\/\>' 
        return self.GetItemListFromXml(self.file_path,xx)
   
    def permissionFliter(self,str):
        str = str.split('.')
        for index,item in enumerate(str):
            if item == 'permission':
                ret = str[index+1:]
                ic = ''
                for i in ret:
                    ic += i + '.'
                return ic[:-1]

    def printResult(self):
        self.log.info('printResult')
        out = ''
        list1 = self.getPermission()
        for l1 in list1:
            out += self.apk_md5 + '|' + '1' + '|' + l1[19:] + '\n'
        list2 = self.getAction()
        for l2 in list2:
            out += self.apk_md5 + '|' + '2' + '|' + l2 + '\n'
        print out

    def run(self):
        self.log.info('run -begin to find permission and action in '+ self.apk_md5 + '.apk' + ' xml')
        out = ''
        f = open(self.output_file, 'a+')
        list1 = self.getPermission()
        for l1 in list1:
            handledPermissionStr = self.permissionFliter(l1)
            out += self.apk_md5 + '|' + '1' + '|' + handledPermissionStr + '\n'
        list2 = self.getAction()
        for l2 in list2:
            out += self.apk_md5 + '|' + '2' + '|' + l2 + '\n'
        f.write(out)
        f.close()

path = sys.argv[1]
md5 = sys.argv[2]
output_file = sys.argv[3]
log_file = sys.argv[4]
obj = ParsingXML(path, md5, output_file,log_file)
obj.run()
obj.log.info('finish find permission and action in '+ md5 + '.apk' + ' xml')
