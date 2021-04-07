# 使用 stow 管理 dotfiles

管理配置文件的困难之处在于，版本管理工具如 Git 管理的话会非常方便，但是这些配置文件大部分都位于家目录的顶级目录下， **在这个位置不太适合初始化一个版本管理仓库**。

有很多工具被设计出来解决这个问题，基本思路都是把这些配置文件安置在某个下级目录中，然后安装或者链接这些文件到它们应该在的位置。 但是这些工具有两个最主要缺点：

*   有很多依赖。比如 Ruby 和一大坨库。

*   有不低的学习成本，因此需要记住如何用它。但是同步和修改配置算是低频场景了，因此要记住各自工具的用法真的挺难。

stow 就提供了一种外部依赖少、学习成本低的方式。

```shell
brew install stow
sudo apt-get install stow
```

将配置文件处理成如下的格式（下面有配图），
```
home目录/
  dotfiles/
    bash/
      .bashrc
      .bash_profile
      .bash_logout
    vim/
      .vim/
      .vimrc
    emacs/
      .emacs.d/
    zshell/
      .zshrc
```

![文件夹组织形式](https://upload-images.jianshu.io/upload_images/1936544-1834515b37eabc2c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


最后 cd 到 `home目录/dotfiles` 下，执行例如 `stow emacs` 即可自动将 `.emacs.d` 链接到家目录下，执行例如 `stow vim`  `stow zshell` 等同理。


具体详见 [http://farseerfc.me/zhs/using-gnu-stow-to-manage-your-dotfiles.html](http://farseerfc.me/zhs/using-gnu-stow-to-manage-your-dotfiles.html)


