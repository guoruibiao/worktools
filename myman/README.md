Linux 自带的man帮助文档虽然是很全面而且很正规的，但是没有示例，所以某一个命令今天查了，明天可能再遇到还是忘记了用法，不得不打开浏览器搜索对应命令的具体用法，这在一定程度上就算是浪费了时间。因此，有了`myman`的想法，与`zsh`, `fish`这些思路不同，`myman`不会抢夺`man`本身的用法，按照unix世界的思想**一个工具一次只完成一个功能**，因此`myman`的定位就只是对**示例**进行完善啦。

## 下载与安装
- 下载脚本：`https://raw.githubusercontent.com/guoruibiao/worktools/master/myman/myman.sh > /targetpath/myman.sh`
- 准备文档存放目录：` cd /targetpath && mkdir docs`
- 配置别名： `echo alias myman='/targetpath/myman.sh' >> ~/.bashrc && source ~/.bashrc`



## 使用范例
![myman使用方法](https://raw.githubusercontent.com/guoruibiao/worktools/master/myman/myman.png)

shell 写脚本相比于其他高级语言，还是有一定的局限性，但是可以直接使用linux上的一些命令，这倒是一个优势。
myman模拟了pip的一些命令，但是实现的比较简单，而且对**`云端文档`** 的依赖性比较大，需要耗费文档编辑的精力和维护。

有兴趣的可以来PR啊，myman,让生活更简单点吧。
