#!/bin/sh
# @Author: anchen
# @Date:   2016-08-23 15:33:15
# @Last Modified by:   anchen
# @Last Modified time: 2016-09-18 17:47:27
out_log='log/virus_analyze.log'
key_code_block='result/key_codeblock.txt'
action_permission_report='result/act_permis.txt'
temp_log='temp.txt'

DecompilingApk()
{
    JAVA_OPTS="-Xmx4G" jadx -j 1 -d $2 $1 > $temp_log
}

getFileNameFromPath()
{
    get=$1
    div=($(tr "/" " " <<< $get))
    sum=${#div[@]}
    let index=$sum-1
    tar=${div[$index]}
    echo $tar 
}

dir=$1
tar=${dir%%.*}
apk_md5=$(getFileNameFromPath $tar)

#$1 APK文件路径 $2 源码包输出路径
msg=':begin to decode apk.............'
echo $apk_md5$msg
DecompilingApk $1  $2
#解析APK反编译日志文件
echo 'begin to analyze decode apk log.............'
python ApkDecodeLogHandler.py $temp_log  $out_log  $apk_md5
echo 'begin to find key codeblock........................'
python codeSort.py $2  $apk_md5   $key_code_block  $out_log  

xml_file_name=/AndroidManifest.xml
xml_path=$2$xml_file_name
echo 'begin to find action and permission........................'
python actionPraser.py $xml_path $apk_md5  $action_permission_report $out_log
rm $temp_log
echo '............................finish..................................'