# 一、`(?y)` 这种匿名函数
```haskell
greaterThan100 :: [Integer] -> [Integer]
greaterThan100 xs = filter (>100) xs
```
(>100) is an **operator section**: if `?` is an operator, then `(?y)` is equivalent to the function `\x -> x ? y`, and `(y?)` is equivalent to `\x -> y ? x`. In other words, using an operator section allows us to partially apply an operator to one of its two arguments. What we get is **a function of a single argument**.

# 二、Function composition
都知道，点操作符(.)是用来 compose 两个函数的，但是为什么要引入它吗？仅仅是为了书写方便的语法糖？
```haskell
foo :: (b -> c) -> (a -> b) -> (a -> c)
foo f g = \x -> f (g x)
```
 Does foo actually do anything useful or was that just a silly exercise in working with types?
As it turns out, foo is really called `(.)`, and represents function composition. That is, if f and g are functions, then `f . g` is the function which does **first g and then f**.

由此可见，并不仅仅是语法糖。

```haskell
myTest :: [Integer] -> Bool
myTest xs = even (length (greaterThan100 xs))

myTest' :: [Integer] -> Bool
myTest' = even . length . greaterThan100
```
This example also demonstrates why function composition seems “backwards”: it’s because function application is backwards! Since we read from left to right, it would make sense to think of values as also flowing from left to right. **But** in that case we should write `(x)f` to denote giving the value x as an input to the function f. But no thanks to `Alexis Claude Clairaut` and `Euler`, we have been stuck with the backwards notation since 1734.

> 这里解释了读起来不是从左向右而是 “backwards”。因为一般习惯了函数写成 `f(x)` ，而不是写成 `(x)f`。函数式编程语言跟数学关系密切，所以这里可以理解成是为了照顾到数学的习惯。

# 三、“point-free” style
This style of coding in which we define a function **without reference to its arguments** — in some sense saying what a function `is` rather than what it `does` — is known as **“point-free”** style. 


# 四、用中缀表达式理解 fold
```haskell
fold :: b -> (a -> b -> b) -> [a] -> b
fold z f []     = z
fold z f (x:xs) = f x (fold z f xs)

fold f z [a,b,c] == a `f` (b `f` (c `f` z)) // 用中缀表达式理解
```

# 五、Haskell type class和 Java interface 的对比

Type classes in Haskell are used to present an interface for types that have some behavior in common. 
Java interface 就不解释了。

相同点：Both define a set of types/classes which implement a specified list of operations.

不同点：
1）定义 Java 类时，必须声明它实现的任何接口。 类型类实例与相应类型的声明可以分开，甚至可以放在单独的模块中。

2）Java 只能动态单派发，而 Haskell 可以轻松实现动态多派发，例如，
```haskell
class Blerg a b where
  blerg :: a -> b -> Bool
```
编译器应该选择哪种 Blerg 实现同时取决于类型 a 和 b，这是多派发。Java 编译器只支持动态单派发。

3）对于子类的二元相关操作，Java 较为笨拙，而 Haskell 可以很优雅，例如，
```haskell
class Num a where
  (+) :: a -> a -> a
  ...
```
类似这种操作在Java中没有很好的方法，原因是，
1. 二元操作的两个参数中的一个必须是 “privileged”，即实际上是在它上面调用（+）方法（假设 Java 支持运算符重载），这种不对称性很丑；
2. 由于Java的子类型获取某个接口类型的两个参数并不能保证它们实际上是相同的类型，这使得实现二元运算符如（+）通常需要一些运行时类型检查。

# 六、side-effect、惰性求值、严格求值
严格求值的定义：Under a strict evaluation strategy, function arguments are completely evaluated before passing them to the function.
严格求值的好处：The benefit of strict evaluation is that it is easy to predict when and in what order things will happen. Usually languages with strict evaluation will even specify the order in which function arguments should be evaluated (e.g. from left to right).

side-effect 的定义：By “side effect” we mean **anything that causes evaluation of an expression to interact with something outside itself**.
> 彩蛋：The challenge facing the Haskell designers was to come up with a way to allow such effects in a principled, restricted way that did not interfere with the essential purity of the language. They finally did come up with something (namely, the IO monad).

惰性求值的定义：Under a lazy evaluation strategy, evaluation of function arguments is delayed as long as possible: they are not evaluated until it actually becomes necessary to do so.  
> When some expression is given as an argument to a function, it is simply packaged up as an unevaluated expression (called a “thunk”, don’t ask me why) without doing any actual work.

惰性求值的时机：The slogan to remember is **“pattern matching drives evaluation”**. To reiterate the important points:
- Expressions are only evaluated when pattern-matched
- …only **as far as necessary** for the match to proceed, and no farther!
> 1. “模式匹配驱动求值”
> 2. Important thing to note is that thunks are evaluated **only enough** to allow a pattern match to proceed, and no further! (求值时求到够用即可)

