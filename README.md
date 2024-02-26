# SimpLedger
简说记账系统源码，包括但不限于：Web页面、飞书机器人、微信机器人功能，持续更新。

## 环境安装

在自己的阿里云/腾讯云或者其他服务器（需要有公网ip）先手动安装 miniconda，然后运行以下指令安装环境。

当然本地使用内网穿透也可以的。

```bash
git clone https://github.com/XksA-me/SimpLedger
# 如果国内下载慢加个镜像源
# git clone https://mirror.ghproxy.com/https://github.com/XksA-me/SimpLedgerr
cd SimpLedger
conda create -n SimpLedger python=3.9
conda activate SimpLedger
pip install -r requirements.txt
```

## 运行程序

修改 configs_tmp.ini 名称为 configs.ini，并将文件内容改为对应值。
```bash
[env]
APP_ID = 飞书机器人ID
APP_SECRET = 飞书机器人SECRET
SPREADSHEET_TOKEN = 电子表格SPREADSHEET
SHEET_ID = 电子表格SHEET
```
具体获取方式看教程：

```bash
# 进入项目目录
# cd SimpLedger
python feishu/feishu_backend.py
# 也可以nohup挂后台
# nohup python -u feishu/feishu_backend.py > feishu/run.log 2>&1 &
```

详细代码和机器人构建教程：

## 功能更新计划

简说记账系统：

- [x] 飞书记账机器人
- [ ] 钉钉记账机器人
- [ ] 微信记账机器人
- [ ] Web端


## 作者简介

老表，16年开始自学，分享Python，SQL零基础入门、数据分析、数据挖掘、机器学习优质文章以及学习经验。

个人公众号：简说Python

<img src="./files/images/qr.jpg"  alt="老表微信" style="zoom:80%;" />

微信交流：

<img src="files/images/wx.jpeg" alt="老表微信" style="zoom:50%;" />

掘金主页：https://juejin.cn/user/993614243314551

CSDN主页：https://blog.csdn.net/qq_39241986

个人网站：https://python-brief.com/



## 支持与贡献

后面陆续会更新微信记账机器人、钉钉记账机器人、记账系统Web端等功能。



有其他相关想法或者建议欢迎加我微信私聊。



如果觉得项目代码还可以，欢迎点个 Star。



支持远程部署+教学服务，加微信说明需求即可。

