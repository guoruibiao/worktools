#!/usr/bin/env bash
# 查看SVN管理下某文件最近一次被改动的内容
# svn log xxx -l 2
# svn diff xxx -r old_version:new_version

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

# 格式化输出内容
echo "                        ${NEW_VERSION_NUMBER} <-- ${OLD_VERSION_NUMBER} "
echo "操作人[${NEW_OPERATOR}] ----------------> 被操作人[${OLD_OPERATOR}]"
echo "详细改动为"
svn diff $DIFF_OBJECT -r ${OLD_VERSION_NUMBER}:${NEW_VERSION_NUMBER}