# 七、关于 fold 一段很精彩的话
The fold for T will take one (higher-order) argument for each of T’s constructors, encoding how to turn the values stored by that constructor into a value of the result type — assuming that any recursive occurrences of T have already been folded into a result. Many functions we might want to write on T will end up being expressible as simple folds.

# 八、关于 Haskell 的 IO，一段精彩的话
Values of type `IO a` are ***descriptions of*** effectful computations, which, if executed would (possibly) perform some effectful I/O operations and (eventually) produce a value of type `a`. **A value of type `IO a`, in and of itself, is just an inert, perfectly safe thing with no effects**. It is just a ***description of*** an effectful computation.

In the same way, a value of type `IO a` is just a “recipe” for producing a value of type `a` (and possibly having some effects along the way). Like any other value, it can be passed as an argument, returned as the output of a function, stored in a data structure, or (as we will see shortly) combined with other IO values into more complex recipes.

So, how do values of type `IO a` actually ever get executed? There is only one way: the **Haskell compiler** looks for a special value.

Think of the **Haskell runtime system** as a master chef who is **the only one** allowed to do any cooking. If you want your recipe to be followed then you had better make it part of the big recipe (main) that gets handed to the master chef. Of course, main can be arbitrarily complicated, and will usually be composed of many smaller IO computations.

# 九、IO String 和 String 的区别（也适用于 IO a 和 a）
A value of type `IO String` is **a description of** some computation, a recipe, for generating a `String`. There is no `String` “inside” an `IO String`, any more than there is a `cake` “inside” a `cake recipe`. To produce a String (or a delicious cake) requires actually executing the computation (or recipe). And **the only way** to do that is to give it (perhaps as part of some larger IO value) to the Haskell runtime system, via main.
> 注意第一句话：A value of type `IO String` is a description of some computation, a recipe, for generating a `String`. （只是一个描述而已。）


# 十、IO 的简单组合
The simplest way to combine two IO computations is with the `(>>)` operator (pronounced “and then”), which has the type 
```haskell
(>>) :: IO a -> IO b -> IO b
```
This simply creates an IO computation which consists of running the two input computations in sequence. Notice that the result of the first computation is **discarded**; we only care about it for its effects. For example: 
```haskell
main = putStrLn "Hello" >> putStrLn "world!"
```

What if we don’t want to throw away the result from the first computation?
there is an operator `(>>=)` (pronounced “bind”) with the type
```haskell
(>>=) :: IO a -> (a -> IO b) -> IO b
```


# 十一、type 和 Kind，以及深入理解 Kind

Types are little labels that values carry so that we can reason about the values. But types have their own little labels, called kinds. A kind is more or less the type of a type. 
> 类型是值的标签，而 Kind 是类型的标签。
> 弄清楚三个东西：值、类型、Kind

搞懂 kind，能加深对 Haskell 类型系统的理解。
在 ghci 中，通过 `:k` 查看 kind，
```haskell
ghci> :k Int
Int :: *
```
A * means that the type is a **concrete type**. A concrete type is a type that doesn't take any type parameters and values can only have types that are concrete types.
> 一个 * 代表这个类型是 `concrete type`。一个 `concrete type` 是没有任何类型参数，且值只能属于 `concrete type`。

再看看 Maybe 的 kind，
```haskell
ghci> :k Maybe  
Maybe :: * -> * 
```
> `Maybe` is, in a sense, **a function on types** — we usually call it a type constructor. 

The `Maybe` **type constructor** takes one concrete type (like `Int`) and then returns a concrete type like `Maybe Int`. And that's what this kind tells us. Just like `Int -> Int` means that a **function** takes an `Int` and returns an `Int`, `* -> *` means that the **type constructor** takes one concrete type and returns a concrete type. 
> `Maybe` 的类型构造子接受一个具体类型(如 `Int`)然后回传一个具体类型(如 `Maybe Int`)。这就是 kind 告诉我们的信息。就像 `Int -> Int` 代表这个函数接受一个 `Int` 并返回一个 `Int` 。 `* -> *` 代表这个类型构造子接受一个具体类型并返回一个具体类型。



再看看 Either，
```haskell
ghci> :k Either 
Either :: * -> * -> *
```
这说明 Either 接受两个具体类型作为参数，并构造出一个具体类型。它看起来也像是一个接受两个参数并返回值的函数类型。类型构造子是可以 curry 化的，所以也能 partially apply，

```haskell
ghci> :k Either String  
Either String :: * -> *  
ghci> :k Either String Int  
Either String Int :: *  
```

再来看看 Functor 的定义，

