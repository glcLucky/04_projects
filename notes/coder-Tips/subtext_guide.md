# 一. 常用的Packages
----

## 1. Package Control

包管理器是必备的，新下载的Sublime Text 2第一个装的肯定是这个，有了它，装其他的包就很方便了。

安装方式有两种，第一种是在线下载安装：在 Sublime Text 2 中按下ctrl+\`（就是大键盘数字1左边的那个键），拷贝以下命令到窗口下部的终端中

    import urllib2,os; pf='Package Control.sublime-package'; ipp=sublime.installed_packages_path(); os.makedirs(ipp) if not os.path.exists(ipp) else None; urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler())); open(os.path.join(ipp,pf),'wb').write(urllib2.urlopen('http://sublime.wbond.net/'+pf.replace(' ','%20')).read()); print 'Please restart Sublime Text to finish installation'  

  在安装完包管理器之后，只要按下ctrl+shift+p，输入**ip**，选择“Package Control: Install Package”，然后输入要安装的包的名称，就可以在线安装了。

只要按下`ctrl+shift+p`，输入**ip** 即可进入安装包程序 输入**remove** 进入卸载包程序


## 2. SODO
这是个主题，也就是Sublime自身的皮肤，比自带的要漂亮一些。在包管理器中装上之后，打开配置文件`Preferences` -> `Settings` - `User`，加上一行"theme": "Soda Light.sublime-theme"或者 "theme": "Soda Dark.sublime-theme"。前面一个是亮色主题，后面一个是暗色主题。我喜欢暗色，看起来比较有黑客的调调。




## 3. Markdown Build and MarkDown preview

这两个是写Markdown必备的。可以在包管理器中安装。装完之后，写作Markdown时（右下角显示语法为Markdown），可以按ctrl+b，直接就会生成HTML，并在浏览器中显示。

如果仅仅想看md的效果的话，可以在 `Preferences` -> `Key Bindings User` 中加上如下代码：
    { "keys": ["alt+m"], "command": "markdown_preview", "args": { "target": "browser"} }

还需要修改下配置,将下面代码拷入MarkDown preview的个人设置中:

``` 
    {
"enable_mathjax": true,
"enable_autoreload": true,
"enable_uml": true
}
```
第一个表示支持mathjax
第二个表示启动实时更新 保存后刷新

若要支持mathjax 还需要安装`MathJax库` 方法如下:

```
下载MathJax：https://github.com/downloads/timonwong/OmniMarkupPreviewer/mathjax.zip
然后解压到下面的目录里：
${Packages} \OmniMarkupPreviewer\public
之后在目录${Packages} \OmniMarkupPreviewer中创建一个空文件MATHJAX.DOWNLOADED
这样子MathJax就安装成功了。 
```



## 4. SublimeLinter
这是用来在写代码时做代码检查的。可以在包管理器中安装。写Python程序的话，它还会帮你查代码是否符合PEP8的要求。有问题有代码会出现白框，点击时底下的状态栏会提示出什么问题。
必须按照pycodestyle才生效
SublimeLinter-pycodestyle

## 5. Python PEP8 Autoformat

这是用来按PEP8自动格式化代码的。可以在包管理器中安装。如果以前写程序不留意的话，用SublimeLinter一查，满屏都是白框框，只要装上这个包，按ctrl+shift+r，代码就会按PEP8要求自动格式化了，一屏的白框几乎都消失了。

## 6. gbk

听说Sublime Text 2读GBK编码的文件会乱码，所以我早早就把这个给装上了，没见过乱码，不知管用不。

## 7. Bracket Highlighter

这是用来做括号匹配高亮的，可以在包管理器中安装。Sublime Text 2自带的括号匹配只有小小的一横线，太不显眼了，这个可以让高亮变成大大的一坨，不过我觉得它大得会盖住光标了。

## 8. Terminal

这是用来在当前文件所在位置打开终端的。可以在包管理器中安装。对于Windows用户，安装完后，要先在Preferences -> Package Setting -> Terminal -> Settings - Default里，设置"terminal": "cmd",。（如果喜欢用ipython的话，也可以改为ipython）之后只要按下ctrl+shift+t，即可在当前文件位置打开命令行窗口。


## 9. SideBarEnhancements
这是用来增强左边的侧边栏。左侧边栏可以在View -> Side Bar -> Show Side Bar中打开，可以用Project -> Add Folder to Project...往侧边栏加入常用的文件夹。装完这个插件，侧边栏的右键菜单会多一些功能，挺实用的。


## 10. Boxy
Boxy（The most hackable theme for Sublime Text 3）；自带多种主题风格，
可以融合ihodev/sublime-file-icons；切换主题风格不必改配置；还用废那心思自己改主题去？简单够用就好！
安装方法：Ctr+Shift+P


## 11. Jedi - Python autocompletion Jedi
比较强大的python代码补全功能

1. `install package` -> Boxy Theme

2. `install package` -> A File Icon


# 二. 常用的快捷键
----

## 1. 默认

- `ctrl+shift+p` 基本上啥功能都在里面了
- `ctrl+r` 快速定位到指定类/函数/标题
- `ctrl+g` 快速跳转到某一行号，在debug时很常用
- `ctrl+b` build
- `ctrl+shift+t` 在当前位置打开终端（需安装terminal）
- `ctrl+shift+r` 按PEP8格式化代码（需安装Python PEP8 Autoformat）
- `ctrl+D` 多重选择
- `shift+Tab` prev_field 
- `ctrl+tab` prev_view_in_stack 浏览上一个tab
- `ctrl+k+u` uppcase
- `ctrl+k+l` lowercase

## 2. 自定义

### 2.1 按下`ENTER`跳出括号

在`Preferences` -> `Key Bindings User`中的中括号里加上如下代码:(注意前面加个逗号)
 ```python代码
   
        [  
        {"keys": ["enter"], "command": "move", "args": {"by": "characters", "forward": true}, "context":  
            [  
                { "key": "following_text", "operator": "regex_contains", "operand": "^[)\\]\\>\\'\\\"\\ %>\\}\\;\\,]", "match_all": true },  
                { "key": "preceding_text", "operator": "not_regex_match", "operand": "^.*\\{$", "match_all": true  },  
                { "key": "auto_complete_visible", "operator": "equal", "operand": false }  
            ]  
        }  
    ]  
```


# 三. 进阶玩法
----

## 1. 修改行距

可以参考如下博客:
[修改行距](http://www.feelcss.com/sublime-text-2-settings.html)

## 2. 设置字体
-[1] 下载安装 Microsoft Yahei Mono
-[2] ```preference``` -> ```settings-user```:

``` 
     "font_size": 14,
     "font_face": "Microsoft Yahei Mono",
     "tab_size": 4,
     "translate_tabs_to_spaces": true,
     "word_wrap": true,
     "word_wrap_column": 100,
```

## 3. 设置当前语法为python的快捷方法

ctrl+shift+p 输入sspy即可将当前语言设置为python
