#。。。未完待续


# 更改Mac默认睡眠模式

## 三种睡眠模式

Mac睡眠模式有三种，Sleep（睡眠）、Deep Sleep（深度睡眠）和Safe Sleep（安全睡眠）；对应的操作分别是Suspend to RAM、Suspend to Disk和Suspend to RAM and Disk，内部代码是睡眠模式0、1、3。

* Sleep：数据驻留在内存中，内部代号```hibernatemode 0```。

	这种模式下电脑进入睡眠时，数据保留在内存中，不写入硬盘，仅用少量的电量对内存供电，以保持内存中的数据不会因断电而丢失。

	唤醒时直接重内存加载数据。所以优点是入睡快，唤醒快，不占用硬盘空间。但是一旦掉电，数据全部丢失，不可恢复，所以数据安全性不高是他的缺点。

* Deep Sleep：将数据保存在硬盘中，内部代号```hibernatemode 1```

	这种模式下，电脑进入睡眠时，首先将内存的数据快速写入硬盘中睡眠专用的内存镜像文件中（该文件位于：/var/vm/目录下，名为sleepimage，这是一个隐藏目录，vm的意思就是虚拟内存）。一旦内存数据写入硬盘成功后，就不再对内存供电，仅保留CPU监听唤醒信号的功能。

	唤醒时再将硬盘中的数据加载到内存中，因为入睡时要写入硬盘，唤醒的时候会看到一个显示加载进度的进度条，它的优点时安全性高、省电，缺点是占用硬盘空间和唤醒速度较Sleep要慢。

* Safe Sleep：上面两种模式的结合(也是OSX系统默认的睡眠级别)，内部代号```hibernatemode 3```

	当Mac进入睡眠时，先将内存中的数据写入到硬盘（防止数据丢失），然后对内存持续供电，所以它的特点是入睡快、唤醒快、安全性高。

	当电源供电正常时，可以像Sleep那样唤醒时直接重内存中读取数据；当电池耗尽后唤醒Mac，可以Deep Sleep那样从硬盘中的数据加载到内存。

	该模式结合了前两种模式的有点，同时也继承了缺点，就是要给内存持续供电、占用硬盘空间。

	便携式电脑一般采用这种模式，写入硬盘这点表现的尤为明显，如果时笔记本电脑，当你合上笔记本或点击睡眠的时候，就会发现呼吸灯首先一直保持高亮状态，这表示正在向硬盘中写入数据，当写入完成时指示灯开始进入呼吸状态，这表示你的Mac已经进入梦乡了！！

## 查看你的Mac当前的睡眠模式：

打开“终端”输入下面内容：```pmset -g | grep hibernatemode```

## 设置睡眠模式

打开“终端”输入下面内容：```sudo pmset -a hibernatemode xxx```

> xxx代表睡眠模式的代号

如果想设置回默认，则输入```sudo pmset -a hibernatemode 3```


## 如何选择

作为开发人员，平时工作会打开很多软件，如果每次开机完打开各种软件，然后把各个软件恢复到昨天或者一段时间之前的状态，会花掉很多时间。

所以对于开发人员来说，用操作系统上下文切换、保存现场的话来说，就是迅速恢复到当时的工作状态，这点是很重要的。因此：

* 如果```中断工作---再次工作```的时间较**长**频率较**低**，则建议将默认的睡眠模式设置为**深度睡眠模式** 
* 如果```中断工作---再次工作```的时间较**短**频率较**高**，则建议直接使用**默认睡眠模式** 


# 设置显示隐藏文件

```
defaults write com.apple.finder AppleShowAllFiles -bool true
killall Finder
```

若要不显示隐藏，将第一句的```true```改为```false```即可

# Mac自带emacs快捷键

例如，```C-n C-p C-b C-f C-a C-e```等等等等。

用这些能大幅度提高输入效率。

建议将```Ctrl```和```Caps lock```互换。

方法如下：

打开系统偏好设置=> 键盘，然后如图所示操作

