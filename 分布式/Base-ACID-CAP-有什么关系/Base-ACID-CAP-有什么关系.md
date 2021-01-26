

A：
When applying CAP (and other distributed system design principles) to design of any modern distributed system, certain architectural properties or guarantees will emerge. BASE is some sort of categorization of a class of systems that use/apply CAP in a similar manner, have a certain subset of common requirements (I am talking about architectural, not the functional requirements).

BASE stands for Basically Available Soft State and Eventually Consistent. Such systems have a huge focus on availability, high scalability, low client-server operation latency. Consistency is not a big requirement and is not looked as a MUST for the success of business goals. BASE is actually a result of applying CAP in a certain manner as desired by the requirements of a distributed system.


参考：https://www.quora.com/What-is-the-difference-between-CAP-and-BASE-and-how-are-they-related-with-each-other

# 个人赞同点

一、一些能帮助理解的小细节

- CAP适用于分布式的东西 (ACID 适用于本地存储) ；“BASE is one such design choice”，Base 是 CAP 的一个 design choice。
- ACID focuses on Consistency and availability （CA）.
- BASE focuses on Partition tolerance and availability and throws consistency out the window （AP）.

> 用自己的话总结一下就是：CAP 是道，ACID 和 BASE 是术。即 CAP 是普适的理论， ACID 和 BASE 是面对两种不同场景的 design choise。

二、深入理解 BASE

Base 源于 NOSQL 的理论中，下面两段话引证，

It’s harder to develop software in the fault-tolerant BASE world compared to the fastidious ACID world, but Brewer’s CAP theorem says you have no choice if you want to scale up. However, as Brewer points out in this presentation, there is a continuum between ACID and BASE. You can decide how close you want to be to one end of the continuum or the other according to your priorities.

Many of the NOSQL databases above all have loosened up the requirements on Consistency in order to achieve better Availability and Partitioning. This resulted in systems know as BASE (Basically Available, Soft-state, Eventually consistent). These have no transactions in the classical sense and introduce constraints on the data model to enable better partition schemes (like the Dynamo system etc). A more comprehensive discussion of CAP, ACID and BASE is available in this introduction.

三、需要注意的一个小点

注意一句话：CAP is basically a continuum along which BASE and ACID are on opposite ends.

这句话应该怎么理解呢？
ACID 和 BASE 是两个极端，前者为了一致性放弃了基本放弃了可用性，后者为了可用性基本放弃了较强一致性 (说法不准确，能意会意思就好) (这也是为什么 ACID 是 RDBMS 和 NewSQL 的代名词，而 BASE 是 NOSQL 的代名词)。
但是这两个极端之间存在一个连续性。根据各自业务的优先级，结合 CAP 理论进行一定的取舍，以决定想要接近某一端或另一端。







