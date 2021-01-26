# 报错如下
```c++
error: 'mutex' in namespace 'std' does not name a type
error: 'thread' in namespace 'std' does not name a type
error: 'condition_variable' in namespace 'std' does not name a type
```

# 原因分析
MinGW-w64 (or rather GCC on windows) needs to be compiled with posix thread support if you want to use std::thread, presumably you downloaded a build with native windows threads.

Check out the mingw-builds folders targeting 64 bit or 32 bit and pick a version with posix threads. You'll also need to choose the exception handling method, if you don't have a reason to choose otherwise then stick with the GCC defaults of seh for 64 bit and dwarf for 32.

> 大致意思就是说，在 win 下，mingw64 需要用 posix 接口的 thread 库。而我这里的报错时用的库是 Windows native thread 库，而不是 posix 的。

# 解决办法
就像上面英文所说，下载 mingw-builds with posix threads。
下载地址如下，
https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/

进去发现，有很多版本，例如 SEH / SJLJ，那么下哪个版本呢？这些版本之间有何区别？
这就引出来另一个问题。

# What is the difference between MinGW SEH and MinGW SJLJ?

SJLJ and SEH are two different exception handling systems.

For the specific differences, the resources you've already seen cover everything.

However, as for which one is better to install, go with SJLJ unless you know that you need SEH.
> 所以我这里下载的是 SJLJ 版本。

### SJLJ
SJLJ is more widely supported across architectures, and is more robust. Also, SJLJ exceptions can be thrown through libraries that use other exception handling systems, including C libraries. However, it has a performance penalty.

### SEH
SEH is much more efficient (no performance penalty), but unfortunately is not well-supported. SEH exceptions will cause bad things to happen when thrown through libraries that do not also use SEH.

As far as your code is concerned, there are no real differences. You can always switch compilers later if you need to.



