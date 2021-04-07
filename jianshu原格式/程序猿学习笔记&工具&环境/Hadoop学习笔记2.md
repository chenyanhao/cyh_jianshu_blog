# Hadoop 2.x产生背景

* Hadoop 1.0种的HDFS和MR在高可用、扩展性等方面存在问题；
* HDFS存在的问题：
	* NameNode单点故障，难以应用于在线场景；
	* NameNode压力过大，且内存受限，影响系统扩展性。
* MR存在的问题：
	* JobTracker访问压力大，影响系统扩展性；
	* 难以支持除MR之外的计算框架，比如Spark、Storm等。

**Hadoop 1.x 与 Hadoop 2.x**

结构如图所示：

![Hadoop 1 and 2](http://upload-images.jianshu.io/upload_images/1936544-205e516f50d717a3?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Hadoop 2.x 由HDFS、MR和YARN三个分支构成：

* HDFS：NN Federation、HA
* MR：运行在YARN上的MR
* YARN：资源管理系统


**HDFS 2.x**

* 解决HDFS 1.0种单点故障和内存受限问题
    * 解决单点故障
        * HDFS HA：通过主备NameNode解决
        * 如果主NN发生故障，则切换到备NN上
    * 解决内存受限问题
        * HDFS Federation(联邦)
        * 水平扩展，支持多个NN
        * 每个NN分管一部分目录
        * 所有NN共享所有DN存储资源
* 2.x仅仅是架构上发生变化，使用方式不变
* 对HDFS使用者透明
* HDFS 1.x种的命令和API仍可以使用

## HDFS 2.x HA

![HDFS 2.x HA大观](http://upload-images.jianshu.io/upload_images/1936544-4d884dd666ad546e?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 主备NN
	* 从JournalNodes集群中读写元数据
* 解决单点故障
	* 主NN对外提供服务，备NN同步主NN元数据，以待切换
	* 所有DN同时向两个NN汇报数据块信息
* 两种切换选择
	* 手动切换：通过命令实现主备之间的切换，可以用于HDFS升级等场合
	* 自动切换：基于Zookeeper实现
* 基于Zookeeper自动切换方案
	* 客户端不直接请求NN，而是去请求ZK。
	* ZK FailoverController：监控NN健康状态，并向ZK注册NN
	* NN挂掉后，ZKFC为NN竞争锁，获得ZKFC锁的NN变为Active状态
	* ZKFC必须和NN在同一台机器上

## HDFS 2.x Federation

![HDFS 2.x Federation大观](http://upload-images.jianshu.io/upload_images/1936544-dc22db3193c6b8ca?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 通过多个NN/namespace把元数据的存储和管理分散到多个节点中，使得NN/namespace可以通过增加机器来进行水平扩展。

* 能把单个NN的负载分散到多个节点中，在HDFS数据规模较大的时候也不会降低HDFS的性能。

* 可以通过多个namespace来隔离不同类型的应用，把不同类型应用的HDFS元数据的存储和管理分派到不同的NN中。

## YARN：Yet Another Resource Negotiator

* Hadoop 2.0新引入的资源管理系统，直接从MRv1演化而来的
    * 核心思想：将MRv1中的JobTracker的资源管理和任务调度两个功能分开
    * ResourceManager：负责整个集群的资源管理和调度
    * ApplicationMaster：负责应用程序相关的事务，比如任务调度、任务监控和容错等(最好跟DN在同一台机器)
    
* YARN的引入，使得多个计算框架可运行在一个集群中
    * 每个应用程序对应一个ApplicationMaster
    * 目前多个计算框架可以运行在YARN上，比如MR、Spark、Storm等。

**MapReduce On YARN**

> 有了YARN，就不再有JobTracker和TaskTracker了。

* MapReduce On YARN：MRv2
* 将MR作业直接运行在YARN上，而不是由JobTracker和TaskTracker构建的MRv1系统中
* 基本功能模块
	* YARN：
	* MRAppMaster：
	* MapTask/ReduceTask：
* 每个MR作业对应一个MRAppMaster
	* MRAppMaster任务调度
	* YARN将资源分配给MRAppMaster
	* MRAppMaster进一步将资源分配给内部的任务
* MRAppMaster容错
	* 失败后，由YARN重新启动
	* 任务失败后，MRAppMaster重新申请资源


# ZooKeeper的作用

用来保证数据在zk集群之间的数据的事务性一致。

## 搭建ZooKeeper服务器集群(具体的参见官网)

1. 确定分布式集群结构：
	> zk服务器集群规模不小于3个结点，要求各服务器之间系统时间要保持一致。
2. 在hadoop0的```/usr/local```目录下，解压缩zk.tar.gz，设置环境变量。
3. 在```/usr/local/zk/conf```目录下，修改文件：```vi zoo_sample.cfg```，并将其重命名为```zoo.cfg```
	* 修改```dataDir=/usr/local/zk/data```
		> 默认改之前是```/tmp/data```，而```/tmp```随着机器重启，就会销毁，因此不安全，所以要修改此处。
	* 新增```server.0=hadoop0:2888:3888```，```server.1=hadoop1:2888:3888```，```server.2=hadoop2:2888:3888```
4. 创建文件夹：```mkdir /usr/local/zk/data```，并在data目录下，创建文件myid，值为0.
5. 分别在其他结点，重复2-4的逻辑：
	* 把zk目录复制到hadoop1和hadoop2种。
	* 把hadoop1和hadoop2中相应的myid的值对应改为1和2。
6. 启动集群中的各个机器：
	* cd到bin目录下；
	* 执行命令```zkServer.sh start```；
	* 启动剩下的参与集群机器。
		> 验证：在三个结点上分别执行命令```zkServer.sh status```；

启动所有集群后，它们之间会通信，根据“选举算法”选举出Leader。


# HBASE

## Hadoop生态圈

![Hadoop生态](http://upload-images.jianshu.io/upload_images/1936544-94d49e5d8ba193fa?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* Hadoop官网：```hadoop.apache.org```
* Zookeeper官网：```zookeeper.apache.org```
* HBase官网：```hbase.apache.org```

## HBase简介

* HBase其全称叫做Hadoop DataBase，是一个高可靠、高性能、 **面向列** 、可伸缩、 **实时读写** 的分布式数据库。

* HBASE利用Hadoop HDFS作为其文件存储系统，利用Hadoop MapReduce来处理HBASE中的海量数据，利用Zookeeper作为协调工具。

* 主要用来存储非结构化和半结构化的松散数据(列存NoSQL数据库)

> 前面提到过，MR是一个离线的计算框架。它不是实时的，它是在计算好了数据后，将其放在HDFS中，以供后面查询以及使用。因此从这里可知，一般什么数据会放在HBase中呢？答案是，比如通话记录、账单记录、微博QQ微信的聊天信息等，这些都是放在HBase中。

## HBase数据模型

![HBase数据模型](http://upload-images.jianshu.io/upload_images/1936544-7bcf7c0b5949a692?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 是一行数据，而不是三行。
* 为什么会有时间戳呢？因为HBase依托于HDFS，而HDFS不让修改数据，所以HBase用时间戳来记录修改的情况，每次修改都对应一个新增的版本。
* CF1叫做列族，同理，CF2也叫做列族，CF3也叫做列族。依此类推。
* 图中每个单元格叫一个```cell```。要定位一个cell,需要三样东西：
	* 哪个Row-Key下
	* 哪个列族下
	* 哪个版本下

## 数据模型详解

* Column Family列族 & qualifier列
    * HBase表中每个列都归属于某个列族，列族必须作为表模式(scheme)定义的一部分预先给出。如```create 'test', 'course'```
    * 列名以列族为前缀，每个“列族”都可以有多个列成员(column)；如```course:math, course:english```，新的列族成员(列)可以随后按需、动态加入
    * 权限控制、存储以及调优都是在列族层面进行的
    * HBase把同一列族里面的数据存储在同一目录下，由几个文件保存
* Timestamp时间戳
    * 在HBase每个cell存储但愿对同一份数据有多个版本，根据唯一的时间戳来区分每个版本之间的差异，不同版本的数据按照时间倒序排序，最新的数据版本排在最前面
    * 时间戳的类型是64位整形
    * 时间戳可以有HBase(在数据写入时自动)赋值，此时时间戳是精确到毫秒的当前系统时间
    * 时间戳也可以由客户显示赋值，如果应用程序要避免数据版本冲突，就必须自己生成具有唯一性的时间戳
* Cell单元格
	* 由行和列的坐标交叉决定
	* 单元格是有版本的
	* 单元格的内容是未解析的字节数组，且是以key/value的形式进行存储的
		* key由```{row-key, column(=<family>+<qualifier>), version}```组成；value就是存储的数据。
		* cell中的数据是没有类型的，全部是字节形式存储。
* HLog(WAL log)：记录了对HBase读写操作的日志
	* HLog文件就是一个普通的Hadoop Sequence File
	* Sequence File的Key是HLogKey对象，HLogKey中记录了写入数据的归属信息。除了table和region名字外，同时还包括sequence number和timestamp，timestamp似乎“写入时间”，sequence number的起始值为0，或者是最近一次存入文件系统中sequence number
	* Sequence File的Value是HBase的Key/Value对象，即对应HFile中的Key/Value


## HBase架构体系

![HBaseArch1](http://upload-images.jianshu.io/upload_images/1936544-29b88a6fdffa292d?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> **注意：** 图中有两处错误(虽然是官方给的图)
> **第一处错在HLog有多份** ，**第二处错在HLog属于HRegion** 。正确的应该是：每一个HRegionServer只有一个HLog，而不是像图中画的那样有多个；HLog属于HRegionServer，而不是像图中画的那样属于HRegion

* HBase中主节点叫HMaster，从节点叫HRegionServer
* 什么是HRegion？答案是，对表中的数据进行横向切分(按行切)，就得到一个个的Region
* 每一个Store对应一个列族，Store分为两种，一种是MemStore，一种是StoreFile
	* MemStore在内存中，StoreFile在磁盘上 (这样做的原因类比关系数据库，每次读写先写在内存中，然后读写达到一定量或者到一定时间间隔后，再将内存中的数据刷入磁盘。这样一方面有利于提高读写效率；另一方面HDFS不适合存储小数据。) (从这个意义上说，StoreFile是MemStore溢写产生的。)
	* StoreFile中的数据是需要存到HDFS上的，存到HDFS上的那些文件我们称之为HFile。所以StoreFile里面有HFile的元数据信息。
* Client：包含访问HBase的接口并维护cache来加快对HBase的访问
* Zookeeper
	* 保证任何时候，集群中有且只有一个Master
	* 存储所有Region的寻址入口
	* 实时监控RegionServer的上线和下线信息，并实时通知Master
	* 存储HBase的scheme和table元数据
* Master
	* 为RegionServer分配Region
	* 负责RegionServer的负载均衡(将新增的Region放到负载较低的RegionServer上去)(因此Master只能解决新插入数据的负载均衡，而不能解决全局的负载均衡)
	* 发现失效的RegionServer并重新分配其上的region
	* 管理用户对table的增删改操作
* RegionServer
	* RegionServer维护region，处理对这些region的IO请求
	* RegionServer负责切分在运行过程中变得过大的region
* Region
	* HBase自动把表水平划分成多个区域(region)，每个region会保存一个表里面某段 **连续的** 数据
	* 每个表一开始只有一个region，随着数据不断插入，region不断增大；当增大到一个阈值的时候，region就会等分为两个新的region(裂变)
    * 当table中的行不断增多，就会有越来越多的region。这样一张完整的表被保存在多个RegionServer上
* MemStore与StoreFile
	* 一个region由多个store组成，一个store对应一个CF(列族)
	* store包括位于内存中的MemStore和位于磁盘的StoreFile
	* 写操作先写入MemStore，当MemStore中的数据达到某个阈值，HRegionServer会启动FlashCache进程写入StoreFile，每次写入形成单独的一个StoreFile
	* 当StoreFile文件的数量增长到一定阈值后，系统会进行合并(两种合并：minor compaction和major compaction)，在合并过程中会进行版本合并和删除工作(major compaction的时候才会删，minor compaction时不删)，形成更大的StoreFile
	* 当一个Region所有的StoreFile的大小超过一定阈值后，会把当前的Region分割成两个，并有HMaster分配到相应的RegionServer服务器，实现负载均衡
	* 客户端检索数据，现在MemStore，找不到再找StoreFile

**再看region**

![再看region](http://upload-images.jianshu.io/upload_images/1936544-d17ceda668468ef1?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* HRegion是HBase中分布式存储和负载均衡的最小单元。最小单元就表示不同的HRegion可以分布在不同的HRegionServer上
* HRegion由一个或者多个Store组成，每个Store保存一个columns family
* 每个Store又由一个MemStore和0至多个StoreFile组成
* StoreFile以HFile格式保存在HDFS上


**再看HBase架构**

![再看HBase架构](http://upload-images.jianshu.io/upload_images/1936544-e8e593ce83640491?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 这个架构图画得就很正确了，可以和前面那个有两处小错误的架构图对比。


## 完全分布式HBase和Zookeeper

一个完全分布式运行的HBase依赖一个zookeeper集群。所有的节点和客户端都必须能够访问zookeeper。默认情况下HBase会管理一个zookeeper集群(HBase自带一个zookeeper)，这个集群会随着HBase的启动而启动。

当然，也可以让HBase依赖已有的zookeeper集群，但需要配置HBase(具体的配置参见zookeeper官网)。

**需要几个zookeeper**

* 运行一个zookeeper也是可以的，但是在生产环境中，最好部署3/5/7个节点。部署的越多，可靠性就越高，当然只能部署奇数个，偶数个是不可以的。
* 需要给每个zookeeper 1GB左右的内存，如果可能的话，最好有独立的磁盘(独立磁盘可以确保zookeeper高性能)。
* 如果集群负载很重，不要把zookeeper和RegionServer运行在同一台机器上(就像DataNodes和TaskTrackers一样)。

**HBase启动**

* 在哪台机器启动集群，HMaster就在哪台机器上启动
* 启动完集群后，可以再去其他机器上再启动一个或多个HMaster

> 例如，有4个HBase节点，分别是node1/node2/node3/node4；
> 在node1上启动集群，则node1上会先启动HMaster，然后分别在node1/node2/node3/node4上启动RegionServer(此时node1上有HMaster和RegionServer，node2/node3/node4上各有一个RegionServer)；
> 此后，可以再在比如node4上，执行命令```./hbase-daemon.sh start master```，则node4上会再启动一个HMaster进程(此时node1/node2/node3上的进程如前，node4上会多一个HMaster进程)。


## HBase应用难点

* 表结构怎么设计
* HBase怎么优化
