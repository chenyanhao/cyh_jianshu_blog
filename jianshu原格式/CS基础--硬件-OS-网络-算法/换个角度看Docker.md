
docker学习最大的障碍，不是网上的资源太少，而是网上的资源太多，资源太多带来的噪声让学习效率降低不少。而在讲解docker原理上，所有的讲解都是关于cgroups，namespace，aufs以及deviceMapper，这对于一个初学者来说，就是用一堆名词替换另一堆名词。在这篇解析中，将不会讨论：

* 一堆堆砌在一起的专有名词，让阅读者云里雾里
* 一大堆写满了专有名词的图，但是不给太多解释


这篇解析将会涉及：

* 虚拟机的实现原理
* 虚拟机和容器的区别

在开始讨论前，先抛出一些问题，可先别急着查看答案，讨论的过程可以让答案更有趣，问题如下：

* [Docker 容器有自己的kernel吗](https://superuser.com/questions/889472/docker-containers-have-their-own-kernel-or-not)
* [docker的kernel version由镜像确定还是由宿主机确定](https://groups.google.com/forum/#!topic/docker-user/IDz4iQ15t0A)


# 虚拟机

先来理解一下虚拟机概念，广义来说，虚拟机是一种模拟系统，即在软件层面上通过模拟硬件的输入和输出，让虚拟机的操作系统得以运行在没有物理硬件的环境中（也就是宿主机的操作系统上），其中能够模拟出硬件输入输出，让虚拟机的操作系统可以启动起来的程序，被叫做hypervisor。用一张图来说明这个关系就是：

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-0881e3358dc25942?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在这张图中：

* 物理机被称为宿主机
* 虚拟机也被称为guest OS
* 被hypervisor虚拟出来的硬件被称为虚拟硬件

比如，举一个大家都很熟悉的例子，在编写android程序时，调试和测试运行都可以在X86架构的台式机或笔记本进行，这就是一个典型的虚拟机例子，在这之中：

* 宿主机就是台式机或笔记本
* 虚拟机就是虚拟出来的android
* 而模拟android的软件就是android box

当然android模拟机一个大问题就是：启动速度非常慢，最长可达10分钟或以上，这是因为单纯模拟硬件的输入输出，效率是很差的，所以这样的虚拟机如果真部署在服务器上，速度是感人的。

这个时候，就有计算机科学家提出了非常偷懒的想法：假如我们不模拟硬件输入输出，只是做下真实硬件输入输出的搬运工，那么虚拟机的指令执行速度，就可以和宿主机一致了。当然这前提是宿主机的硬件架构必须和虚拟硬件架构一致。比如，

* 我们可以在linux的台式机上轻松模拟windows，而且这个windows的运行速度基本上和原生装一个windows速度差不多，因为windows也能被直接安装在这台台式机上。
* 这个思路对于在windows系统中运行android系统不管用，因为android系统的运行硬件一般是手机（arm系统，可以理解为不同的硬件架构体系和cpu指令集），所以android模拟机还是一样的慢。

由于本篇并不是主要关于虚拟机的内容，所以这些点就点到而止。

# 容器的概念

一般来说，虚拟机都会有自己的kernel，自己的硬件，这样虚拟机启动的时候需要先做开机自检，启动kernel，启动用户进程等一系列行为，虽然现在电脑运行速度挺快，但是这一系列检查做下来，也要几十秒，也就是虚拟机需要几十秒来启动。

* 重新来理解虚拟机的概念，计算机科学家发现其实我们创建虚拟机也不一定需要模拟硬件的输入和输出，假如宿主机和虚拟机他们的kernel是一致的，就不用做硬件输入输出的搬运工了，只需要做kernel输入输出的搬运工即可，为了有别于硬件层面的虚拟机，这种虚拟机被命名为 操作系统层虚拟化：[Operating-system-level virtualization](https://en.wikipedia.org/wiki/Operating-system-level_virtualization)，也被叫做容器

* 让我们来回顾虚拟机的概念，在虚拟机的系统中，虚拟机认为自己有独立的文件系统，进程系统，内存系统，等等一系列，所以为了让容器接近虚拟机，也需要有独立的文件系统，进程系统，内存系统，等等一系列，为了达成这一目的，主机系统采用的办法是：只要隔离容器不让它看到主机的文件系统，进程系统，内存系统，等等一系列，那么容器系统就是一个接近虚拟机的玩意了

至此就可以回答引言提到的两个问题：

```
Q: Docker 容器有自己的kernel吗?
A: 没有，docker和宿主机共享kernel

Q: docker的kernel version由镜像确定还是由宿主机确定
A: 由宿主机决定
```


# 容器实现细节
 
接下来讨论linux启动流程 中，容器需要使用其中的几步？

linux的启动流程如下图：

![这里写图片描述](http://upload-images.jianshu.io/upload_images/1936544-28b8e143e1d6310d?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 先从fork说起

在讲解容器之前，先来谈谈linux实现进程的原理，linux实现进程的方法为fork，实现的方式分为两个步骤：

1. 在内存中复制一个父进程，得到“子进程”，此时子进程就是父进程上下文的简单克隆，内容完全一致
2. 设置子进程的 pid，parent_pid，以及其他和父进程不一致的内容

# namespace让进程隔离更灵活

从进程被制造的步骤可以看出，进程大部分资源和父进程共享，如果需要制造一个看起来像虚拟机的进程，我们需要比普通的进程多做几步。

* 可以自定义rootfs，比如我们把整个ubuntu发行版的可执行文件以及其他文件系统都放在目录/home/admin/ubuntu/ 下，当我们重定义rootfs = /home/admin/ubuntu 后，则该文件地址被印射为 "/"
* 把自身pid 印射为0，并看不到其他任何的pid，这样自身的pid成为系统内唯一存在pid，看起来就像新启动了系统
* 用户名隔离，可以把用户名设置为“root”
*  hostname隔离，可以另取一个hostname，成为新启动进程的hostname
* IPC隔离，隔离掉进程之间的互相通信
* 网络隔离，隔离掉进程和主机之间的网络

如果做完这几步，至少在进程自身看来，和虚拟机执行环境上已经区别不大了，对应到linux系统中，这几个隔离需要的方法：[clone(2) - Linux manual page](http://man7.org/linux/man-pages/man2/clone.2.html)

而clone方法和fork方法，在复制上下文的时候，调用的都是syscall_clone() 本质上它们是差不多的。

# 其实docker是一个内核的搬运工

所以虽然docker帮助我们准备好了rootfs地址，镜像里面的文件，以及各种资源隔离的配置，但是在启动一个容器的时候，它只是调用系统中早已内置的可以隔离资源的方法，而kernel支持这些方法，也是在创建进程的方法上做了一层资源隔离的扩展而已。

这就解释了docker两个特性：

* 启动速度快，因为本质来说容器和进程差别没有想象中的大，共享了很多代码，流程也差的不多
* linux内核版本有最低的要求，因为linux是在某个版本后开始支持隔离特性


# One more thing

让我们再来看看前面提出的问题：```linux启动流程 中，容器需要使用其中的几步？```

看完了fork，clone以及一大堆隔离后，相信很容易有答案了，这中间容器做完了隔离之后就算启动完毕，根本就不会来做kernel init之类的步骤，所以答案是一步都不用。

# learn more

* 比较除docker外其他的容器类产品，如coreOS，LXC
* 了解linux如何做隔离，请参考：[namespaces(7)](http://man7.org/linux/man-pages/man7/namespaces.7.html)
* 了解freebsd如何做隔离，请参考：[freebsd jail](https://www.freebsd.org/doc/handbook/jails.html)
* docker 真正想做的事情是把资源隔离的接口标准化（最新的版本里windows的接口也被抽象到了docker自己的体系），严格说它是所有相似资源隔离的一层抽象和搬运工
* docker 镜像很小的优势，主要是靠AUFS实现的
