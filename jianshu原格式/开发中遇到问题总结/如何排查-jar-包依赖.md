# 吐槽在前

依赖冲突之类的，是个很蛋疼的问题。感觉在不远、较远、非常远的将来，也很难解决。为什么呢，这是个哲学问题，哲学问题还是交给哲学家去解决。。。
大到各个 Unix / Unix-like 发行版，例如 Unix 的 make、Ubuntu 的 apt-get、Mac OSX 的 Macport / homebrew；
小到各个编程语言，例如 Java 的 maven、Python 的 pip、Ruby 的 gem、Scala 的 sbt 等等。
反正上面提到的这些，不管工业中用的多么广、设计理念多么好，都有很多被诟病的地方，只是程度不同罢了。
这也从侧面说明，依赖管理是个很蛋疼的东西，要不然开源界那帮大牛们早把这解决了。
排查起来就更蛋疼了。
maven 还算坑少点的，所以 maven 项目的依赖排查相对与其他工具例如 pip、gem 等，不知道高到哪里去了。能够 user-friendly 一些。


# 问题描述

这次又遇到了 slf4j 版本冲突问题，记录一下，免得后面再遇到忘记怎么解决。。。

报错是，
```java
java.lang.IllegalAccessError: tried to access field org.slf4j.impl.StaticLoggerBinder.SINGLETON from class org.slf4j.LoggerFactory
    at org.slf4j.LoggerFactory.<clinit>(LoggerFactory.java:57)
    at org.apache.commons.logging.impl.SLF4JLogFactory.getInstance(SLF4JLogFactory.java:156)
    at org.apache.commons.logging.impl.SLF4JLogFactory.getInstance(SLF4JLogFactory.java:132)
    at org.apache.commons.logging.LogFactory.getLog(LogFactory.java:685)
    ......
```
重点是这一行，
```java
at org.slf4j.LoggerFactory.(LoggerFactory.java:57)
```
追进去代码，
```java
loggerFactory = StaticLoggerBinder.SINGLETON.getLoggerFactory();
```
这行代码访问 StaticLoggerBinder.SINGLETON，
```
public class StaticLoggerBinder implements LoggerFactoryBinder {
    private static final StaticLoggerBinder SINGLETON = new StaticLoggerBinder();
    ......
}
```
这玩意儿是 private 的，没法这样访问。
出现这个问题的原因是 JAR 包冲突，咱们的项目中，slf4j 有些包是 1.3.1，有些包是1.6.2，当它们和 1.3.1 配合的时候，就会出现这个问题。




# 问题解决

排查思路是，首先找到 org.slf4j.LoggerFactory 和 org.slf4j.impl.StaticLoggerBinder 这两个类是哪个 jar 包加载的，然后再找加载它们的 jar 包是由其他哪个 jar 依赖并加载的。大致思路如下，

虚拟机带上参数 `-verbose:class`  启动，这样会把类的加载情况都打印出来。省略无关内容、并重点关注 1.3.1 版本，可以看到，
```
[Loaded org.slf4j.LoggerFactory from file:/Users/yj/.m2/repository/org/slf4j/com.springsource.slf4j.api/1.3.1/com.springsource.slf4j.api-1.3.1.jar]
[Loaded org.slf4j.spi.LoggerFactoryBinder from file:/Users/yj/.m2/repository/org/slf4j/com.springsource.slf4j.api/1.3.1/com.springsource.slf4j.api-1.3.1.jar]
[Loaded org.slf4j.impl.StaticLoggerBinder from file:/Users/yj/.m2/repository/org/slf4j/slf4j-log4j12/1.6.2/slf4j-log4j12-1.6.2.jar]
```

可以看到，罪魁祸首是这个：com.springsource.slf4j.api-1.3.1.jar。1.3.1 和 1.6.2 冲突了。

接着排查依赖树，看看是谁依赖这个它。执行命令，`mvn dependency:tree >> haha.txt` ，然后打开 `haha.txt`，搜索关键字 `com.springsource.slf4j.api` ，可以看到，例如，

![image](https://upload-images.jianshu.io/upload_images/1936544-e3d7b9b463b40977.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

需要注意的是，要在 **最上级（而不是被排除的 jar 的直接父级 jar）** 的 jar 中排除掉不想要的依赖，即，

```
// 最上级中排除
<dependency>
   <groupId>com.alipay.sofa.service</groupId>
   <artifactId>sofa-service-api</artifactId>
   <exclusions>
      <exclusion>
         <groupId>org.slf4j</groupId>
         <artifactId>com.springsource.slf4j.api</artifactId>
      </exclusion>
   </exclusions>
</dependency>



// 而不是这样
<dependency>
   <groupId>com.alipay.cloudengine.kernel</groupId>
   <artifactId>com.alipay.cloudengine.kernel.osgi</artifactId>
   <exclusions>
      <exclusion>
         <groupId>org.slf4j</groupId>
         <artifactId>com.springsource.slf4j.api</artifactId>
      </exclusion>
   </exclusions>
</dependency>
```

同理，一个一个搜索，解决一下即可。