```haskell
class Functor f where   
    fmap :: (a -> b) -> f a -> f b  
```
可以看到 `f` 类型变量是接受一个 concrete type 且构造出一个 concrete type 的类型。 知道它构造出 concrete type 是因为是作为函数参数的类型。 从那里可以推测出一个类型要是属于 `Functor` 必须是 `* -> *` Kind。

接下来看看下面这个新定义的 typeclass，看看 Kind 的威力，

```haskell
class Xxxxx t where  
    yyyyy :: j a -> t a j
```

可以来看看他的 kind 是什么？
1. 由于 `j a` 被当作 `yyyyy` 这个函数的入参，所以 `j a` 的 Kind 一定是 `*`；
2. 假设 `a` 的 Kind 是 `*`，那么 `j` 的 Kind 就会是 `* -> *`；
3. 由于 `t a j` 是函数的返回值，而知道 `a` 和 `j` 的 Kind 分别是 `*` 和 `* -> *`，因此可以推测出 `t` 的 Kind 是 `* -> (* -> *) -> *`；
4. 也就是说 `t` 接受一个具体类型 `a`、一个接受单一参数的类型构造子 `j`，然后产生出一个具体类型；
5. `Xxxxx` is a **higher-order type constructor**, in the same way that `map` is a **higher-order function**. （注意对比理解）


看最后一个例子，定义一个类型具有 `* -> (* -> *) -> *` 的 kind，下面是一种定义的方法，

```haskell
data Frank a b  = Frank {frankField :: b a} deriving (Show)  
```

怎么推断出这个类型具有 `* -> (* -> *) -> *` 的 kind 呢？
1. ADT 中的字段是要来塞值的，所以其 Kind 必须是 `*`；
2. 假设 `a` 是 `*`，那 `b` 就是接受一个类型参数的 Kind，即 `* -> *`；
3. 现在知道 a 和 b  的 Kind 了，而它们又是 Frank 的类型参数，所以可以推断出 Frank 的 Kind 是 `* -> (* -> *) -> *`，其中第一个 `*` 代表 a，第二个 `(* -> *)` 代表  b。

# 十二、 为什么要引入 Functor
这里尝试换个角度说明为什么要引入 Functor。

### 从消除重复代码的角度
首先明确一点，软件设计的很多概念和思想其实都是为了一件事情 ------ 消除重复代码，例如继承。

因此从这个角度来看，Functor 也是一种消除重复代码的方式。先看看一堆的 Map 函数，
```haskell
map :: (a -> b) -> [a] -> [b]

treeMap :: (a -> b) -> Tree a -> Tree b

maybeMap :: (a -> b) -> Maybe a -> Maybe b
```

仔细对比发现，这是 repeated pattern，因此需要消除，将类型抽象出来，就可以消除重复代码了，
```haskell
thingMap :: (a -> b) -> f a -> f b
```
> `thingMap` has to work differently for each particular f. 

可以看到，这和 fmap 的签名是一样的。

### 从设计模式的角度
对于 OO 类的静态语言如 C++、Java等，设计模式用得非常多。
设计模式用一句简单的话来总结就是 ------ 用固定的“套路”解决问题。这些“套路”就是那些设计模式了。

在 FP 类的语言中，也有不少“套路”，例如 Functor/Applicative/Monad 等。

### 彩蛋
来玩一个好玩的事情。
回顾一下，Functor 定义如下，
```haskell
class Functor f where
  fmap :: (a -> b) -> f a -> f b
```
如果对 `(->) e` 实现 Functor 会怎样？将其代入 Functor 的定义中，得到，

```haskell
instance Functor ((->) e) where
  fmap :: (a -> b) -> (->) e a -> (->) e b
```

然后将 `(->)` 写成中缀写法，
```haskell
instance Functor ((->) e) where
  fmap :: (a -> b) -> (e -> a) -> (e -> b)
```

仔细看，上面这个函数签名是不是很熟悉？是的，
```haskell
instance Functor ((->) e) where
  fmap = (.)
```

Crazy! 
Funny!

# 十三、Applicator 的一些杂记
Like `pure (+) <*> Just 3 <*> Just 5`（操作结果为 `Just 8`）, applicative functors and the applicative style of doing pure `f <*> x <*> y <*> ...` allow us to take a function that expects parameters that aren't necessarily wrapped in functors（`pure` 函数可以将该 function 包装到 functors 中） and use that function to **operate on several values that are in functor contexts**（通过 `<*>` 函数）. The function can take as many parameters as we want, because it's always partially applied step by step between occurences of `<*>`.


# 十四、有了 Applicator 为何还需要 Monad

Applicative gives us no way to decide what to do next based on previous results: we must decide in advance operations we are going to run, before we see the results.


