# LSP

`LSP` 的全称叫做 `Language Server Protocol`，摘录一段英文，

The Language Server protocol is used between a tool (the client) and a language smartness provider (the server) to integrate features like auto complete, go to definition, find all references and alike into the tool.
> 简单来说就是 LSP 是一个 C-S 协议。详见 https://langserver.org/

# cquery

https://github.com/jacobdufault/cquery，这个 `cquery` 是一个基于 `lsp` 的服务端实现。

`lsp-mode` 是一个 EMACS 上 `lsp` 的 client 的 lib，然后 `cquery.el` 是 EMACS 上的 client 实现；

https://melpa.org/#/cquery 在 melpa 上也有一个 `cquery`，这里不要和前面那个 `cquery` 混淆，这个是打包了 `lsp-mode` 和 `cquery.el` 的一个 package，可以理解成它是一个 **完整的 cquery 客户端**。


# 类比
| src | 类比 |
| :-- | :-- |
| jacobdufault#cquery | cquery 的服务端 |
| lsp-mode | 网关 |
| cquery.el | EMACS 的 cquery client (不包括网关) |
| melpa#cquery | 完整的 client (包括网关)  |

> vscode 上也有 cquery 的 client，去插件平台轻易能搜到，这个相当于完整的 client (包含了网关)。
