

homebrew

brew install vim macvim python3 git stow

oh-my-zsh [https://ohmyz.sh/#install](https://ohmyz.sh/#install)

下载安装
搜狗输入法 [https://pinyin.sogou.com/mac/](https://pinyin.sogou.com/mac/)
item2 [https://www.iterm2.com/downloads.html](https://www.iterm2.com/downloads.html)
alfred [https://xclient.info/s/alfred.html#versions](https://xclient.info/s/alfred.html#versions)
emacs25.3 [https://emacsformacosx.com/builds](https://emacsformacosx.com/builds)
vscode 下载完后安装 setting-sync 插件，拉取远程配置 https://code.visualstudio.com/
chrome 
firefox 注意不要下载了国内版的，要下载国际版 [https://www.mozilla.org/en-US/firefox/new/](https://www.mozilla.org/en-US/firefox/new/)
pycharm
app cleaner & uninstaller pro [https://xclient.info/s/app-cleaner-uninstaller-pro.html#versions](https://xclient.info/s/app-cleaner-uninstaller-pro.html#versions)
istatistica pro [https://xclient.info/s/istatistica-pro.html#versions](https://xclient.info/s/istatistica-pro.html#versions)
office
IINA [https://www.iina.io/](https://www.iina.io/)
the unarchiver [https://www.theunarchiver.com/](https://www.theunarchiver.com/)
Scroll Reverser [https://pilotmoon.com/scrollreverser/](https://pilotmoon.com/scrollreverser/)

然后将 dotfiles-mac 拉取到本地，并通过 stow 初始化配置文件。
```
cd ~
git clone https://github.com/chenyanhao/dotfiles-mac.git
cd dotfiles-mac
stow vim
stow emacs 
stow zshell
...
```


设置一位数的密码
终端输入：`pwpolicy -clearaccountpolicies`，然后 `系统偏好设置 > 用户与群组` 中更改成一位数密码即可。

默认电脑名很长，建议改短，`系统偏好设置 > 共享` 中修改后注销重新登录即可。


显示隐藏文件：`defaults write com.apple.finder AppleShowAllFiles -bool true`
不显示隐藏文件：`defaults write com.apple.finder AppleShowAllFiles -bool false`
显示/不显示隐藏文件，快捷键操作：`shift+cmmand+.`

