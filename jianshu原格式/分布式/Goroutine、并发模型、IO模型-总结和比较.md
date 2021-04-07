最近 Go 实在是太火，确切说其实是协程火，让人禁不住想研究一下。Go 的卖点其实也就是 Channel 和 Goroutine 了。理解的核心在于两点：一个是 Channel 和 Goroutine 之间的协作关系，另一个是 Gotoutine 的调度。

观摩 Goroutine 后，还是感觉意犹未尽，好奇为什么要设计这个模型，这个模型解决什么痛点，还有什么其他的解决方案，因此引出了并发模型“历史”的挖掘。

而并发模型总是和 IO 模型联系在一起的，因此最后又复习了下 IO 模型清单。

结构安排：

1.  Channel 和 Goroutine 的协作关系

2.  Gotoutine 的调度

3.  并发模型“历史”

4.  IO 模型清单

# [](#85atlh)Channel 和 Goroutine 的协作关系

Channel 的基本目的就是在 Gotoutine 之间做同步，就像一个管道在 Goroutine 之间传递数据一样，使其可以无锁通信。

举个好理解的例子，上灵魂画手，

![image](https://upload-images.jianshu.io/upload_images/1936544-9c393a6f2a5bfd1e.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) 

图中传送带就是 Channel，食客和厨师就是 Goroutine，

*   如果食物在转盘上摆满了，厨师(发送 Goroutine)肯定放不下了，这时候他就拿着做好的食物默默等待，直到有食物被食客(接收 Goroutine)取走

*   如果转盘上没有食物，食客(接收 Goroutine)就只能眼睁睁阻塞着，直到厨师(发送 Goroutine)把食物放在转盘上

因此可以总结出一些基本性质：

Channel 是一个自动阻塞的管道，当 Channel 满了，发送 Goroutine 阻塞(因为放不下)；当 Channel 为空，接收 Goroutine 阻塞(因为拿不到)。

上图是有缓冲的 Channel，还有无缓冲的 Channel，如下图，即一对一服务，

![image](https://upload-images.jianshu.io/upload_images/1936544-617df6d0f4b73bbb.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

# [](#uomssf)Gotoutine 调度

先要从协程说起。协程据说是个很古老的概念，最开始是在编译界提出，词法解析器解析了一定的 token 时，就开始执行语法解析器，等语法解析器解析完这些的 token，再把控制权转交给词法解析器。这里让出控制流时，需要它们记住自身的状态，以便从上次执行的位置开始恢复。这就是协程的前身。这里的协程，和子程序调用的区别在于，**其控制流能够主动让出和恢复**。

Knuth 老爷子说过：“子程序是协程的特例。” 恩，老爷子说的很对啊。

然后复习下操作系统线程实现模型，一般的 OS 线程实现有 3  种模型
![图片.png](https://upload-images.jianshu.io/upload_images/1936544-d5f2108986543591.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


从理论上说，协程采用的是 N:1 模型，但是为了利用多核，一般工程实现还是 N:M，Goroutine 就是 N:M 模型，优点是既能实现协程，又能利用多核。

Go 调度器包含了 3 个角色：M、P、G，

*   **M** 代表系统 **线程**，也就是前面说的普通线程。

*   **P** 代表 **调度器**，我们可以把它当做单线程的本地调度器。（留意下这里，P 是实现 N:1 到 N:M 的关键）

*   **G** 代表 **Goroutine**，它包含了 ESP、PC 寄存器，以及其它调度相关信息。

![image](https://upload-images.jianshu.io/upload_images/1936544-c306b35c3f1ea97a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

上图是 2 个 线程（M），每个线程对应一个处理器（P），M 是必须关联 P 才能执行协程（G）的。图中蓝 G 代表的是运行中的 Goroutine，灰 G 表示的待执行的 Goroutine，

待执行的 Goroutine 存储在一个全局队列中，此时 P 执行 Goroutine 会这个队列中取，需要加锁，线程会经常阻塞等待锁。

前面提到 N：1 模型，一个线程系统调用阻塞会导致所有线程阻塞，那么如果其中一个 G 执行的时候，阻塞了（例如发生了系统调用）怎么办？

![image](https://upload-images.jianshu.io/upload_images/1936544-a3bcc7d2fd08420c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

上图左边，G0 中陷入系统调用，导致 M0 阻塞，接下来：

*   M0 放弃了它的 P，让 M1 去处理 P 中剩下的 Goroutine，这里的 M1 可能是在线程缓存中取的，或者运行中生成的。

*   当 M0 从系统调用中恢复，它会去别的 M 中找 P 来执行 G0（比如说别的 M 阻塞丢出了 P），如果没有 P，那么它会把 G0 放到全局队列中，并且把它自己放到线程缓存中。

*   全局队列保存了 Goroutine，当各自 P 中的局部队列没有 Goroutine 时，P 会到全局队列中取 Goroutine。并且即使 P 中局部队列有 Goroutine，也会周期性地从全局队列中取 Goroutine，保持全局队列中的 Goroutine 能够尽快被执行。

*   处理系统调用，也是 go 程序为什么跑在多线程上的一个原因，即使 GOMAXPROCS 是 1，也可能会有多个工作线程。

当 P 局部队列不均衡时怎么处理？如果有多个 P，其中一个 P 的局部队列 Goroutine 执行完了，

![image](https://upload-images.jianshu.io/upload_images/1936544-f882ab026fa02736.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

如果一个 P 局部队列为空，那么它尝试从全局队列中取 Goroutine，如全局队列为空，则会随机从其它 P 的局部队列中“挪一半” Goroutine 到自己的队列当中， 以保证所有的 M 都是有任务执行的，间接做到负载均衡。

虽然协程强调的是协作式调度，但是如果其中一个协程不够“合作”，不主动让出控制权，那么会导致这个线程一直被占用，降低并发度。如果一个 P 连续执行长时间，没有切换 G，怎么处理？

首先，Go 在启动时会创建一个系统线程，这个系统线程会监控所有 Goroutine 的状态。它是通过遍历所有的 P，如果 P 连续长时间执行，就会被抢占。表现为改 P 对应当前执行的 G 会被移除，放置到全局 Goroutine 队列中，然后 P 去捞新的 G 来执行。

# [](#yf4mbp)并发模型分类

*   共享内存模型：通过多线程和锁实现并发控制。**代表：Java**

*   CSP  模型：全称 Communication sequential process。由并发执行的 Processor(协程 or 线程 or 进程)和 Channel 组成，Processor 之间通过 Channel 发送消息进行通信。**代表：Go**

*   Actor 模型：Actor 是并发实体，Actor 之间通过 mailbox(是个逻辑概念) 发送消息来传送数据，消息传送是异步的。每个 Actor 相互独立且隔离。Actor 使用消息模型，每个 Actor 在同一时间处理最多一个消息，也可以发送消息给其他 Actor，保证了从而避免了多线程写争夺。**代表：Erlang、Scala**

# [](#11n2iy)CSP 和 Actor 的区别

CSP 中的 Process 和 Actor 很相似，Channel 概念也和 Actor 的 Mailbox 很相似，但它们还是有很大的区别：

*   CSP 进程通常是同步的(即任务被推送进 Channel 就立即执行，如果任务执行的线程正忙，则发送者就暂时无法推送新任务)，Actor 进程通常是异步的(消息传递给 Actor 后并不一定马上执行)

*   CSP 中的 Channel 通常是匿名的, 即任务放进 Channel 之后你并不需要知道是哪个 Channel 在执行任务，而 Actor 是有“身份”的，可以明确的知道哪个 Actor 在执行任务

*   在 CSP 中，只能通过 Channel 在任务间传递消息, 在 Actor 中可以直接从一个 Actor 往另一个 Actor 传输数据

*   CSP 中消息的交互是同步的，Actor 中支持异步的消息交互

*   理论上，每个 Actor **有且只有**一个 Mailbox，所以只需要向 Actor 的 Mail Address (标识符) 发消息；Channel 和 Process 之间没有从属关系，Process 可以订阅任意个 Channel，Process 没必要拥有标识符，只有 Channel 需要，因为只向 Channel 发消息

几个图对比 CSP 和 Actor ：

![image](https://upload-images.jianshu.io/upload_images/1936544-f60eb0d1bf65f065.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

![image](https://upload-images.jianshu.io/upload_images/1936544-691724ae60af1776.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

![image](https://upload-images.jianshu.io/upload_images/1936544-e302b0875fb4a3bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

总结：

*   Actor 之间直接通信，而 CSP 是通过 Channel 通信，后者更加松耦合。

*   同时，它们都是描述独立的进程通过消息传递进行通信。主要的区别在于：在 CSP 消息交换是同步的(即两个进程的执行"接触点"的，在此他们交换消息)，而Actor模型是完全解耦的，可以在任意的时间将消息发送给任何未经证实的接受者。由 Actor享有更大的相互独立,因为他可以根据自己的状态选择处理哪个传入消息。自主性更大些。

*   在 Go  语言中为了不堵塞进程，程序员必须检查不同的传入消息，以便预见确保正确的顺序。CSP 好处是 Channel 不需要缓冲消息，而 Actor 理论上需要一个无限大小的邮箱作为消息缓冲。

# [](#r6fsxh)并发模型发展史

了解发展史是了解一个领域最好的方式，历史能帮助回答我们的很多“为什么”。

**从这段历史也可以看到，复杂的抽象一定是有问题的、不长久的、不健全的甚至不正确的。因为编程也是不断在对现实世界做抽象，越贴近现实世界，抽象就越成功，而这个世界的哲学是很简单的。因此好的抽象一定是简单的，可能思考、设计、抽象的过程是很复杂的，但是最终的呈现面貌一定很简单。**

这里也会深入分析 CSP 和 Actor 的区别。

## [](#zko2gl)传统模型

首先，并发编程为什么这么蛋疼呢？引用 akka 的一句话：

*We believe that writing correct concurrent, fault-tolerant and scalable applications is too hard. Most of the time it’s because we are using the wrong tools and the wrong level of abstraction.*

> 之所以难，是因为我们用了错误的工具和错误的抽象。
> 
> 那 akka 的工具和抽象如何呢？看完历史自然就知道了~

接下来处理程序的抽象历史。

最开始的程序是面向过程的，数据结构 + 函数，以 C 语言为代表(其实那时候已经有 Lisp 这类语言了，只不过没火，暂时忽略，只考虑主流)。后来有了面向对象，对象组合了数据结构和函数，人们想用对象来模拟现实世界，抽象出对象，有状态和行为。

> 其实虽然现在 OO 一直处于主流，但是从我个人口味来说很不喜欢 OO 这个编程范式。基于封装的范式一般有三种，为了避免歧义，用英文来表示，分别是：data-abstraction、object-based、object-oriented。简要区别就是，C 语言是 data-abstraction，现代 C++ 的一种最佳实践是  object-based，Java/C# 这些是 object-oriented。因此第一种是值语义，后两种是对象语义，值语义更容易构建并发安全的程序。

但无论是面向过程的函数还是面向对象的函数，本质上都是代码块的组织单元，本身并没有包含代码块的并发策略的定义。于是为了解决并发的需求，引入了线程的概念。

线程的使用比较简单，如果这块代码需要并发，就把它放在单独的线程里执行，由系统负责调度，具体什么时候使用线程，要用多少个线程，由调用方决定，但定义方并不清楚调用方会如何使用自己的代码（比如 Java 的 HashMap 不是并发安全的，误用在多线程环境就会导致问题），这同时也带来了两个额外的复杂度，

*   race condition

*   依赖关系和执行顺序

> 为了解决前者，引入了一系列的 lock 如互斥锁、读写锁等（[锁的理解见这篇](https://lark.alipay.com/yanhao.cyh/ryn7l1/sin0m6)） 以及 一些特殊操作如 CAS；为了解决后者，引入了一系列基于条件原语构建的工具类如 CountDownLatch 等.

这真是解决了一个问题就引入另一个问题或者说带来了额外复杂度。如果说上面两个问题只是增加了复杂度，我们通过深入学习，严谨的 CodeReview，全面的测试，一定程度上能解决。（其实互斥器和条件变量是非常底层的原语，除非是系统和架构层面的开发才会使用，用它们来实现高层的同步措施，如 CountDownLatch、BlockingQueue 等，应用层次的开发中很少直接使用，这是后话）

但是这个模型有个问题一定是解决不了的，那就是 **系统里到底需要多少个线程？**

> **阻抗匹配原则并不是银弹。**

举个喂小孩子吃饭时判断小孩是否吃饱的例子：

![图片.png](https://upload-images.jianshu.io/upload_images/1936544-b691281c20b542b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


通过这个例子可以看出，从外部系统来观察，或者以经验的方式进行计算，都是非常困难的。于是结论就来了 **让孩子会说话，吃饱了自己说，自己学会吃饭，自管理**。

然并卵，计算机不会自己说话，如何自管理？

## [](#5ouuve)新的思路

有句老话叫做 **陈力就列，不能者止。**这句话是说，能干活的代码片段就放在线程里，如果干不了活（需要等待、被阻塞等），就拿掉。通俗的说就是不要占着茅坑不拉屎，如果拉不出来，需要酝酿下，先把茅坑让出来，因为茅坑是稀缺资源。

针对此，一般有两种方案：

1.  **异步回调方案：**以 nodejs 为典型代表。遇到阻塞的情况，如网络调用，则注册一个回调方法（其实还包括了一些上下文数据对象）给 IO 调度器（linux 下是 libev，调度器在另外的线程里），当前线程就被释放了，去干别的事情了。等数据准备好，调度器会将结果传递给回调方法然后执行，执行其实不在原来发起请求的线程里了，但对用户来说无感知。这种方式的问题就是很容易遇到 callback hell，因为所有的阻塞操作都必须异步，否则系统就卡死了。还有就是异步的方式有点违反人类思维习惯，人类还是习惯同步的方式。

2.  **Coroutine/Fibre：**以 goroutine 为典型代表**。**这种方案其实和上面的方案本质上区别不大，关键在于回调上下文的保存以及执行机制。为了解决回调方法带来的难题，这种方案的思路是写代码的时候还是按顺序写，但遇到 IO 等阻塞调用时，将当前的代码片段暂停，保存上下文，让出当前线程。等 IO 事件回来，然后再找个线程让当前代码片段恢复上下文继续执行，写代码的时候感觉好像是同步的，仿佛在同一个线程完成的，但实际上系统可能切换了线程，但对程序无感。

> Coroutine 是 Continuation 的一种实现，一般表现为语言层面的组件或者类库。主要提供 yield，resume 机制。
> 
> Continuation 是 FP 中的概念，可以理解为让我们的程序可以暂停，然后下次调用继续（contine）从上次暂停的地方开始的一种机制。可以理解为相当于程序调用多了一种入口。
> 
> Fibre 和 Coroutine 其实是一体两面的，主要是从系统层面描述，可以理解成 Coroutine 运行之后的东西就是Fibre。

Goroutine 很大程度上降低了并发的开发成本，是不是我们所有需要并发的地方直接 go func 就搞定了呢？

Go 通过 Goroutine 的调度解决了 CPU 利用率的问题。但遇到其他的瓶颈资源如何处理？比如带锁的共享资源，比如数据库连接等。互联网在线应用场景下，如果每个请求都扔到一个  Goroutine 里，当资源出现瓶颈的时候，会导致大量的 Goroutine 阻塞，最后用户请求超时。这时候就需要用 Goroutine 池来进行控流，同时问题又来了：池子里设置多少个 Goroutine 合适？

这又回到了前面的问题，所以这个问题还是没有从根本上解决。

## [](#q5vdcf)Actor 模型

Actor 的概念其实和 OO 里的对象类似，是一种抽象。面向对象编程对现实的抽象是对象 = 属性 + 行为，但当使用方调用对象行为的时候，其实占用的是调用方的 CPU 时间片，是否并发也是由调用方决定的。这个抽象其实和现实世界是有差异的。现实世界更像Actor的抽象，互相都是通过异步消息通信的。

举个例子，比如 A 对 B say hi，B 是否回应、如何回应是由 B 自己决定的，运行在 B 的大脑里，并不会占用 A 的大脑。

所以Actor有以下特征：

*   Processing – actor 可以做计算的，不需要占用调用方的CPU时间片，并发策略也是由自己决定

*   Storage – actor 可以保存状态

*   Communication – actor 之间可以通过发送消息通讯

Actor 遵循以下规则：

*   发送消息给其他的 Actor

*   创建其他的 Actor

*   接受并处理消息，修改自己的状态

Actor 的目标：

*   **可独立更新，实现热升级**。因为 Actor 互相之间没有直接的耦合，是相对独立的实体，可能实现热升级。

*   **无缝整合本地和远程调用**。因为 Actor 使用基于消息的通讯机制，无论是和本地的 Actor，还是远程 Actor 交互，都是通过消息，这样就弥合了本地和远程的差异。

*   **容错**。Actor 之间的通信是异步的，发送方只管发送，不关心超时以及错误，这些都由框架层和独立的错误处理机制接管。

*   **易扩展**。天然分布式因为 Actor 的通信机制弥合了本地和远程调用，本地 Actor 处理不过来的时候，可以在远程节点上启动 Actor 然后转发消息过去。

## [](#golang-csp-vs-actor)CSP VS Actor

**相同点**

二者的格言都是：*Don’t communicate by sharing memory, share memory by communicating*

它们都是通过消息通信的机制来避免竞态条件，但具体的抽象和实现上有些差异。

**不同点**

*   CSP 里消息和 Channel 是主体，处理器是匿名的。也就是说发送方需要关心自己的消息类型以及应该写到哪个 Channel，但不需要关心谁消费了它，以及有多少个消费者。Channel 一般都是类型绑定的，一个 Channel 只写同一种类型的消息，所以 CSP 需要支持 alt/select 机制，同时监听多个 Channel。Channel 是同步的模式（Golang 的 Channel 支持 buffer，支持一定数量的异步），背后的逻辑是发送方非常关心消息是否被处理，CSP 要保证每个消息都被正常处理了，没被处理就阻塞着。

*   Actor 里 Actor 是主体，Mailbox（类似于 CSP 的 Channel）是透明的。也就是说它假定发送方会关心消息发给谁消费了，但不关心消息类型以及通道。所以 Mailbox 是异步模式，发送者不能假定发送的消息一定被收到和处理。Actor 模型必须支持强大的模式匹配机制，因为无论什么类型的消息都会通过同一个通道发送过来，需要通过模式匹配机制做分发。它背后的逻辑是现实世界本来就是异步的、不确定的，所以程序也要适应面对不确定的机制编程。

从这样看来，CSP 的模式比较适合 Boss-Worker 模式的任务分发机制，它的侵入性没那么强，可以在现有的系统中通过 CSP 解决某个具体的问题。它并不试图解决通信的超时容错问题，这个还是需要发起方进行处理。同时由于 Channel 是显式的，很难做到对使用方透明。

而 Actor 则是一种全新的抽象，它试图要解决的问题要更广一些，比如容错、分布式。但 Actor 的问题在于以当前的 **调度效率**，哪怕是用 Goroutine 这样的机制，也很难达到直接方法调用的效率。当前要像 OO 的『一切皆对象』一样实现一个『一切皆Actor』的语言，效率上肯定有问题。所以折中的方式是在 OO 的基础上，将系统的某个层面的组件抽象为 Actor，算是目前采用较多的一种方式。

## [](#akx0bt)Rust 带来的思考

Rust 解决并发问题的思路是首先 **承认现实世界的资源总是有限的**，想彻底避免资源共享是很难的，不试图完全避免资源共享，它认为 **并发的问题不在于资源共享，而在于错误的使用资源共享**。比如大多数语言定义类型的时候，并不能限制调用方如何使用，只能通过文档或者标记的方式（比如 《Java Concurrency in Practice》 中常用的 @ThreadSafe ,@NotThreadSafe ）说明是否并发安全，但也只能仅仅做到提示的作用，不能阻止调用方误用。

所以 Rust 的解决方案就是：

*   定义类型的时候要明确指定该类型是否是并发安全的。

*   引入了变量的所有权（Ownership）概念。Rust 认为非并发安全的数据结构在多个线程间转移，也不一定就会导致问题，导致问题的是多个线程同时操作，也就是说是因为这个变量的所有权不明确导致的。有了所有权的概念后，变量只能由拥有所有权的作用域代码操作，而变量传递会导致所有权变更，从语言层面限制了竞态条件出现的情况。

> 有了这机制，Rust 可以在编译期而不是运行期对竞态条件做检查和限制。虽然开发的时候增加了心智成本，但降低了调用方以及排查并发问题的心智成本，也是一种解决方案。

# [](#x7f4fq)IO 模型清单

此清单也再现了 IO 模型（reactor 模型）的发展历史，从清单也可以看出，就是不断的“排列组合”。

表格中 “socket 互通” 指的是 多个连接之间能否方便地交换数据；

顺序性指的是在如果连接顺序地发送多个请求，计算得到的多个响应是否按相同顺序发送响应。

![图片.png](https://upload-images.jianshu.io/upload_images/1936544-0229bf5896a7001b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


 |