![](http://upload-images.jianshu.io/upload_images/1936544-518ae410b69ddd68?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/1936544-9dcda19d74b75256?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



# 显示用户目录下的资源库文件夹(~/Library)

在我自己的电脑系统(OS X 10.11.5)下，用户目录下的资源库文件夹默认隐藏了不让查看，可能是由于苹果担心用户不小心误删了资源库中的文件，而故意隐藏。

不过想让这个文件夹显示出来也非常简单，直接在终端输入下列命令就可以了：

```chflags nohidden ~/Library```

如果还想让它隐藏，输入下面的指令：

```chflags hidden ~/Library```


# VIM

VIM想提高生产力，插件挺重要，号称最难装的插件———```YouCompleteMe```见另一篇[ VIM的折腾和配置](http://blog.csdn.net/chenyyhh92/article/details/52464101) (按照这篇的步骤，严格一步一步来，一定可以成功！)

然后就是配置：[```.vimrc```以及```.ycm_extra_conf.py```配置](https://github.com/chenyanhao/vim-cyh)

# Emacs

Emacs很复杂，已经可以单独占篇幅了，所以参见我的另一篇博客：[Emacs的折腾和配置 ](http://blog.csdn.net/chenyyhh92/article/details/53414497)

# Java&Scala环境搭建

* Java：去Oracle官网下载想要安装的JDK的dmg包，然后挂载dmg包，按照正常的dmg软件安装流程去安装即可，安装后不需要自行去配置环境变量。

	安装目录：```/Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home```
	
	> 验证：终端输入<code>java -version</code>

* Scala：有2种方式安装，推荐第二种

	1. 先去Scala官网下载Scala的语言包，该包是个.tar文件，解压该包，并把文件夹放到<code>/usr/local/</code>下，然后在家目录新建<code>.bash_profile</code>文件，并在里面添加两行：<code>SCALA\_HOME="/usr/local/scala-2.11.8"</code><br><code>export PATH=$PATH:$SCALA\_HOME/bin</code>
	2. 通过Homebrew安装：brew install scala

	> 验证：终端输入<code>scala -version</code>

## XCode安装以及一些必备插件

1. 安装XCode：去苹果商店下载。
2. 安装必备插件：
	* 安装Alcatraz(插件管理器)：<code>curl -fsSL https://raw.github.com/alcatraz/Alcatraz/master/Scripts/install.sh | sh</code>
		
		> 验证：XCode->Windows->Package Manager，看到这个就说明安装成功。
		
	* 安装xvim(vim插件)：进入Package Manager，然后搜索xvim，点击install即可。其他插件的安装同理。
	* 安装SCXcodeMinimap(代码地图)：像sublime text一样，右上角有个地图导航。
	* ...：根据个性化安装

	> 安装插件时候，有时候会遇到提示UUID失败等类似的错误提示，解决方案如下：
		0. 查找自己的UUID：<code>defaults read /Applications/Xcode.app/Contents/Info DVTPlugInCompatibilityUUID</code>
		1. 终端输入：<code>find ~/Library/Application\ Support/Developer/Shared/Xcode/Plug-ins -name Info.plist -maxdepth 3 | xargs -I{} defaults write {} DVTPlugInCompatibilityUUIDs -array-add ACA8656B-FEA8-4B6D-8E4A-93F4C95C362C</code>
		2. 手动添加：右键Xcode，选择显示包内容；然后找到Contents/Info.plist路径下的Info.plist文件；双击Info.plist文件，找到DVTPlugInCompatibilityUUID，将对应的UUID复制；接下来到出问题的插件所在目录下，右键，选择显示包内容，然后找到Contents/Info.plist路径下的Info.plist文件；双击Info.plist文件，将刚刚复制的UUID增加到DVTPlugInCompatibilityUUID字段里面，保存。

3. 卸载插件

	安装插件一般二个办法：一是通过前面提到的插件管理器Alcatraz安装，另一种是自己clone源码然后build安装。

	因此：
	* 如果是通过Alcatraz安装的，直接打开XCode的Package Manager卸载
	* 如果是通过自己手动安装的，进目录<code>~/Library/Application Support/Alcatraz/Plug-ins</code>删除插件的整个文件夹，然后删除<code>~/Library/Application Support/Developer/Shared/Xcode/Plug-ins</code>目录下该插件对应<code>.xcplugin</code>文件。
	
	删除Alcatraz本身(同上，删除插件文件夹以及插件的配置文件)：<code>rm -rf ~/Library/Application\ Support/Developer/Shared/Xcode/Plug-ins/Alcatraz.xcplugin<br>
rm -rf ~/Library/Application\ Support/Alcatraz</code>

# 终端命令显示不同颜色

Mac默认的终端不显示颜色，可以在<code>.bash_profile</code>中加上一句话即可：<code>alias ls="ls -G"</code>

# 关闭开机音

终端输入以下命令（会要求输入密码）

关闭：sudo nvram SystemAudioVolume=

开启：sudo nvram -d SystemAudioVolume


# Homebrew的安装与卸载

Homebrew是一个很好的包管理工具，它的好处和基本使用就不多说了，前人之述备矣。

安装卸载的方法来自于官网，具体有疑问的地方请参见Homebrew的Github官网。

Homebrew 将软件包分装到单独的目录```/usr/local/Cellar```，然后 symlink 到```/usr/local```中。 

* 安装：
<code>/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
</code>

* 卸载：
	1. <code>cd \`brew --prefix\`</code>
	2. `rm -rf Cellar`
	3. `brew prune`
	4. <code>rm \`git ls-files\`</code>
	5. `rm -r Library/Homebrew Library/Aliases Library/Formula Library/Contributions`
	6. `rm -rf .git`
	7. `rm -rf ~/Library/Caches/Homebrew`

CSDN网友给了个示例，也可以考虑这个：

```
gerryyang@mba:~$ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"  
It appears Homebrew is already installed. If your intent is to reinstall you  
should do the following before running this installer again:  
  
    rm -rf /usr/local/Cellar /usr/local/.git && brew cleanup 
```

这玩意儿很强大很好，建议就装着别卸。

## brew可以用第三方库

命令```brew tap xxx/yyy```，然后就可以```brew install aaa```了。

**brew常用命令：**

```
brew tap                     # list tapped repositories
brew tap <tapname>           # add tap
brew untap <tapname>         # remove a tap
```
## brew卸载时自动卸载不相关依赖

在stackoverflow上找到了答案，把问题和回答贴出来

**问题：**

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-40d72587b9bfe15e?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**答案：**
![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-00ea01fcde7d8a8d?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> stackoverflow原贴链接：```http://stackoverflow.com/questions/7323261/uninstall-remove-a-homebrew-package-including-all-its-dependencies```


# Mac下的Python环境

这篇[Python的杂项](http://blog.csdn.net/chenyyhh92/article/details/52963962)也可以参考。

我们知道，Mac系统自带了Python2，因为系统有些东西依赖了Python2；系统没有自带Python3。

系统的这种设定有几个问题：

1. 系统自带的跑跑系统的依赖还行，但是作为开发者要Python开发这就不够用了；
2. 系统有东西依赖着自带的Python，所以系统自带的Python也就顺理成章地成为了“高危区域”，一旦自己一个手贱把自带的Python搞坏了哪怕一点点，可能系统就会出现问题；
3. 系统自带的Python连pip这种神器都没有，需要自己```sudo easy_install pip```，而且国外网被墙了，经常失败，咱要是装个自带pip等这种神器的Python多好。

基于上面几点，所以我们需要安装平时可用(乱搞)的Python，这时候就就要借助到上面提到的Homebrew了。

用Homebrew安装的Python在```/usr/local/Cellar```下。

## 安装Python2

```brew install python```

## 安装Python3

```brew install python3```

> 这样安装好的Python2和Python3自带了pip~

## 设置PATH

可以先看一下自己的PATH：```echo $PATH```

里面应该会有: ```/usr/bin: /bin: /usr/sbin: /sbin: /usr/local/bin```

这个决定了终端里面找命令的顺序，因此想在输入Python时找我们自己装的Python，只需要把```/usr/local/bin```放在最前面即可：

改成：```/usr/local/bin: /usr/bin: /bin: /usr/sbin: /sbin```

> 修改PATH可以在```/etc/paths```里面修改，也可以在```~/.bash_profile```里面修改。建议后者，因为前者是系统的，后者是用户的。系统的别随便改，用户的随意改。

> 跟改之前的对比一下，可以看出，内容没有丝毫改变，就是改变了一下顺序而已。

## 验证PATH设置成功

1. 验证Python2
	* 输入```which python```
	* 如果显示```/usr/local/bin/python```则表明成功

2. 验证Python3
	* 输入```which python3```
	* 如果显示```/usr/local/bin/python3```则表明成功

## 安装、设置后，如何使用系统的Python

如果有需要想使用一下系统的Python，输入```/usr/bin/python```即可

## 安装后续

通过Homebrew安装的Python都是自带pip的，通过自带的这个pip安装的包都装到哪个目录中去了呢？

答案是：```/usr/local/lib/python2.7/site-packages```和```/usr/local/lib/python3.5/site-packages```下面

## 其他情况、杂项

如果之前自行手动安装过Python官网的dmg包，或者用系统的Python安装过其他东西，例如用系统自带的Python，安装了pip。

而上面说过，**这种方式不推荐，而是推荐Homebrew**，现在想卸载掉原来安装的，然后再用Homebrew安装，以保证系统Python的纯净，那该怎么办呢？

* 用老方式安装过了pip

	```sudo easy_install pip```: 安装路径在。。。。。(个人猜测：```/Library/Python/2.7/site-packages```)，根据安装路径进去找对应文件，删掉。


* 用老方式安装的pip安装了virtualenv

	```sudo pip install virtualenv```:安装路径在。。。。。(个人猜测：```/Library/Python/2.7/site-packages```)，根据安装路径进去找对应文件，删掉。

* 用老方式安装了Python3

	如果去Python官网下载了Python3的dmg包安装了Python3，现在想卸载干净怎么办？

	结合suspicious package这个软件就可以删干净了(前提是原安装包还在)



## 安装MySQL

通过Homebrew安装：```brew install mysql```

手动开启MySQL服务：

1. ```mysql.server start```; 
2. ```mysql -uroot -p```; 
3. ```输入密码(初始没有密码的情况下直接回车)```

如果想配置开机自启动以及设置成自启动后想取消自启动，进行如下操作：

```java
$ cp /usr/local/Cellar/mysql/5.6.16/homebrew.mxcl.mysql.plist ~/Library/LaunchAgents/  
#5.6.16是数据库版本号，根据你当时所安装的版本号自己修改

#start
launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist

#stop
launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
```

安装好后，MySQL的root用户默认是没有密码，如果想设置密码，可以进行如下操作：```set password for root@localhost = password('XXXXX'); ```

# 安装MySQL驱动

目前,有两个 MySQL 驱动:

* mysql­-connector-­python:是 MySQL 官方的纯 Python 驱动;
* MySQL­python:是封装了 MySQL C 驱动的 Python 驱动。

可以两个都装上，使用的时候再决定用哪个：

* pip install mysql­-connector-­python

	> * 如果失败，改成这样```pip install mysql-connector-python --allow-external mysql-connector-python```

	> * 如果依然失败，需要改成这样：```pip install --extra-index-url https://pypi.python.org/pypi/mysql-connector-python/2.0.4 mysql-connector-python```
	
	> * 如果上面都失败的话，就这样：```pip install https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.1.4.tar.gz```
	
* pip install mysql-python

**注意：** 在拿到数据库链接这一步，二者的用法稍微不同：

* mysql­-connector-­python

	```python
	import mysql.connector
	conn = connector.connect(......)
	```

* mysql-python

	```python
	import MySQLdb
	conn = MySQLdb.connect(......)
	```


# Mac下Ruby环境

还没写，待补充，可暂时参见[Ruby的杂项](http://blog.csdn.net/chenyyhh92/article/details/53232816)。。。

## native extension报错的解决办法

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-6792600b8442ef24?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# Mac好用的编辑器

除了vim和emacs，其他的人气高的、公认好用的编辑器有：

* VS Code
* Sublime Text 3
* Textmate 2

## VS Code

目前个人感觉它的vim插件不太好用，其他的目前没发现什么不爽的地方。

原生可以在编辑器里预览MarkDown，这个简直不能太爽！！！

另外，它的插件安装在：```~/.vscode/extensions/```目录下

## Sublime Text 3

按照个人的习惯和品位，还是更喜欢VS Code。

Sublime我比较欣赏的是，不需要任何插件，配置一下配置文件就有vim模式。

Sublime的插件安装目录在：```~/Library/Application Support/Sublime Text 3/Packages```目录下

## TextMate 2

Mac下大名鼎鼎的编辑器！

我个人用得较少，因为其vim插件“textmatevim”只支持TextMate 1，不支持TextMate 2。用习惯了vim模式，离开了它确实不太习惯。所以我用得少。

# Mac的```~/Library```

这个目录下放的是个人用户的资源库。
> 可以类比```/Library```：放的是系统的资源库

```~/Library```下有个```Application Support```目录，这个目录放了个人用户应用程序相关的数据以及支持文件，比如第三方的插件、帮助应用、模板等。
> **注意** ，有些软件的插件放在这个目录下。比如我如果装了JetBrains家的某些IDE，可能还会装个```IDEA Vim```插件，该插件就在这个目录下。

## 其他重要目录

结合上面提到的Python的一些目录的情况，加上Unix/Linux系统的一些基础知识，就可以自行推知其他重要目录的作用。

# Mac下的emacs

我们都知道，Mac下是自带了emacs的。而Ruby的安装会引入emacs。它们都分别装在哪里呢？来看一下。

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-91dd5082f60f176c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中打红框的是系统自带的emacs，没打的是由于Ruby引入的。

> Ruby受Lisp影响很大，Ruby之父的Lisp水平也很高，他自己也明确表示过很喜欢Lisp，个人猜想有这个原因？

# Mac自带的Python以及Ruby等

##  ```/Library/Python/```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-64825891ac5e0dab?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

## ```/System/Library```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-82e35f6846eef934?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

## ```/System/Library/Frameworks```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-250b9a36b97881c3?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

## ```/System/Library/Frameworks/Python.framework```

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-b3bad13660b31387?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

其他自带的一些东西，可以举一反三。

# Mac删干净VMware Fusion 8.5

## 方法一：手动删

手动删除下面这些文件（版本不同可能有点出入，不过不要紧，就是把相关文件删除干净的意思）：

* /Library/Application Support/VMware
* /Library/Application Support/VMware Fusion
* /Library/Preferences/VMware Fusion
* ~/Library/Application Support/VMware Fusion
* ~/Library/Caches/com.vmware.fusion
* ~/Library/Preferences/VMware Fusion
* ~/Library/Preferences/com.vmware.fusion.LSSharedFileList.plist
* ~/Library/Preferences/com.vmware.fusion.LSSharedFileList.plist.lockfile
* ~/Library/Preferences/com.vmware.fusion.plist
* ~/Library/Preferences/com.vmware.fusion.plist.lockfile
* ~/Library/Preferences/com.vmware.fusionDaemon.plist
* ~/Library/Preferences/com.vmware.fusionDaemon.plist.lockfile
* ~/Library/Preferences/com.vmware.fusionStartMenu.plist
* ~/Library/Preferences/com.vmware.fusionStartMenu.plist.lockfile

## 方法二：软件删结合手动删

推荐软件：APPdelete

用该软件删完后，再手动查找上面列出的东东，没删掉的话删干净即可。

> 一般这种删软件的APP，对于家目录下的关联文件夹基本都能删干净，所以这里手动检查的时候，重点检查非家目录下的文件(夹)。
