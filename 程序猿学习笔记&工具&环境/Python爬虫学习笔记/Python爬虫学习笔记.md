# 结构安排

**一**至**十八**是第一部分；

**十九**至**二十六**是第二部分。

# 一、大数据时代的挑战

数据抽取、转换、存储 (Data ETL)

* 原始资料：Raw Data
* ETL脚本：ETL Scipt
* 结构化数据：Tidy Data

# 二、非结构化数据处理与网络爬虫

1. 网页链接器(Web Connector)向目标网页发出请求(request)；
2. 目标网页将响应(response)发送给网页链接器(Web Connector)；
3. 对收到的响应进行资料剖析(Data Parser)，剖析成结构化数据；
4. 将结构化数据存入数据中心(Data Center)

# 三、了解网络爬虫背后的秘密

* 浏览器内建的开发人员工具
* requests
* BeautifulSoup4 (注意，BeautifulSoup4和BeautifulSoup是不一样的)
* jupyter

	> jupyter中编辑的文件会保存在用户的家目录下，例如在windows中就会是```C:\Users\username```


以Chrome为例，抓取前的分析步骤如图：

![抓取前的分析.png](http://upload-images.jianshu.io/upload_images/1936544-6f73eadb0aead9b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


1. 按```F12```进入到开发者工具；
2. 点击```Network```；
3. ```刷新页面```；
4. 找到```Doc```；
5. 找到左边```Name```这一栏的第一个(需要爬去的链接90%的情况都是第一个)；
6. 点击右边的```Headers```；
7. 找到请求的URL和请求方式。



# 四、撰写第一只网络爬虫

## Requests库

* 网络资源撷取套件
* 改善Urllib2的缺点，让使用者以最简单的方式获取网络资源
* 可以使用REST操作存取网络资源

## jupyter

使用jupyter来抓取网页并打印在浏览器中，再按```Ctrl-F```查找对应的内容，以确定我们要爬去的内容在该网页中。

## HelloWorld

```python
import requests
res = requests.get('http://www.sina.com.cn/')
res.encoding = 'utf-8'
print(res.text)
```

# 五、用BeautifulSoup4剖析网页元素

```python
from bs4 import BeautifulSoup
html_sample = ' \
<html> \
<body> \
<h1 id="title">Hello World</h1> \
<a href="#" class="link">This is link1</a> \
<a href="# link2" class="link">This is link2</a> \
</body> \
</html>'

soup = BeautifulSoup(html_sample, 'html.parser')
print(soup.text)
```


# 六、BeautifulSoup基础操作

**使用select找出含有h1标签的元素**

```python
soup = BeautifulSoup(html_sample)
header = soup.select('h1')
print(header)
print(header[0])
print(header[0].text)
```

**使用select找出含有a的标签**

```python
soup = BeautifulSoup(html_sample, 'html.parser')
alink = soup.select('a')
print(alink)
for link in alink:
    print(link)
    print(link.txt)
```

**使用select找出所有id为title的元素(id前面需要加#)**

```python
alink = soup.select('#title')
print(alink)
```

**使用select找出所有class为link的元素(class前面需要加.)**
```python
soup = BeautifulSoup(html_sample)
for link in soup.select('.link'):
	print(link)
```

**使用select找出所有a tag的href链接**

```python
alinks = soup.select('a')
for link in alinks:
	print(link['href']) # 原理：会把标签的属性包装成字典
```

```python
a = '<a href="#" qoo=123 abc=456> i am a link</a>'
soup2 = BeautifulSoup(a, 'html.parser')
print(soup2.select('a'))
print(soup2.select('a')[0])
print(soup2.select('a')[0]['qoo'])
```


# 七、观察如何抓取新浪新闻信息

关键在于寻找CSS定位

* Chrome开发人员工具(进入开发人员工具后，左上角点选元素观测，就可以看到了)  

![Chrome寻找元素定位.png](http://upload-images.jianshu.io/upload_images/1936544-973c33a2f878679a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


* Firefox开发人员工具
* InfoLite(需翻墙)


# 八、制作新浪新闻网络爬虫

抓取时间、标题、内容

```python
import requests
from bs4 import BeautifulSoup

res = requests.get('http://news.sina.com.cn/china')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

for news in soup.select('.news-item'):
    if (len(news.select('h2')) > 0):
        h2 = news.select('h2')[0].text
        time = news.select('.time')[0].text
        a = news.select('a')[0]['href']
        print(time, h2, a)

```

# 九、抓取新闻内文页面

新闻网址为：```http://news.sina.com.cn/c/nd/2016-08-20/doc-ifxvctcc8121090.shtml```

![内文资料信息说明.png](http://upload-images.jianshu.io/upload_images/1936544-a2a2e68128754123.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**取得内文页面**的步骤和```三、了解网络爬虫背后的秘密```相同。

# 十、取得新闻内文标题

寻找标题的CSS定位同```七、观察如何抓取新浪新闻信息```中步骤一致。

```python
soup.select('#artibodyTitle')[0].text # 抓取标题
```

# 十一、取得新闻发布时间

![时间和来源.png](http://upload-images.jianshu.io/upload_images/1936544-b6b6e3330b90ff25.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```python
timesource = soup.select('.time-source')[0].contents[0].strip() # 抓取时间
```


**时间和字符串转换**

```python
from datetime import datetime

// 字符串转时间 --- strptime
dt = datetime.strptime(timesource, '%Y年%m月%d日%H:%M')

// 时间转字符串 --- strftime
dt.strftime(%Y-%m-%d)
```



# 十二、处理新闻来源信息

```python
medianame = soup.select('.time-source span a')[0].text # 抓取来源
```



# 十三、整理新闻内文

每一步的步骤分析如下：
![抓取内文1.png](http://upload-images.jianshu.io/upload_images/1936544-3a03e43476bff03e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![抓取内文2.png](http://upload-images.jianshu.io/upload_images/1936544-582cb333d967bc9d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![抓取内文3.png](http://upload-images.jianshu.io/upload_images/1936544-246b0971ae92adff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 去掉最后一行的编辑者信息。

![抓取内文4.png](http://upload-images.jianshu.io/upload_images/1936544-083eb1666fdc87c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![抓取内文5.png](http://upload-images.jianshu.io/upload_images/1936544-02a828185b0b3350.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 去掉空格。

![抓取内文6.png](http://upload-images.jianshu.io/upload_images/1936544-c446a7d3432e16b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![抓取内文7.png](http://upload-images.jianshu.io/upload_images/1936544-222c206944e4c70f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 将空格替换成```\n```，这里可以自行替换成各种其他形式。

![抓取内文8.png](http://upload-images.jianshu.io/upload_images/1936544-eae361d3b2e66464.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 简写为一句话。


# 十四、撷取新闻编辑者名称

```python
editor = soup.select('.article-editor')[0].text.lstrip('责任编辑：')
```


# 十五、抓取新闻评论数


![常规方法抓取评论](http://upload-images.jianshu.io/upload_images/1936544-e43f27c3f79c1c9d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 常规方法抓取，会发现评论数为空。

![不能采取常规办法了](http://upload-images.jianshu.io/upload_images/1936544-50672c98f52906e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 因此猜想，评论是是通过JS代码传过来的；
> 那么接着猜，既然是JS，那么通过AJAX传过来的概率很高，于是点到```XHR```中看，但是发现Response中没有出现总评论数```208```；
> 然后就只能去```JS```里面了，地毯式搜索，找哪个Response里出现了总评论数```208```，终于找到了。

![找到链接和请求方式](http://upload-images.jianshu.io/upload_images/1936544-c1facce782f51779.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 因此可以兑现代码了


![兑现代码1](http://upload-images.jianshu.io/upload_images/1936544-c8d9881f34f91e1c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![兑现代码2](http://upload-images.jianshu.io/upload_images/1936544-2a1db4521f74e35f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 可以发现通过```newsid```传了参数过来，而这个id可以通过请求页面的URL得知；
> 除此之外，还有一个```jsvar=loader_xxxxx```也传过来了一个很像时间戳的参数，这个不太好猜，于是把这个请求参数去掉试试看。

![去掉后](http://upload-images.jianshu.io/upload_images/1936544-44220da780b55065.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 去掉后，查看内容，跟上面对比，并没有大的差别。因此可以给它去掉。
> 图中的```var data={......}```看着很像是个```json```串。

![有var data=](http://upload-images.jianshu.io/upload_images/1936544-2134f5423c1e9137.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![无var data=](http://upload-images.jianshu.io/upload_images/1936544-14cdd43c6b5b1b4d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 去掉```var data=```，使其变为```json```串。

![包装成json](http://upload-images.jianshu.io/upload_images/1936544-9a7779a1331038b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 可以看到，```jd```串中就是评论的信息了。

![回到Chrome开发工具](http://upload-images.jianshu.io/upload_images/1936544-98daa177ad989a53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 回到Chrome开发工具中，这样浏览```jd```中的信息会比较快。

![Done](http://upload-images.jianshu.io/upload_images/1936544-7a7391dbd849b2fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 总评论数这时候变成了217而不是开始的208，是因为延时的关系，即操作的这段时间有9个用户又评论了。


# 十六、剖析新闻标识符

**方式1：切割法**

```python
newsurl = 'http://news.sina.com.cn/c/nd/2016-08-20/doc-ifxvctcc8121090.shtml'
newsid = newsurl.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
newsid
```

**方式2：正则表达式**

```python
import re
m = re.search('doc-i(.*).shtml', newsurl)
print(m.group(0)) # doc-ifxvctcc8121090.shtml
print(m.group(1)) # fxvctcc8121090
```


# 十七、建立评论数抽取函式

做一个总整理，把刚刚取得评论数的方法整理成一个函式。之后有新闻网页的链接丢进来，可以通过这个函式去取得它的总评论数。


```python
commentURL = 'http://comment5.new.sina.com.cn/page/info?aaa=bbb......&newsid=comos-{}&xxx=yyy&...'
```

> 注意上面的```&newsid=comos-{}```

```python
newsid = fxvctcc8121090
commentURL.format(newsid)
```

> 此时commentURL会变为```http://comment5.new.sina.com.cn/page/info?aaa=bbb......&newsid=comos-fxvctcc8121090&xxx=yyy&...```；成功完成格式化。

```python
import re
import requests
import json

def getCommentCounts(newsurl):	
    m = re.search('doc-i(.*).shtml', newsurl)
    newsid = m.group(1) # fxvctcc8121090
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']
```


# 十八、完成内文信息抽取函式

将抓取内文信息的方法整理成一函式。

```python
import requests
from bs4 import BeautifulSoup

def getNewsDetail(newsurl):
	result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text
    result['newssource'] = soup.select('.time-source span a')[0].text
    timesource = soup.select('.time-source')[0].contents[0].strip()
    result['dt'] = datetime.strptime(timesource, '%Y年%m月%d日:%H%M')
    result['article'] = '\n'.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    result['editor'] = soup.select('.article-editor')[0].text.strip('责任编辑：')
    result['comments'] = getCommentCounts(newsurl)
    return result
```


# 十九、从列表链接取出每篇新闻内容

如果```Doc```下面没有我们想要找的东西，那么就有理由怀疑，这个网页产生资料的方式，是通过非同步的方式产生的。因此需要去```XHR```和```JS```下面去找。

有时候会发现非同步方式的资料```XHR```下没有，而是在```JS```下面。这是因为这些资料会被```JS```的函式包装，Chrome的开发者工具认为这是JS文件，因此就放到了```JS```下面。

在```JS```中找到我们感兴趣的资料，然后点击```Preview```预览，如果确定是我们要找的，就可以去```Headers```中查看```Request URL```和```Request Method```了。

> 一般```JS```中的第一个可能就是我们要找的，要特别留意第一个。

![图示](http://upload-images.jianshu.io/upload_images/1936544-6203af489b43cadf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 二十、找寻分页链接

![头](http://upload-images.jianshu.io/upload_images/1936544-dbab251f9132f279.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![尾](http://upload-images.jianshu.io/upload_images/1936544-a3d3aa737d68214c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 需要去掉头和尾，将其变成标准的```json```格式。

![变成json](http://upload-images.jianshu.io/upload_images/1936544-a9df8b6d1f0f457c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 将json格式变成python的字典。


# 二十一、剖析分页信息

![获取新闻链接列表](http://upload-images.jianshu.io/upload_images/1936544-b8bc0c4232c876b0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 获取新闻链接列表

# 二十二、建立剖析清单链接函式

将前面的步骤整理一下，封装到一个函式中。

```python
def parseListLinks(url):
	newsdetails = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('newsloadercallback()').rstrip(');'))
    for ent in jd['result']['data']:
    	newsdetails.append(getNewsDetail(ent['url']))
    return newsdetails
```



# 二十三、使用for循环产生多页链接

![for循环产生多页链接](http://upload-images.jianshu.io/upload_images/1936544-c6e73080ee270c74.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 二十四、批次抓取每页新闻内文

![批次抓取每页新闻内文](http://upload-images.jianshu.io/upload_images/1936544-adbd0ea249e12a9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 二十五、使用Pandas整理数据

Python for Data Analysis

* 源于R
* Table-Like格式
* 提供高效能、简易使用的资料格式(Data Frame)让使用者可以快速操作及分析资料

![pandas范例](http://upload-images.jianshu.io/upload_images/1936544-bc158204cfc7c5b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> ```df.head()```：默认显示5条数据；
> ```df```：默认显示全部数据；
> ```df.head(10)```：默认显示10条数据。

# 二十六、保存数据到数据库

![保存至Excel或者sqlite3](http://upload-images.jianshu.io/upload_images/1936544-44d3074c9977938d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> sqlite3同oracle、mysql不一样，它不需要在操作系统上去启动一个服务，然后让客户端连接到这个服务才可以进行对数据库的操作。
> sqlite3它将所有的资料都存放在一个档案之中，在这个例子中，这个档案就叫做```news.sqlite```。执行完毕后，所有的资料都存在放```news.sqlite```这个资料库的```news```表格。

![可以保存成多种格式](http://upload-images.jianshu.io/upload_images/1936544-f2f6e460304ffffa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
