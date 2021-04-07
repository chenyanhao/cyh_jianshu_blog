# 桌面

Linux 发行版及其桌面我感兴趣的有：Manjaro（Kde）、linuxmint（mint）、deepin（DDE）。

单说桌面的话，人气较高的一般有这些：KDE、GNOME、mint、XFCE 等。2018 年时候的某个时间点，某个国外的网站统计了桌面占比排名，由高到低分别是：gnome、kde、cinnamon(mint)、mate、xfce4。Linus 大神用的是 xfce4，哈哈。

gnome 基于 gtk，C 项目（gtk 要用 C 写面向对象，所以对于普通人来说写起来稍微蛋疼和啰嗦，大神级别除外）；kde 基于 qt，C++ 项目。
XFCE4 基于 GTK，所以可以说 XFCE4 主要是 C 语言写成的。
deepin 的 DDE 桌面最初似乎是基于 H5，H5 写桌面肯定性能不佳，后来用 Qt 重写了。

另外说一点，现在在开源软件中 UI 大多都选择 Qt 了，好多也在往 Qt  迁移，例如 LXDE 都在迁移到Qt。一些需要跨平台的软件也迁移到 Qt 了，例如 WPS。

 Qt 的优点是，在软件质量、功能、API 设计、文档等方面广受赞誉。Qt 的缺点是，Qt 的 UI 运行效率与 wxWidgets、Windows 的 MFC，Linux 的 GTK+ 都没法比。主要原因之一是 Qt 的信号槽这个核心机制，给开发带来便利，但代价是丧失了一些性能。
但是 GTK+ 也有它自身的问题。有人认为，要不是 Qt 过去有协议问题，连 gnome 都不会用 GTK+ 。


gnome 似乎“作死”过一下，具体历史可以查查，分出来了 GNOME2 和 GNOME3。现在大家谈论的某某发行版配置的 GNOME 桌面，一般指的是 GNOME3。

基于 GNOME 的 2 和 3，又衍生出来一些，例如 cinnamon/mint 桌面是属于 gnome3 的fork；mate 桌面是属于 gnome2 的 fork。
不过基于 GNOME3 的 Cinnamon/mint 与 GNOME 的发展方向是完全背道而驰的，所以 Cinnamon/mint 发展得很不容易。


# 显示管理器

这里再多说点一些“名词”，例如 gdm、kdm、lightdm。它们称作“显示管理器”，或者“登录管理器”，它们向用户显示登录屏幕，提供登录的图形界面并处理用户身份验证等问题。简单来说，显示管理器可以理解为，它是一个在图形界面，是进到桌面环境之前的用户登录界面。

显示管理器目前最主要是 gdm、kdm、lightdm 这三个。
- dm3 是 gdm 的后继者，它是 GNOME 显示管理器。较新的 gdm3 使用 gnome-shell 的最小版本，并提供与 GNOME3 会话相同的外观。例如 Ubuntu 默认版配置的这个。
- kdm 是 KDE4 的显示管理器，已被弃用。目前在 KDE5 中取而代之的是 SDDM。SDDM 是基于 QML 的显示管理器，KDE 4 的 kdm 的继任者，Plasma 5 以及 LXQt 推荐。例如 Ubuntu 的 KDE 版本 KUbuntu 配置的是 SDDM。
- LightDM 是 Canonical/mint 的显示管理器解决方案，它比较轻量级的。是 Ubuntu 开发的 GDM 替代品，使用 WebKit。例如 Xubuntu/Lubuntu 配置。

除了这几个之外，还有很多很多显示管理器，大概如下（来自网络资源），
- Entrance：基于 EFL 的显示管理器，高度实验性质。
- LXDM：LXDE 显示管理器 ，可以独立于 LXDE 桌面环境使用。
- MDM：MDM 显示管理器，在 Linux Mint 中使用， GDM 2 的一个 fork。
- SLiM：简单登录管理器，轻量且优雅的图形化登录解决方案（不再继续开发）。
- XDM：X 显示管理器 (xorg-xdm)，带有 XDMCP，主机选择支持的 X 显示管理器。个人猜测比如 XWINDOW 可能就是用的这个。

> 注意: 如果使用 桌面环境,应该尽量使用对应的显示管理器。







Qingy: getty 使用 DirectFB 的替代者 (qingy)
wdm: WINGs 显示管理器 (wdm)
CDM: 控制台显示管理器 (available in the AUR: cdm-git)




