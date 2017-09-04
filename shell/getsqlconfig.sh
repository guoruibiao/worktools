#!/usr/bin zsh
# 使用AWK和grep看看能不能获取到数据库特定字段的密码
keyword=$1
if [ -z "$keyword" ]
then
    echo "关键字不能为空，否则无法使用这个脚本的!"
	echo "格式为:"
	echo "sh getter.sh 'keyword'"
	exit
else
    echo "即将匹配的字段名为：$1"
    cat /Users/changba164/guo/code/ktvserver/common/config.db.inc.php | grep $1
    echo "开始复制密码"
    sleep 1
    cat /Users/changba164/guo/code/ktvserver/common/config.db.inc.php | grep $1 | grep password | awk -F = '{print $2}' | sed 's/;$//' | sed "s/\'//g" | pbcopy
    echo "密码字段已复制到系统剪切板"
fi