# 十五、Type variables are independent of parameter names or other value names
例子，
```haskell
(<$>) :: (Functor f) => (a -> b) -> f a -> f b  
f <$> x = fmap f x 
```
The ***`f` in the function declaration*** here is a type variable with a class constraint saying that any type constructor that replaces `f` should be in the Functor typeclass. The ***`f` in the function body*** denotes a function that we map over `x`. The fact that we used `f` to represent both of those **doesn't mean that they somehow represent the same thing**.


# 十六、sequence 函数来历及其用法举例

### 怎么来
We can combine any amount of applicatives into one applicative that has a list of the results of those applicatives inside it, 
```haskell
sequenceA :: (Applicative f) => [f a] -> f [a]  
sequenceA [] = pure []  
sequenceA (x:xs) = (:) <$> x <*> sequenceA xs 
```
> 例如，combine `Just [3,4]` with `Just 2` to produce `Just [2,3,4]`

Another way to implement sequenceA is with a fold. Remember, pretty much any function where we go over a list element by element and accumulate a result along the way can be implemented with a fold, 
```haskell
sequenceA :: (Applicative f) => [f a] -> f [a]  
sequenceA = foldr (liftA2 (:)) (pure [])  
```
其中，`liftA2` 定义如下，
```haskell
liftA2 :: (Applicative f) => (a -> b -> c) -> f a -> f b -> f c  
liftA2 f a b = f <$> a <*> b  
```

换个角度理解 `sequenceA` ------ Doing `(+) <$> (+3) <*> (*2)` will create a function that takes a parameter, feeds it to both `(+3)` and `(*2)` and then calls `+` with those two results. In the same vein, it makes sense that `sequenceA [(+3),(*2)]` makes a function that takes a parameter and feeds it to all of the functions in the list. Instead of calling `+` with the results of the functions, a combination of `:` and `pure []` is used to gather those results in a list, which is the result of that function.


### 怎么用
##### 示例一
Using sequenceA is cool when we have a list of functions and we want to feed the same input to all of them and then view the list of results. For instance, 
```haskell
ghci> map (\f -> f 7) [(>4),(<10),odd]  
[True,True,True]  
ghci> and $ map (\f -> f 7) [(>4),(<10),odd]  
True  
```
Another way to achieve the same thing would be with sequenceA,
```haskell
ghci> sequenceA [(>4),(<10),odd] 7  
[True,True,True]  
ghci> and $ sequenceA [(>4),(<10),odd] 7  
True  
```
>  注意：lists are homogenous, all the functions in the list have to be functions of the same type, of course. You **can't** have a list like `[ord, (+3)]`, because `ord` takes a character and returns a number, whereas `(+3)` takes a number and returns a number.

##### 示例二
`sequenceA` 还可以用来做列表生成式（list comprehension），
```haskell
ghci> sequenceA [[1,2,3],[4,5,6]]  
[[1,4],[1,5],[1,6],[2,4],[2,5],[2,6],[3,4],[3,5],[3,6]]  
ghci> [[x,y] | x <- [1,2,3], y <- [4,5,6]]  
[[1,4],[1,5],[1,6],[2,4],[2,5],[2,6],[3,4],[3,5],[3,6]]  

ghci> sequenceA [[1,2],[3,4]]  
[[1,3],[1,4],[2,3],[2,4]]  
ghci> [[x,y] | x <- [1,2], y <- [3,4]]  
[[1,3],[1,4],[2,3],[2,4]]  
```
Here is how `sequenceA` works,
1. We start off with `sequenceA [[1,2],[3,4]]`
2. That evaluates to `(:) <$> [1,2] <*> sequenceA [[3,4]]`
3. Evaluating the inner `sequenceA` further, we get `(:) <$> [1,2] <*> ((:) <$> [3,4] <*> sequenceA [])`
4. We've reached the edge condition, so this is now `(:) <$> [1,2] <*> ((:) <$> [3,4] <*> [[]])`
5. Now, we evaluate the `(:) <$> [3,4] <*> [[]]` part, which will use `:` with every possible value in the left list (possible values are `3` and `4`) with every possible value on the right list (only possible value is `[]`), which results in `[3:[], 4:[]]`, which is `[[3],[4]]`. So now we have `(:) <$> [1,2] <*> [[3],[4]]`
6. Now, `:` is used with every possible value from the left list (`1` and `2`) with every possible value in the right list (`[3]` and `[4]`), which results in `[1:[3], 1:[4], 2:[3], 2:[4]]`, which is `[[1,3],[1,4],[2,3],[2,4]`

##### 示例三

When used with I/O actions, `sequenceA` is the same thing as `sequence`! It takes a list of I/O actions and returns an I/O action that will perform each of those actions and have as its result a list of the results of those I/O actions. 
That's because to turn an `[IO a]` value into an `IO [a]` value, to make an I/O action that yields a list of results when performed, all those I/O actions have to be sequenced so that they're then performed one after the other when evaluation is forced. Remenber that You ***can't get the result of an I/O action without performing it***.












