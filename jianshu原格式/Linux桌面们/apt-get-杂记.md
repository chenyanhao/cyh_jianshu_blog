# 默认存放位置

下载的软件：/var/cache/apt/archives
安装后软件： /usr/share
可执行文件：/usr/bin
配置文件：/etc
lib 文件：/usr/lib

# 常用命令  
 update - 重新获取软件包列表  
 upgrade - 进行更新  
 install - 安装新的软件包  
 remove - 移除软件包  
 autoremove - 自动移除全部不使用的软件包  
 purge - 移除软件包和配置文件  
 dist-upgrade - 发行版升级  
 clean - 清除下载的归档文件  
 autoclean - 清除旧的的已下载的归档文件  

# apt 和 dpkg 区别

一句话简单来说，dpkg 是基础设施，它只管本地安装 deb 包；apt 基于 dpkg 之上，它会解决模块依赖问题，从远端软件仓库拉取安装包到本地，然后调用 dpkg 完成本地安装。




