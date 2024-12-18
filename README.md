<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-addons-manager/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-addons-manager/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-addons-manager

_✨ 求生之路addons文件夹Q群管理插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-addons-manager.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-addons-manager">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-addons-manager.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

这个插件是用来对求生之路服务器上的addons文件夹进行管理，使用此插件可以方便在QQ群中直接进行vpk文件的增删改查，其中除了查询以外的所有操作均可设置插件管理员权限，防止恶意破坏服务器文件夹，如果不想让他人查询服务器上的特定vpk文件，可以将文件后缀设置为VPK，上传vpk文件只需有权限的人将vpk文件传至群文件即可，其余指令请查看下面使用部分

**如果觉得插件不错的话请动手点点右上角的star收藏一下**

#### 完整搭建QQ群机器人：
1. 安装nonebot2
2. 下载插件，下载安装查看下面安装部分
3. 将nonebot与机器人框架对接，如NapCat，LLOneBot

#### 参考资料：
1. <a href="https://blog.csdn.net/iteapoy/article/details/141254725?ops_request_misc=%257B%2522request%255Fid%2522%253A%25229784319256f6f0009c0e7e959b22a141%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=9784319256f6f0009c0e7e959b22a141&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-2-141254725-null-null.142^v100^pc_search_result_base7&utm_term=nonebot&spm=1018.2226.3001.4187">
   <p>Python聊天机器人-NoneBot2入门</p>
</a>

2. <a href="https://nonebot.dev/docs/">
   <p>NoneBot官方文档</p>
</a>

3. <a href="https://llonebot.github.io/zh-CN/guide/getting-started">
    <p>LLOneBot官方文档</p>
</a>

4. <a href="https://napneko.pages.dev/config/basic">
   <p>NapCat官方文档</p>
</a>

借鉴了一些下面两个插件的代码与思路：
1. <a href="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query">
   <p>nonebot-plugin-valve-server-query</p>
</a>

2. <a href="https://github.com/Agnes4m/nonebot_plugin_l4d2_server">
   <p>nonebot_plugin_l4d2_server</p>
</a>


## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-addons-manager

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-addons-manager
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-addons-manager
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-addons-manager
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-addons-manager
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_addons_manager"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 |                                                       说明                                                        |
|:-----:|:----:|:----:|:---------------------------------------------------------------------------------------------------------------:|
| destination_path | 是 | 无 | addons文件夹的路径 例：destination_path="/root/Steam/steamapps/common/Left 4 Dead 2 Dedicated Server/left4dead2/addons" |
| admin_qq | 否 | [] |                          将管理员的QQ添加至列表中，多个管理员用逗号隔开，该值为空即所有人均有权限 例：admin_qq=[1111,2222]                           |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| /file | 所有人 | 否 | 群聊 | 查询当前服务器中的所有vpk文件 |
| /rename | 插件管理员 | 否 | 群聊/私聊 | 重命名vpk文件名字，原名字和新名字之间用逗号隔开 |
| /delete | 插件管理员 | 否 | 群聊/私聊 | 删除服务器vpk文件，紧跟需要删除的vpk文件名 |
| 无 | 插件管理员 | 否 | 群聊 | 插件管理员直接上传vpk文件，检测到vpk文件之后会自动下载至addons文件夹中 |
### 效果图
#### 上传文件
<img src="images/uoload.png">

#### 查询文件
<img src="images/query.png">

#### 修改文件名
<img src="images/rename.png">

#### 删除文件
<img src="images/delete.png">
