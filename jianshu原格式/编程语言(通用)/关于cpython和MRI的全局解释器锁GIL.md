As known to all，python 的最流行的解释器 cpython 和 ruby 的最流行的解释器 mri 都用了 GIL。外面讨论 GIL 性能的挺多，看到一些有深度的点评，挺有意思。

下面这个就是：

GIL 是个伪命题 —— 初级程序员很容易被 80 年代的中文翻译过来的垃圾过时教程说，解决 concurrency 只能用多线程。然后就拿着多线程这个锤子到处找钉子。

其实这里要区分一个 IO 密集和 CPU 密集的。IO 密集，即便有 GIL 也可以通过coroutine 或者 Fiber 很好解决，性能不低。

CPU 密集——这个得好好想一下。

如果只有一个核心，10 件事每个事要做 1 分钟，对于 CPU 密集任务，怎么用多线程都还是至少需要 10 分钟才能得到结果吧？多线程有毛用？
如果有多个核心，这就是 Python/Ruby 的问题了。只能用一个核心来处理任务。因为有 GIL。
所以 GIL 不是不能用多线程问题，而是多线程只能用单个核心的问题。但是实际上，大家也不是没见过 Chrome 啊，3D 游戏里只把一个核心占满的情况。这不就是只能利用一个核心的毛病么？为啥 GIL 就臭名昭著，而 C/C++ 大家就会很自然想到一个借口说你代码写得不好呢？

但是反过来说，你要用脚本语言解决计算密集问题？你 TM 逗我？计算性能问题，首先就得说 MRI/CPython 这个和 C 语言 30 倍性能差距的问题。。。。。。。。。。

就算没 GIL 的 Java 里，写多线程也不是个什么好体验。JVM 是不会卡进程，各种锁得你自己搞。搞得不好还是会卡进程。就算 C/C++ 直接用 pthreads，写起来是各种坑。

在实际应用中，GIL 给大家带来的不便是 0 。绝大多数市面上能看到的多线程教程，无论什么语言，都是用来解决 io wait 的问题的。 io wait 在 Ruby/Python 已经有 n 种解决方案了。

你如果写代码真碰到 GIL 问题了，请一定怀疑你的姿势不对。

最后还是要喷一下：为什么 nodejs 没有 GIL 问题？因为别人压根不支持多线程。(还不是活得好好的。)
