#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-09-06 14:38:46
# @Last Modified by:   anchen
# @Last Modified time: 2016-09-09 11:57:09
import xml.etree.ElementTree as ET
import Mylog
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
        self.tree = ET.parse(self.file_path)
        self.root = self.tree.getroot()
        self.log = Mylog.Mylog(self.log_file).getObject()


    def tellPythonVersion(self):
        v = sys.version
        version = v[0:6]
        num = 10*int(version[0]) + int(version[2])
        return num  

#2.7以上使用getiterator    #2.6以下使用iter
    def parseTag(self,tag):
        self.log.info('parseTag')
        action_list = []
        version = self.tellPythonVersion()
        if version > 26:
            tag_list = self.root.iter(tag)
        else:
            tag_list = self.root.getiterator(tag)

        for v in tag_list:
            f = v.attrib.values()
            f=f[0]
            if f not in action_list and 'action.MAIN' not in f:
                action_list.append(f)
        return action_list

    def getAction(self):
        self.log.info('getAction')
        return self.parseTag('action')

    def getPermission(self):
        self.log.info('getPermission')
        return self.parseTag('uses-permission')

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
            out += self.apk_md5 + '|' + '1' + '|' + l1[19:] + '\n'
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


