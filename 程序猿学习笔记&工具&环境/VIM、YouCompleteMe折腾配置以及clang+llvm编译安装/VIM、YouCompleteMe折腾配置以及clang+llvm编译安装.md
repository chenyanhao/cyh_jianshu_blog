比较麻烦，未完待续。。。。。。

# VIM

配置：[```.vimrc```以及```.ycm_extra_conf.py```配置](https://github.com/chenyanhao/vim-cyh)

插件：个人觉得以下几乎是必需的插件

## 插件列表：

* Vundle： 这个绝对是首先装好
* nerdtree： 目录结构浏览
* YouCompleteMe： 超级强大的自动补全，集成了具有语法检查功能的syntactic
* tagbar： 相当于eclipse的outline
* ctrlp： 全局搜索+状态条
* powerline
> 个人更偏爱小巧轻便，所以有些鸡肋的插件不想装

## 插件地址：

* Vundle: VundleVim/Vundle.vim
* nerdtree: scrooloose/nerdtree
* YouCompleteMe: Valloric/YouCompleteMe
* tagbar: majutsushi/tagbar
* ctrlp: kien/ctrlp.vim
* powerline: powerline/powerline

## 安装YouCompleteMe

其他的插件都很好装，就是ycm不好装。

按照步骤来，一定能成功的。

如果哪里出错了，仔细从头地对照教程检查；如果每一步真的都是按照步骤来，一定可以成功。

### 安装Vundle

略

### 确保前提

Ensure that your version of Vim is at least 7.4.143 and that it has support for Python 2 or Python 3 scripting.

> **翻译：** 确保Vim版本至少为7.4.143，并且它支持Python 2或Python 3脚本。

验证：

1. 在Vim中输入 :version 可以查看版本。

2. After you have made sure that you have Vim 7.4.143+, type the following in Vim: ```echo has('python') || has('python3')```. The output should be 1. If it's 0, then get a version of Vim with Python support.

	> **翻译：** 确定Vim 7.4.143+后，在Vim中键入以下命令：```echo has（'python'）|| has（'python3'）```，输出应为1；如果它为0，那么去装一个带有Python支持的Vim版本。

### 安装YouCompleteMe插件

两种方式安装：

1. Vundle安装：```Plugin 'Valloric/YouCompleteMe'```

	> 如果用Vundle更新YCM，yum_support_lib库API改变了，YCM会提醒你重新编译它。

2. git安装：先用```git clone --recursive https://github.com/Valloric/YouCompleteMe.git```获取最新的仓库；而后使用```git submodule update --init --recursive```确认仓库的完整性后，开始安装流程


### Download the latest version of libclang: 下载libclang（版本>=3.9）
### **翻译：** 下载最新版本的libclang（3.9以上版本）

下载地址：```http://llvm.org/releases/download.html```

官方建议下二进制包：（别下错了）

* Clang for x86_64 Ubuntu 14.04 (.sig)
* Clang for x86_64 Ubuntu 16.04 (.sig)
* Clang for Mac OS X (.sig)


### 编译安装ycm_core库之前戏

Compile the ycm_core library that YCM needs. 
This library is the C++ engine that YCM uses to get fast completions.

> **翻译：** 编译YCM需要的```ycm_core```库。 这个库是YCM用来获得快速完成的C ++引擎。

编译安装```ycm_core```需要```cmake```和```python-dev```支持。

安装```cmake```:

* **Ubuntu:** ```sudo apt-get install cmake``` 
* **Mac:** ```brew install cmake```

安装```python-dev```:

* **Ubuntu:** ```sudo apt-get install python-dev python3-dev```
* **Mac:** they should already be present(Mac下，它们是现成的，不需要额外装)

Here we'll assume you installed YCM with Vundle. 
That means that the top-level YCM directory is in ```~/.vim/bundle/YouCompleteMe```.

> **翻译：** 现在我们假设你安装YCM与Vundle。 这意味着顶层YCM目录在中```~/.vim/bundle/YouCompleteMe```。

### 正式编译安装ycm_core: Compile the ycm_core library that YCM needs. This library is the C++ engine that YCM uses to get fast completions.

We'll create a new folder where build files will be placed. Run the following:

> **翻译：** 创建一个新文件夹，其中将放置构建文件。 运行以下命令：

```shell
cd ~
mkdir ycm_build
cd ycm_build
```

下一步生成```makefile```，这一步很重要，有点复杂。

> 这一步作者的原英文介绍特别冗长，这里总结了一下，列出来。作者的原文附在后面。

1. 如果不需要C族语言的语义支持，在```ycm_build```目录下执行： ```cmake -G "Unix Makefiles" . ~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp```
2. 如果需要C族语言的语义支持，还得分几种情况：
	1. 从llvm的官网下载了```LLVM+Clang```的二进制包
		* 解压到：```~/ycm_temp/llvm_root_dir```

			> 该目录下有```bin, lib, include```等文件夹
		
		* 然后执行: ```cmake -G "Unix Makefiles" -DPATH_TO_LLVM_ROOT=~/ycm_temp/llvm_root_dir . ~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp```
	2. 如果想用系统的libclang: ```cmake -G "Unix Makefiles" -DUSE_SYSTEM_LIBCLANG=ON . ~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp```
	3. 如果想用自定义的libclang: ```cmake -G "Unix Makefiles" -DEXTERNAL_LIBCLANG_PATH=/path/to/libclang.so . ~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp```
	 
	 	> ```/path/to/libclang.so```这部分填入你自己编译libclang的路径

至此，```makefile```已生成。

我自己是按照作者建议，从llvm网站下载的二进制文件，安装的。

### 生成ycm_core

```cmake --build . --target ycm_core --config Release```

### 安装完成

**至此**，YouCompleteMe已经算是**安装成功**！

**注意**：这时候，ycm_build目录可以删除啦！

> 安装成功后，```ycm_build```以及```ycm_temp```目录都可以删除，不影响YouCompleteMe插件的使用。


<br>
<br>
<br>
<br>
<br>


===================================================================================================

==================================================================================================

### (可跳过)附录：作者原文中主要步骤和关键点摘抄

Now we need to generate the makefiles. If you DON'T care about semantic support for C-family languages, run the following command in the ycm_build directory:

We'll assume you downloaded a binary distribution of LLVM+Clang from llvm.org in step 3 and that you extracted the archive file to folder ```~/ycm_temp/llvm_root_dir``` (with bin, lib, include etc. folders right inside that folder). 

NOTE: This only works with a **downloaded** LLVM binary package, not a **custom-built** LLVM! See docs below for ```EXTERNAL_LIBCLANG_PATH``` when using a custom LLVM build.

With that in mind, run the following command in the ```ycm_build``` directory:

```cmake -G "<generator>" -DPATH_TO_LLVM_ROOT=~/ycm_temp/llvm_root_dir .  ~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp```, where <generator> is ```Unix Makefiles``` on Unix systems.

Now that configuration files have been generated, compile the libraries using this command: ```cmake --build . --target ycm_core --config Release```

> The ```--config Release``` part is specific to Windows and will be ignored on a Unix OS.

For those who want to use the system version of libclang, you would pass ```-DUSE_SYSTEM_LIBCLANG=ON``` to cmake instead of the ```-DPATH_TO_LLVM_ROOT=...``` flag.

> **注意作者这里的NOTE提示：**

NOTE: We **STRONGLY** recommend **AGAINST** use of the system libclang instead of the upstream compiled binaries. Random things may break. Save yourself the hassle and use the upstream pre-built libclang.

> **如果是custom libclang而不是downloaded LLVM binary package：**

You could also force the use of a custom libclang library with ```-DEXTERNAL_LIBCLANG_PATH=/path/to/libclang.so``` flag (the library would end with .dylib on a Mac). Again, this flag would be used instead of the other flags. 
**If you compiled LLVM from source, this is the flag you should be using.**

Running the cmake command will also place the ```libclang.[so|dylib|dll]``` in the ```YouCompleteMe/third_party/ycmd``` folder for you if you compiled with clang support (it needs to be there for YCM to work).

Don't forget that if you want the C-family semantic completion engine to work, 
you will need to provide the compilation flags for your project to YCM. 

==================================================================================================

==================================================================================================

<br>
<br>
<br>
<br>
<br>


### 配置

1. 前戏准备

	```
	    cp ~/.vim/bundle/YouCompleteMe/third_party/ycmd/examples/.ycm_extra_conf.py ~/  
	    vim ~/.ycm_extra_conf.py
	    
	    /*
	    ** 注：下面需要注释的内容只有稍微老一点的版本才有，最新的是没有的
	    */
	    // 如果有如下内容，注释掉:
	    try:  
	      final_flags.remove( '-stdlib=libc++' )  
	    except ValueError:  
	      pass 
	    // 注释完后变成下面这样
	    #try:  
	    #  final_flags.remove( '-stdlib=libc++' )  
	    #except ValueError:  
	    #  pass 
	```
2. ```.vimrc```中的配置

	``` vim
	" #####YouCompleteMe Configure   
	let g:ycm_global_ycm_extra_conf = '~/.ycm_extra_conf.py'  
	" 自动补全配置  
	set completeopt=longest,menu    "让Vim的补全菜单行为与一般IDE一致(参考VimTip1228)  
	autocmd InsertLeave * if pumvisible() == 0|pclose|endif "离开插入模式后自动关闭预览窗口  
	inoremap <expr> <CR>       pumvisible() ? "\<C-y>" : "\<CR>"    "回车即选中当前项  
	"上下左右键的行为 会显示其他信息  
	"inoremap <expr> <Down>     pumvisible() ? "\<C-n>" : "\<Down>"  
	"inoremap <expr> <Up>       pumvisible() ? "\<C-p>" : "\<Up>"  
	"inoremap <expr> <PageDown> pumvisible() ? "\<PageDown>\<C-p>\<C-n>" : "\<PageDown>"  
	"inoremap <expr> <PageUp>   pumvisible() ? "\<PageUp>\<C-p>\<C-n>" : "\<PageUp>"  
	  
	"youcompleteme  默认tab  s-tab 和自动补全冲突  
	"let g:ycm_key_list_select_completion=['<c-n>']  
	let g:ycm_key_list_select_completion = ['<Down>']  
	"let g:ycm_key_list_previous_completion=['<c-p>']  
	let g:ycm_key_list_previous_completion = ['<Up>']  
	let g:ycm_confirm_extra_conf=0 "关闭加载.ycm_extra_conf.py提示  
	  
	let g:ycm_collect_identifiers_from_tags_files=1 " 开启 YCM 基于标签引擎  
	let g:ycm_min_num_of_chars_for_completion=2 " 从第2个键入字符就开始罗列匹配项  
	let g:ycm_cache_omnifunc=0  " 禁止缓存匹配项,每次都重新生成匹配项  
	let g:ycm_seed_identifiers_with_syntax=1    " 语法关键字补全  
	nnoremap <F5> :YcmForceCompileAndDiagnostics<CR>    "force recomile with syntastic  
	"nnoremap <leader>lo :lopen<CR> "open locationlist  
	"nnoremap <leader>lc :lclose<CR>    "close locationlist  
	inoremap <leader><leader> <C-x><C-o>  
	"在注释输入中也能补全  
	let g:ycm_complete_in_comments = 1  
	"在字符串输入中也能补全  
	let g:ycm_complete_in_strings = 1  
	"注释和字符串中的文字也会被收入补全  
	let g:ycm_collect_identifiers_from_comments_and_strings = 0  
	let g:clang_user_options='|| exit 0'  
	"nnoremap <leader>jd :YcmCompleter GoToDefinitionElseDeclaration<CR> " 跳转到定义处  
	" #####YouCompleteMe Configure   
	```

3. ```.ycm_extra_conf.py```中的配置

	1. 用命令查看库路径

		```
		echo | clang -v -E -x c++ -
		```
		```
		结果可能如下：
		clang version 3.6.2 (tags/RELEASE_362/final)
		Target: i386-pc-linux-gnu
		Thread model: posix
		Found candidate GCC installation: /usr/lib/gcc/i686-redhat-linux/4.4.4
		Found candidate GCC installation: /usr/lib/gcc/i686-redhat-linux/4.4.7
		Found candidate GCC installation: /usr/local/bin/../lib/gcc/i686-pc-linux-gnu/4.8.1
		Selected GCC installation: /usr/local/bin/../lib/gcc/i686-pc-linux-gnu/4.8.1
		Candidate multilib: .;@m32
		Selected multilib: .;@m32
		太长了，这里省略一部分中间内容；.........表示生咯的内容
		 "/usr/local/bin/clang" -cc1 -triple ......... -mstackrealign -fobjc-runtime=gcc  directory "/include"
		#include "..." search starts here: 
		这里没有显示任何东西,所以不需要包含任何路径
		#include <...> search starts here:
		这里就是需要包含的路径下面这些都是需要包含的路径
		 /usr/local/bin/../lib/gcc/i686-pc-linux-gnu/4.8.1/../../../../include/c++/4.8.1
		 /usr/local/bin/../lib/gcc/i686-pc-linux-gnu/4.8.1/../../../../include/c++/4.8.1/i686-pc-linux-gnu
		 /usr/local/bin/../lib/gcc/i686-pc-linux-gnu/4.8.1/../../../../include/c++/4.8.1/backward
		 /usr/local/include
		 /usr/local/bin/../lib/clang/3.6.2/include
		 /usr/include
		End of search list.
		# 1 "<stdin>"
		# 1 "<built-in>" 1
		# 1 "<built-in>" 3
		# 318 "<built-in>" 3
		# 1 "<command line>" 1
		# 1 "<built-in>" 2
		# 1 "<stdin>" 2
		```

	2. 整理上述内容，并添加到flag中

		```
		将以上内容复制出来,修改成如下:
		 '-isystem',
		 '/usr/local/bin/../lib/gcc/i686-pc-linux-gnu/4.8.1/../../../../include/c++/4.8.1',
		 '-isystem',
		 '/usr/local/bin/../lib/gcc/i686-pc-linux-gnu/4.8.1/../../../../include/c++/4.8.1/i686-pc-linux-gnu',
		 '-isystem',
		 '/usr/local/bin/../lib/gcc/i686-pc-linux-gnu/4.8.1/../../../../include/c++/4.8.1/backward',
		 '-isystem',
		 '/usr/local/include',
		 '-isystem',
		 '/usr/local/bin/../lib/clang/3.6.2/include',
		 '-isystem',
		 '/usr/include',
		```

> 补全 C 语言全局函数问题(vim ~/.vimrc文件修改)

>默认情况下输入 ., ->, :: 之后会触发补全函数和类， 但是默认情况下是不补全全局函数的，所以 C 语言中的 printf 之类的函数就无法补全

>解决办法就是手动调用补全，对应的 YCM 函数是 ```ycm_key_invoke_completion```，将其绑定到快捷键 let ```g:ycm_key_invoke_completion = '<C-a>'```（默认是 <C-Space>）


# 编译安装clang+llvm

## Clang和LLVM的关系

Clang和LLVM到底是什么关系，这是在研究Clang的过程中所不可避免的一个问题。如果要搞清楚Clang和LLVM之间的关系，首先先要知道 **宏观的LLVM** 和 **微观的LLVM** 。

**宏观的LLVM** ，指的是整个的LLVM的框架，它肯定包含了Clang，因为Clang是LLVM的框架的一部分，是它的一个C/C++的前端。虽然这个前端占的比重比较大，但是它依然只是个前端，LLVM框架可以有很多个前端和很多个后端，只要你想继续扩展。

**微观的LLVM** ，指的是以实际开发过程中，包括实际使用过程中，划分出来的LLVM。比如编译LLVM和Clang的时候，LLVM的源码包是不包含Clang的源码包的，需要单独下载Clang的源码包。

所以这里想讨论的是 **微观的** LLVM和Clang的关系。从编译器用户的角度，Clang使用了LLVM中的一些功能，目前所知道的主要就是对中间格式代码的优化，或许还有一部分生成代码的功能。从Clang和微观LLVM的源码位置可以看出，Clang是基于微观的LLVM的一个工具。而 **从功能的角度来说，微观的LLVM可以认为是一个编译器的后端，而Clang是一个编译器的前端** 。

## 编译安装

先说一下目录结构：

```
llvm
	tools
		clang(cfe)
			tools
				extra(clang-tools-extra)
	projects
		compiler-rt
```

1. 下载llvm的源代码

	```
	wget http://llvm.org/releases/3.9.0/llvm-3.9.0.src.tar.xz
	tar xf llvm-3.9.0.src.tar.xz
	mv llvm-3.9.0.src llvm
	```

2. 下载clang的源代码

	```
	cd llvm/tools
	wget http://llvm.org/releases/3.9.0/cfe-3.9.0.src.tar.xz
	tar xf cfe-3.9.0.src.tar.xz
	mv cfe-3.9.0.src clang
	cd ../..
	```

3. 下载clang-tools-extra的源代码

	```
	cd llvm/tools/clang/tools
	wget http://llvm.org/releases/3.9.0/clang-tools-extra-3.9.0.src.tar.xz
	tar xf clang-tools-extra-3.9.0.src.tar.xz
	mv clang-tools-extra-3.9.0.src  extra
	cd ../../../..
	```

4. 下载compiler-rt的源代码

	```
	cd llvm/projects
	wget http://llvm.org/releases/3.9.0/compiler-rt-3.9.0.src.tar.xz
	tar xf compiler-rt-3.9.0.src.tar.xz
	mv compiler-rt-3.9.0.src compiler-rt
	cd ../..
	```

	这样之后 clang，clang-tool-extra 和 compiler-rt 就可以和 llvm 一起编译了。

5. 编译安装

	**注意：** 3.7.0以后，不允许在源码树中进行构建，我们可以在llvm源码目录同级目录中创建一个目录build目录，然后使用绝对路径进行构建

	```
	./configure --enable-optimized --enable-targets=host-only --prefix=/home/YouPathToInstall/llvm
	```

	> 最后一个编译选项时指定编译路径，前面两个也尽量加上。
	> 不然编译时间的时候会时间很长而且占很大的文件空间。

	```
	make -j4 // 编译使用4核cpu一起编译,加快编译速度
	make install
	```

6. 检查是否安装成功: ```clang –version```

7. 完毕之后

	```
	cd ~/.vim/bundle/YouCompleteMe 
	mkdir ~/build  
	cd ~/build  
	#libclang.so 这个路径,查询的时候updatedb更新locate的数据  
	locate libclang.so  
	~/.vim/bundle/YouCompleteMe/third_party/ycmd/libclang.so  
	~/clang/build/Release+Asserts/lib/libclang.so  
	/usr/local/lib/libclang.so  
	cmake -G "Unix Makefiles"  ~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp/ -DEXTERNAL_LIBCLANG_PATH=~/clang/build/Release+Asserts/lib/libclang.so
	```
	> 要注意的是-DEXTERNAL_LIBCLANG_PATH这个参数，用于指定libclang.so的位置。如果不指定的话，YCM将无法正常工作，总是报：The YCM shut down, crash report...之类的错误。而这个libclang.so就是我们在编译Clang的时候生成的。因此，相关路径也即```~/clang/build/Release+Asserts/lib/libclang.so```需要替换成自己对应的路径。
