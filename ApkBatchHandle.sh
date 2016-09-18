#!/bin/sh
# @Author: anchen
# @Date:   2016-08-26 14:53:10
# @Last Modified by:   anchen
# @Last Modified time: 2016-09-18 16:06:34
md5_exist=1
md5_noHas=0
decoded_log=md5_log.txt 

getFileSize()
{
    dir=$(du -a $1)
    var1=`echo $dir | awk -F ' ' '{print $1}'`
    echo $var1   
}

checkMd5()
{
    md5=$1
    python findMd5.py $md5
    ret=$?
    if test $[ret] -eq 1
    then
        echo $md5_exist
    else
        echo $md5_noHas  
    fi
}

DecompilingApkList()
{
    path=$1
    # bigApk=/opt/smmc/data_backup/big_apk/
    # bigApk=/mnt/hgfs/winShare/big_apk2
    bigApk=/home/sheldon/apkBig/ 
    filelist=`ls -Sr $path`
    for file in $filelist
    do 
        fileNmae=${file%.apk*}
        filePath=$1$file
        sourcePath=$2$fileNmae
        file_size=$(getFileSize $filePath)
        ret=$(checkMd5 $fileNmae)
        if test $[ret] -eq  0                                
        then
            if test $[file_size] -lt 80000
            then
                ./analyzeApk.sh $filePath $sourcePath
                echo $fileNmae >> $decoded_log
            else
                mv $filePath $bigApk
            fi
        else
            echo $fileNmae':file had been handled'
        fi 
    done
}

#$1 APK文件路径   $2 输出APk源码路径
DecompilingApkList  $1  $2 
