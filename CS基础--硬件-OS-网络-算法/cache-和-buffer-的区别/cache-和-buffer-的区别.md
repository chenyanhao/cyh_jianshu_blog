这二者是有区别的。


中文说不清楚，英文解释得很清楚，
```
A buffer is something that has yet to be “written” to disk.
A cache is something that has been “read” from the disk and stored for later use.
```

cache 是为了弥补高速设备和低速设备的鸿沟而引入的中间层，最终起到 **加快访问速度** 的作用。
buffer 的主要目的进行流量的 reduce，把突发的「大数量小规模的I/O」整理成平稳的「小数量较大规模的 I/O」。



