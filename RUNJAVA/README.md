# 命令行终端执行Java

## 初始化脚本
将下面的文件保存为`compileandrun.sh` , 里面的`SEARCH_PATH`路径记得替换成自己的

```
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
```

## 别名
老是`bash compileandrun.sh xxx.java` 总归是多打了几个字符，所以能省事一点就省事一点，比如加一个别名:
```
echo alias runjava='bash /xxxxxx/compileandrun.sh' >> ~/.bashrc
```
再`source`下`~/.bashrc` 就可以在当前会话中生效了。

## 测试
```
// MyTest.java
import java.util.Map;
import redis.clients.jedis.Jedis;
public class MyTest {
    public static void main(String[] args) {
        String key = "uid:2614677";
		Jedis jedis = new Jedis("192.168.32.103", 6379);
		Map<String, String> userinfo = jedis.hgetAll(key);
		System.out.println(userinfo);
    }
}
```
编译、运行
```
###########################################
# 基本上每个项目都只有一个依赖包目录，所以#
# 所以有必要的话单独设置下SEARCH_PATH即可 #
# TODO runtime_class_path 的自发现实现    #
###########################################
{valid=0, birthday=, phone=110, lastlivetime=1548064849, memberid=, truename=xxxxxx, registertime=2017-11-09 10:16:57}
```

基本上可以满足需求了，但是每次取修改SEARCH_PATH也不是个事，能做到依赖包的自发现那就再好不过了，后续可以朝这个方向努努力，争取实现下。
