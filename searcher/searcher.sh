#!/usr/bin bash
# 使用shell配合Python脚本查找文件中某一个变量或者字符串所在的行数


filelist=`find $1 -name "*.*"`

for file in ${filelist[@]};do
    #echo $file;
    python /home/guoruibiao/tools/searcher/searcher.py $file $2
done;

#find $1 -name "*.*" | xargs python $2
