#!/usr/bin bash
# filename: compileandrun.sh
# create at 2019年01月23日19:17:46 by VIM 7.2
# 目标: 自配置classpath
ORIGIN_PATH=`pwd`
#echo $ORIGIN_PATH
# 项目的根目录 一般不会怎么变化，就每次都改着用吧，或者通过export的形式动态添加，会话内有效
echo "###########################################"
echo "# 基本上每个项目都只有一个依赖包目录，所以       #"
echo "# 所以有必要的话单独设置下SEARCH_PATH即可      #"
echo "# TODO runtime_class_path 的自发现实现      #"
echo "###########################################"

SEARCH_PATH=/home/wwwroot/chattvserver/libs/
cd $SEARCH_PATH
RUNTIME_CLASS_PATH=`find ./ -name "*.jar" | sed "s#./#$SEARCH_PATH#" | tr "\n" ":"`.
cd $ORIGIN_PATH
#echo PWD:$ORIGIN_PATH
#echo "--------------------"
NAME=$1
PREFIX=`echo $NAME| echo ${NAME%.*}`
#echo name: $NAME
#echo prefix: $PREFIX
RUBBISH_FILE=$PWD/$PREFIX.class
javac -classpath $RUNTIME_CLASS_PATH $PWD/$1
java -classpath $RUNTIME_CLASS_PATH $PREFIX

rm $RUBBISH_FILE
cd $ORIGIN_PATH
