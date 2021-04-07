# 一个简单的 for

一个非常简单的 for 表达式，看起来像这样，
```scala
val ns = List(1, 2)  
val qs = for (n <- ns) yield n * 2  
assert (qs == List(2, 4)) 
```
它看起来像一个循环，但它不是。这是 map 的伪装，
```scala
val qs = ns map {n => n * 2}  
```

规则很简单，
```scala
for (x <- expr) yield resultExpr  

//展开为
expr map {x => resultExpr}  

//它等同于
expr flatMap {x => unit(resultExpr)}  
```

# 多一点的 For

前面的例子中，for 的括号中只有一条表达式，现在增加一条，
```scala
val ns = List(1, 2)  
val os = List (4, 5)  
val qs = for (n <- ns; o <- os) yield n * o  
assert (qs == List (1*4, 1*5, 2*4, 2*5))  
```
这个形式的 for 看起来想一个嵌套循环，但它不过也是 map 和 flatMap，
```scala
val qs = ns flatMap {n => os map {o => n * o }}  
```

这里需要注意一下，两层 map 它是怎么计算的呢，
```scala
// 第一步
val qs = ns flatMap {n => 
            os map { o => n * o } // 1
          }

// 第二步
val qs = ns flatMap {n =>        // 2
            List(n * 4, n * 5)          // 上面的1
         }

// 第三步
val qs = List(1 * 4, 1 * 5, 2 * 4, 2 * 5) // 上面的2
```

这说明，命令式语言的多层循环之类，可以通过 map/flatMap 来替代。

# 更多的表达式

```scala
val qs = for (n <- ns; o <- os; p <- ps) yield n * o * p  

// 展开为
val qs = ns flatMap {n => 
            os flatMap {o =>   
                {ps map {p => n * o * p}}}}  
```

可以看到，转换是递归的，重复的 flatMap，直到只剩下一条表达式，将最后一条转换为map。

写成更详细的代码就是这样，
```scala
// 第一步
val qs = for (n <- ns;  // 第一个表达式
                o <- os;    // 第二个
                p <- ps)    // 第三个
            yield n * o * p

// 第二步
val qs = ns flatMap {n => // 第一个表达式，用 flatMap 翻译
                for(o <- os; 
                p <- ps) 
                yield n * o * p}

// 第三步
val qs = ns flatMap { n => 
                os flatMap {o => // 第二个也用 flatMap 翻译
                for(p <- ps) 
                yield n * o * p}}

// 第四步
val qs = ns flatMap {n => os flatMap {o =>
                {ps map {p => n * o * p}}} // 第三个(最后一个)用 map 翻译
````

# 命令式的 for
for 也有一个命令式的版本，用于那些只调用一个函数，并不在意副作用的情况。这种版本只用去掉 yield 声明，例如，
```scala
val ns = List(1, 2)  
val os = List (4, 5)  
for (n <- ns; o <- os)  println(n * o) 
```

这个展开规则和 yield 版本很像，但用 foreach 替代了 flatMap 或 map，展开为，
```scala
ns foreach {n => os foreach {o => println(n * o) }}  
```

如果不想使用命令式的 for，就不需要实现 foreach。不过既然已经实现了 map，foreach 的实现是很简单的，
```scala
class M[A] {  
    def map[B](f: A=> B) : M[B] = ......  
    def flatMap[B](f: A => M[B]) : M[B] = ......  
    def foreach[B](f: A=> B) : Unit = {  
        map(f)  
        ()  
    }  
}  
```
换句话说，foreach 可以通过调用 map 并丢掉结果来实现。
> 不过这么做运行时效率可能不好，所以 scala 允许用自己的方式自定义 foreach。

# 带过滤的 for

Scala 的 for 声明还有一个特征：if 守护(guard)，
```scala
val names = List("Abe", "Beth", "Bob", "Mary")  
val bNames = for (bName <- names;  // 注意这里分号不能少
                if bName(0) == 'B'  
            ) yield bName + " is a name starting with B"  

assert(bNames == List(
    "Beth is a name starting with B",   
    "Bob is a name starting with B"))  
```
if 守护会映射为 filter 方法，上面的 for 语句会翻译成下面这样，
```scala
val bNames = (names filter { bName => bName(0) == 'B' }) 
             .map { bName =>   
                bName + " is a name starting with B"   
             }  
```



| Haskell | Scala |
| :-: | :-: |
| `do var1<- expn1 var2 <- expn2 expn3 ` | `for {var1 <- expn1; var2 <- expn2; result <- expn3 } yield result` |
| `do var1 <- expn1 var2 <- expn2 return expn3`  | `for {var1 <- expn1; var2 <- expn2; } yield expn3` |
| `do var1 <- expn1 >> expn2 return expn3 ` | `for {_ <- expn1; var1 <- expn2 } yield expn3` |






