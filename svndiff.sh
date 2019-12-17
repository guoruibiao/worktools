#!/usr/bin/env bash
# 当前工作目录，备用
CURRENT_WORKSPACE=`pwd`
# 待对比对象，可以是具体的文件名，也可以是目录， TODO 处理为空的case
DIFF_OBJECT=$1
#echo $DIFF_OBJECT
cd $CURRENT_WORKSPACE
# 拿到diff 执行结果
NEW_OPERATOR=`svn log $DIFF_OBJECT -l 2 | grep -o "^r.*" | awk -F'|' '{print substr($1, 2, length($1)), $2}' | head -1 | awk '{print $2}'`
NEW_VERSION_NUMBER=`svn log $DIFF_OBJECT -l 2 | grep -o "^r.*" | awk -F'|' '{print substr($1, 2, length($1)), $2}' | head -1 | awk '{print $1}'`
OLD_OPERATOR=`svn log $DIFF_OBJECT -l 2 | grep -o "^r.*" | awk -F'|' '{print substr($1, 2, length($1)), $2}' | head -2| tail -1 | awk '{print $2}'`
OLD_VERSION_NUMBER=`svn log $DIFF_OBJECT -l 2 | grep -o "^r.*" | awk -F'|' '{print substr($1, 2, length($1)), $2}' | head -2| tail -1 | awk '{print $1}'`
COMMENT=`svn log $DIFF_OBJECT -l 1 | grep @`

# 格式化输出内容
echo "操作人[${NEW_OPERATOR}@${NEW_VERSION_NUMBER}] ---> 被操作人[${OLD_OPERATOR}@${OLD_VERSION_NUMBER}]"
echo "详细改动为:  $COMMENT"

svn diff $DIFF_OBJECT -r ${OLD_VERSION_NUMBER}:${NEW_VERSION_NUMBER}
