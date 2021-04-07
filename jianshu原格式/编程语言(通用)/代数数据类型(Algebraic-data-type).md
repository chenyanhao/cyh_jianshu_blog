看多文章都在说这个，但是感觉没有一个人说清楚了。

看到了 Haskell 的 wiki，还是其 wiki 靠谱，讲解深入浅出很清晰，粘一些重要的东西，如下，


This is a type where we specify the shape of each of the elements. Wikipedia has a thorough discussion. "Algebraic" refers to the property that an Algebraic Data Type is created by "algebraic" operations. **The "algebra" here is "sums" and "products"**:

"sum" is alternation (A | B, meaning A or B but not both)
"product" is combination (A B, meaning A and B together)

Examples:
- `data Pair = P Int Double` is a pair of numbers, an Int and a Double together. The tag P is used (in constructors and pattern matching) to combine the contained values into a single structure that can be assigned to a variable.
- `data Pair = I Int | D Double` is just one number, either an Int or else a Double. In this case, the tags I and D are used (in constructors and pattern matching) to distinguish between the two alternatives.

> 注意上面标黑的地方。


Haskell wiki 地址：https://wiki.haskell.org/Algebraic_data_type

