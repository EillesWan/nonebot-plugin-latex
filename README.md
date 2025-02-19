# nonebot-plugin-latex

NoneBot2 LaTeX 图形渲染插件

通过互联网公共服务渲染 LaTeX 公式

利用 www.latex2png.com 和 latex.codecogs.com 在线渲染 LaTeX 公式

## 安装

```bash
pip install nonebot-plugin-latex
```

## 使用

如果希望直接作为 LaTeX 渲染插件使用的话，请在 NoneBot 配置文件中添加以下内容：

```env
latex_enable_as_application = true
```

这样就可以使用 `latex` 命令进行渲染了，例如 `latex $E=mc^2$` 就会返回这个方程式的渲染图片。

## 提交

各位可以搭建自己的 LaTeX 在线渲染服务，或者直接本地渲染，如果提交到本仓库，在下不胜感激。\
对于本地渲染服务，请不要使用 nonebot-plugin-htmlrender