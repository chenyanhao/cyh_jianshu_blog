可以这样去理解，更加直观：
1. 在函数开始处，加入 `result = list()`
2. 将每个 `yield` 表达式 `yield expr` 替换为 `result.append(expr)`
3. 在函数末尾处，加入 `return result`。


举例，下面这段代码，
```python
def createGenerator() :
    mylist = range(3)
    for i in mylist :
        yield i*i

mygenerator = createGenerator() # create a generator
for i in mygenerator:
    print(i)
```

从执行结果上来看，按照上面的理解，yield 函数可以改写成下面这样，
```python
def createGenerator() :
    result = list() # 函数开始处
    mylist = range(3)
    for i in mylist :
        result.append(i*i) # yield 表达式替换
    return result # 函数结尾处
```
