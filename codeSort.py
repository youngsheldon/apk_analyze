#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-08-23 17:24:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-09-14 10:39:17
import os
import re
import sys
import Mylog
reload(sys)
sys.setdefaultencoding('utf-8')

class Analyze(object):
    """docstring for Analyze"""
    def __init__(self, FilePath, apk_md5, output_file, log_file):
        self.output_file = output_file
        self.FilePath = FilePath 
        self.apk_md5 = apk_md5
        self.log_file = log_file
        self.key = ''
        self.filepath = ''
        self.line_index = ''
        self.code_content = ''
        self.log = Mylog.Mylog(self.log_file).getObject()
        self.print_flag = 0

    def clear(self):
        self.log.info('clear')
        self.filepath = ''
        self.line_index = ''
        self.code_content = ''

    def enablePrint(self):
        self.print_flag = 1

    def getRegularExpression(self):
        self.log.info('getRegularExpression')
        expr_dict={}
        f=open('setting/config.ini','r')
        for i in f:
            if 'Key' in i:
                ret=i.split('\n')
                ret1=ret[0].split('=')
            expr_dict[ret1[0]] = ret1[1]
        f.close()
        expr_list=sorted(expr_dict.iteritems(),key = lambda asd:asd[0],reverse = False)
        return expr_list

    def OutPutReport(self):
        self.log.info('OutPutReport')
        f = open(self.output_file, 'a+')
        out = self.apk_md5 + '|' + self.key + '|' + self.filepath + '|' + self.line_index + '|' + self.code_content + '\n'
        f.write(out)
        f.close()

    def GetFilePathList(self, rootDir):
        self.log.info('GetFilePathList')
        FilePathList=[]
        for root,dirs,files in os.walk(rootDir):
            for filespath in files:
                FilePathList.append(os.path.join(root,filespath))
        return FilePathList

    def GetCodeBlockFromJavaSouce(self, Context, StringToFind):
        pattern = re.compile(StringToFind)  
        results = pattern.findall(Context)  
        return results

    def FindTarStringLocationInFile(self, file, TarString):
        self.log.info('FindTarStringLocationInFile')
        line_num = 0
        ContextToSave = ''
        f=open(file,'r')
        for line in f:
            line_num+=1
            ret = self.GetCodeBlockFromJavaSouce(line,TarString)
            if ret and "CONTACT javamail@sun.com" not in line and 'android' not in file:
                ContextToSave+= file +':' + str(line_num)+'\r'+line+'\r'
                self.filepath = file
                self.line_index = str(line_num)
                self.code_content = line.strip()
        if self.print_flag:
            print ContextToSave
        f.close()

    def FindTarString(self,TarString):
        self.log.info('FindTarString')
        list=self.GetFilePathList(self.FilePath)
        for l in list:
            if 'android' not in l and 'javax' not in l and 'res' not in l and '.java' in l:
                f=open(l,'r')
                Context=f.read()
                f.close()
                ret=self.GetCodeBlockFromJavaSouce(Context,TarString)
                if ret:
                    self.FindTarStringLocationInFile(l,TarString)

    def run(self):
        self.log.info('run -begin to find key codeblock in '+ self.apk_md5 + '.apk' + ' source')
        expr_list = self.getRegularExpression()
        for l in expr_list:
            self.key = l[0]
            if self.print_flag:
                print l[0]
            self.FindTarString(l[1])
            if self.code_content is not '':
                self.OutPutReport()
            self.clear()


tarpath = sys.argv[1]
apk_md5 = sys.argv[2]
outPutfileName = sys.argv[3]
log_file = sys.argv[4]
obj = Analyze(tarpath,apk_md5,outPutfileName,log_file)
obj.run()
obj.log.info('finish find key codeblock in '+ apk_md5 + '.apk' + ' source')
