#!/usr/bin bash
# _*_ coding: utf8 _*_

        echo "欢迎使用udloader脚本，本脚本用于跨主机的文件传输使用^_^, 底层封装了一下scp,更多内容可以通过man scp来查看！  "
        echo "------------------------格式------------------------------"
        echo "| ·上传本地文件到远程主机: upload localpath  remotepath  |"
        echo "| ·下载远程主机文件到本地: download remotepath localpath |"
        echo "| ·version: 0.0.1                                        |"
        echo "| ·author: 郭璞                                          |"
        echo "----------------------------------------------------------"

# 具体实现scp包装下的上传逻辑
upload() {
    host=`cat ~/.udloaderrc | grep -w host | awk '{print $2}'`
    port=`cat ~/.udloaderrc | grep -w port | awk '{print $2}'`
    localpath=$1
    remotepath=$host:$2
    #echo "scp -P $port $localpath $remotepath"
    scp -P $port $localpath $remotepath
    echo "uploaded."  
}

# 具体实现SCP包装下的下载逻辑
download() {
    host=`cat ~/.udloaderrc | grep -w host | awk '{print $2}'`
    port=`cat ~/.udloaderrc | grep -w port | awk '{print $2}'`
    localpath=$2
    remotepath=$host:$1
    scp -P $port $remotepath $localpath
    echo "dwonloaded."
}

# 判断action是否指定
if [ -z $1 ];then
    echo "您需要指定upload或者是download！"
    exit
fi

# 判断是否给了路径信息
if [[ -z $2 && -z $3 ]]; then
    echo "没给路径是不能使用的！"
    exit
fi

# 判断参数个数是否合格
if [[ -z $2 && $3 || $2 && -z $3 ]];then
    echo "参数个数不符合要求，请检查后重试！"
    exit
fi
# 判断命令是否支持
case $1 in
    "upload")
        echo "uploading..."
        upload $2 $3
        ;;
    "download")
        echo "downloading..."
    download $2 $3
        ;;
    "--help")
        echo "欢迎使用udloader脚本，本脚本用于跨主机的文件传输使用！  "
        echo "------------------------格式------------------------------"
        echo "| ·上传本地文件到远程主机: upload localpath  remotepath  |"
        echo "| ·下载远程主机文件到本地: download remotepath localpath |"
        echo "| ·version: 0.0.1                                        |"
        echo "| ·author: 郭璞                                          |"
        echo "----------------------------------------------------------"
        ;;
    *)
        echo "不支持的action"
esac
