C 和 FP 并不是对立的！C 语言也可以实现一些比如类型推断，泛型，函数闭包，匿名函数等 FP 中的东西。其实太阳底下其实无新鲜事，这次尝试用 C 来玩 FP 吧！

> GCC 为 C 添加了函数闭包的功能（在函数内定义函数），Clang 加入了 Block Type（可以实现类似匿名函数的功能）。

# 高阶函数

一些基础的高阶函数例如 map、folderRight、folderLeft 等，用 C 语言也可以实现。

## folder 函数

```c
// f (arr[1],f(arr[2],f(arr[3],...f(arr[n],x0))))
// 例如 : 1+(2+(3+(4+x0)))
// f          => map 函数
// x0         => 初始值
// arr/length => 数组
int foldRight(int (*f)(int, int), int x0, int* const arr, int length) {
  int total  =x0;
  for (int i = length - 1; i >= 0; i--) {
    total = f(arr[i], total);
  }
  return total;
}

// foldLeft 同理
int foldLeft(int (*f)(int, int) ,int x0, int* const arr, int length) {
  int total = x0;
  for (int i = 0; i < length; i++) {
    total = f(total, arr[i]);
  }
  return total;
}
```

## map 函数

```c
// f => map 函数
void map(int (*f)(int), int* const arr ,int* const brr ,int length){
  for (int i = 1; i <= length; i++) brr[i] = f(arr[i]);
  return;
}
```

类似以上的写函数的方法，还可以写出另外一些高阶函数比如filter，zip等。

# curring & closure

虽然柯里化现在有些专家对这个特性提出争议，但是还是要玩一下，毕竟柯里化几乎 FP 的标配。

```c
//add2(x)(y)=add(x,y)
int (*add2(int x))(int){
  int add1(int y){
    return add(x,y);
  }
  return add1;
}

//add3(x)(y)(z)=x+y+z
int (*(*add3(int x))(int))(int){
  int (*add2(int y))(int){
    int x1 = x;
    int add1(int z){
      return (x1 + y + z);
    }
    return add1;
  }
  return add2;
}
```

> 在函数内部定义函数这在标准C里面是做不到的，GCC里面实现函数的调用用的是弹床（trampoline）的方法，这个函数调用的方法是专为全局函数所设计的。猜测是通过某种手段，将局部函数提升为全局函数。

根据以上思路，可以写一个函数将传入的函数柯里化
```c
//currying(f)(x)(y)=f(x,y)
int (*(*currying(int (*f)(int, int)))(int))(int){
  int (*fx(int x))(int){
    int (*f1)(int, int);
    f1 = f;
    int fxy(int y){
      return (f1(x, y));
    }
    return fxy;
  }
  return fx;
}
```

# 更大胆的尝试

## 生硬的 Lambda

```c
int main(int argc, const char **argv){
   int max, a, b;
   max = (scanf("%d %d", &a, &b), a > b ? a : b);
   printf("%d\n", max);
   return 0;
}
```

语句表达式可以结合宏使用，会写出意想不到的功能。

## typeof()
感觉这里可能是 C 扩展借鉴了 C++11 里面的 decltype吧
```c
int main(int argc, const char **argv){
  typeof(int (*)(int)) add(int x){
    int add(int y){return x + y;}
    return add;
  }  
  printf("%d\n", add(2)(3));
  return 0;
}
```

typeof()括号里还能放值，例如 `typeof('a') c` 相当于 `char c`

typeof、语句表达式和宏结合，还可以弄出类型推导。

## Lambda

```c
int main(int argc, const char **argv){
  int x = ({int trible(int x){return 3 * x;} trible;})(3);
  printf("%d\n", x);
  return 0;
}
```

对这一段代码进行抽象，

```c
({int trible(int x){return 3 * x;} trible;})
```

总结一下就是，

```c
({ 
   type name func_body
   name;
})
```

用宏实现，

```c
#define Lambda(type,body) ({\
  type lambda_funcname body\
  lambda_funcname; \
})
```

用上 typeof ，
```c
#define Lambda(return_type,func_body) ({\
  typeof(return_type) lambda_funcname func_body\
  lambda_funcname; \
})
```

于是乎，重写 currying 函数，
```c
int (*(*currying(int (*f)(int, int)))(int))(int){
  return Lambda(int (*)(int),(int x){
    int (*f1)(int, int);
    f1 = f;
    return Lambda(int, (int y){
      return f1(x, y);
    });
  });
}
```

__不过……代码的可读性并没有提高，反而更难读了__
# 总结

这种风格的 C 语言程序还是少写为妙，因为：
1. 在 C 语言里面传入函数，传出函数势必使用很多的函数指针，造成了代码维护的困难；
2. C 语言是一个静态弱类型的语言，在类型系统上做得十分糟糕，容许类型的隐式转化，也无法实现泛型与类型推导，这大大限制了这种风格代码的应用广度，比如说前面的 map 函数，不一定映射的是整数，也可以是字符串，但是因为只能声明几种，大大限制了 map 的适用范围；
3. C 扩展对某些功能并不是原生支持的，可能藏着不少 bug。

