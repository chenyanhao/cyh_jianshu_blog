#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import urllib.request
import os
import os.path
import re 


def process_file(src_path, dst_path, file_name):
    img_index = 0
    new_content = []
    import codecs 
    # 例如： ![xxx](https://www.xxx.com/ouo/ei/gh/skd/hg) 
    # 有时候也会有这种情况 ![xxx](https://www.xxx.com/ouo/ei/gh/skd/hg "image") 
    pattern = r"^!\[.*\]\(https:(.*)\)$" 
    with codecs.open(src_path + os.sep + file_name, 'r') as f:
        lines = f.readlines()
        # 迭代原文本中的每一行，如果非图片插入，则正常处理；如果是图片插入，则下载图片、替换图片网络地址为本地图片路径
        for line in lines:
            matched = re.match(pattern, line.strip())
            if matched is not None:
                img_index += 1
                img_url = 'https:' + matched.group(1)
                img_url = img_url.strip().split(' ')[0]
                download_img(img_url, dst_path, '{}.png'.format(img_index))
                img_content_new = '![image](./{}.png)'.format(img_index)
                new_content.append(img_content_new)
            else:
                new_content.append(line)

    new_content = ''.join(new_content)

    # 覆盖写入
    path = dst_path + os.sep + file_name
    with codecs.open(path, 'w') as f:
        f.write(new_content)
        f.flush()
    
    print('{} process success.\t\t\t totally {} images'.format(src_path.split('/')[-1] + os.sep + file_name, img_index))



def download_img(img_url, dst_path, img_name):
    try:
        #是否有这个路径
        if not os.path.exists(dst_path):
            #创建路径
            os.makedirs(dst_path)
        #拼接图片名（包含路径）
        file_name = '{}{}{}'.format(dst_path, os.sep, img_name)
        #下载图片，并保存到文件夹中
        urllib.request.urlretrieve(img_url, filename=file_name)
        # print('{} image download success.'.format(dst_path))
    except IOError as e:
        print("download_img IOError, dst_path={}, img_name={}, mg_url={} ".format(dst_path, img_name, img_url), e)
    except Exception as e:
        print("download_img Exception, dst_path={}, img_name={}, mg_url={} ".format(dst_path, img_name, img_url), e)



'''
example:

src_path (dir)
- Haskell (dir) (child_dir_src)
    - H1.md (file)
    - H2.md (file)
- Rust(dir)
    - R1.md (file)


dst_path (dir)
- Haskell (dir) 
    - H1 (dir)
        - H1.md (file)
        - 1.png (file)
    - H2 (dir) 
        - H2.md (file)
- Rust(dir)
    - R1 (dir)
        - R1.md (file)
'''
src_path = '/Users/yj/cyh_jianshu_blog/jianshu原格式'
dst_path = '/Users/yj/cyh_jianshu_blog'

if src_path.endswith('/'):
    src_path = src_path[0:len(src_path)-1]

if dst_path.endswith('/'):
    dst_path = dst_path[0:len(dst_path)-1]


child_dir_list = os.listdir(src_path) # is a list
for dir_name in child_dir_list:
    child_dir_src = src_path + os.sep + dir_name # src_path/Haskell
    if os.path.isfile(child_dir_src):
        continue
    elif os.path.isdir(child_dir_src):
        for file_name in os.listdir(child_dir_src): # file_name = H1.md
            child_dir_dst = dst_path + os.sep + dir_name + os.sep + file_name.split('.')[0] # dst_path/Haskell/H1
            if not os.path.exists(child_dir_dst):
                os.makedirs(child_dir_dst)
            # child_dir_src=src_path/Haskell    child_dir_dst=dst_path/Haskell/H1    file_name=H1.md
            process_file(child_dir_src, child_dir_dst, file_name) 
