前前后后用过好多种，感觉还是下面这种最简单，可读性比 lambda 还要高，

```java
oldList.removeAll(Collections.singleton(null));
```

将上面代码中的 null 也可以替换成其他东西，
```java
String init[] = { "One", "Two", "Three", "One", "Two", "Three" };

List list1 = new ArrayList(Arrays.asList(init));
List list2 = new ArrayList(Arrays.asList(init));
      
list1.remove("One"); // [Two, Three, One, Two, Three]
list2.removeAll(Collections.singleton("One")); // [Two, Three, Two, Three]
```


