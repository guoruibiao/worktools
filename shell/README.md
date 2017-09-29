一些比较实用的shell脚本，方便查找配置信息用。

## `udloader.sh`
使用方式：
- `~/.udloaderrc` 没有就新建一个。

```
host user@ip
port sshd的端口，默认22，修改了的话记得使用修改后的端口
```
- `~/.zshrc`(或者`~/.bashrc`)中添加如下别名：

```
alias udloader='sh /your/save/path/udloader.sh'
```

- 开始使用：
  * `udloader --help`:  显示帮助信息
  * `udloader upload localpath remotepath`: 将本地文件上传到虚拟机上指定路径
  * `udloader download remotepath localpath`: 将虚拟机上指定路径的文件拷贝到本地指定的路径
