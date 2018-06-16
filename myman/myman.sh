#!/usr/bin bash
# myman command
############################################################
DOCS_PATH="/home/developer/guo/myman/docs"
BIN_PATH="/home/developer/guo/myman/myman.sh"
############################################################
REPO_CMDS_URL="https://raw.githubusercontent.com/guoruibiao/worktools/master/myman/commands.list"
REPO_MYMAN_URL="https://raw.githubusercontent.com/guoruibiao/worktools/master/myman/myman.sh"
CMD_DOWNLOAD_URL="https://raw.githubusercontent.com/guoruibiao/worktools/master/myman/docs/"
LOCAL_AVAIABLE_COMMANDS=`ls $DOCS_PATH | tr "\t" "\n"`
DESCRIPTION="subcommands which myman supports:\n\tmyman linux-command    # 查看linux-command的使用范例\n\tmyman update linux-command        # 更新一个本地已存在的命令文档\n\tmyman install linux-command       # 从云端下载一个命令的文档\n\tmyman list                        # 罗列本地、云端所有的命令文档列表\n\tmyman search linux-command        # 搜索云端支持的命令文档，并以less形式进行展示\n\tmyman --upgrade    # 从云端自更新myman\n\tmyman -h --help    # 查看myman支持的所有子命令\n"


echo ""
for item in ${LOCAL_AVAIABLE_COMMANDS[@]}
do
    if test  "$1" == "$item";then
        cat $DOCS_PATH/$1
        exit 0
    fi
done

# 更新docs
if test "$1" == "update";then
    # 做更新逻辑
    curl -s $CMD_DOWNLOAD_URL$2 > $DOCS_PATH/$2 
    echo "[$2] 命令已更新"
elif test "$1" == "install";then
    # 下载并保存到本地
    curl -s $CMD_DOWNLOAD_URL$2 > $DOCS_PATH/$2 
    echo "[$2] 成功下载到本地啦"
elif test "$1" == "list";then
    echo "本地已安装命令文档:"
    echo $LOCAL_AVAIABLE_COMMANDS
    REPO_AVAIABLE_COMMANDS=`curl -s $REPO_CMDS_URL`
    echo "云端可用命令文档:"
    echo $REPO_AVAIABLE_COMMANDS
    echo "TODO: array diff in bash."
elif test "$1" == "search";then
    IN_REPO=`curl -s $REPO_CMDS_URL | grep $2`
    if test "$IN_REPO" == "$2";then
        curl -s $CMD_DOWNLOAD_URL$2 | less
        echo "[$2] 命令可以下载，简要内容如下:"
    else
        echo "[$2] 命令文档暂不支持，期待您的贡献与参与哦~"
    fi
elif test "$1" == "--help";then
    echo -e $DESCRIPTION
elif test "$1" == "-h";then
    echo -e $DESCRIPTION
elif test "$1" == "--upgrade";then
    curl -s $REPO_MYMAN_URL > $BIN_PATH
    echo "myman 云端自更新完成到$BIN_PATH啦，使用myman --help 看看有什么新功能吧~"
    echo -e "切记本地的DOCS_PATH和BIN_PATH一定要\33[0m\33[31m\33[42m\33[5m按照自己的实际情况来修改\33[0m，否则路径就会存在问题滴~"
else
    echo "Command ["$1"] not found." 
fi
