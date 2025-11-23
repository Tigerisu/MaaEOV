---
order: 4
icon: material-symbols:terminal
---
# MaaPiCli 使用

本节将介绍 MaaPiCli 的使用方法（翻译）

## 选择ADB

当您初次下载，没有配置时会出现下面界面：

```plaintext
异象回声小助手
MaaFramework: vX.X.X

Version: vX.X.X

### Select ADB ###

        1. Auto detect
        2. Manual input

Please input [1-2]:
```

这里 Version 后跟着的是当前资源版本。  
`### Select ADB ###` 翻译过来是当前操作为 `选择 ADB（Android Debug Bridge，这里一般用来操作模拟器）`。  
后面列出选项：

1. 自动检测（推荐，在目标模拟器启动时选择）
2. 手动输入（参考[ADB 路径](./连接设置.md#adb-路径)和[ADB 连接地址](./连接设置.md#adb-地址)填写）

后面 `Please input [1-2]:` 翻译过来是 `请输入 [选项范围]`，请根据需要选择。

这里我们输入 1 后回车，进入下一步。

## 选择设备

紧跟上一步，选择自动检测可到此步骤，显示为：

```plaintext
Finding device...

## Select Device ##

        1. MuMuPlayer12
                D:/Program Files/Netease/MuMu Player 12/shell/adb.exe
                127.0.0.1:16384

Please input [1-1]:
```

这里因为只开了一个模拟器，只显示一条选项，直接输入 1 后回车，完成此步骤

## 选择资源

```plaintext
### Select resource ###

        1. 官服
        2. Bilibili

Please input [1-2]:
```

这里根据需要的资源进行选择，主要和 `启动游戏` 等各个服务器有所区别的功能有关。

## 添加任务

这里是添加任务，显示如下：

```plaintext
### Add task ###

        1. 启动游戏
        2. 每周-阈限禁区
        3. 清体力
        4. 危机行动调令
        5. 事务所（解读仪式）
        6. 市区巡逻
        7. 领取任务奖励
        8. 领取应对协议
        9. 领取邮件
        10. 补给站
        11. 外部招募
        12. 退出游戏
        13. 活动-每日行动补给

Please input multiple [1-13]:
```

首先显示的总菜单，根据需求选择，这里可以同时选多个功能，像：

```plaintext
Please input multiple [1-13]: 1 13 2 3 4 5 6 7 8 10 11 12
```

后面便会显示每个任务的选项供于选择。

下面以单选常规作战为例，选择后显示：

```plaintext
## Input option of "放弃未完成的战斗" for "启动游戏" ##

        1. No
        2. Yes

Please input [1-2]:
```

`## Input option of "放弃未完成的战斗" for "启动游戏" ##` 翻译过来指 `输入"启动游戏"的"放弃未完成的战斗"的选项`，根据需要选择即可。

## 功能菜单

初次启动配置完，或者之前配置过的，便会到当前界面，内容如下：

```plaintext
异象回声小助手
MaaFramework: v4.5.6

Version: v0.0.2-alpha

### Current configuration ###

Controller:

        ADB 默认方式
                D:/Program Files/YXXinYueTongXing-12.0/shell/adb.exe
                127.0.0.1:16384

Resource:

        官服

Tasks:

        - 启动游戏
                - 放弃未完成的战斗: Yes

### Select action ###

        1. Switch controller
        2. Switch resource
        3. Add task
        4. Move task
        5. Delete task
        6. Run tasks
        7. Exit

Please input [1-7]:
```

展示了 Controller（当前控制器，于选择设备设置）、Resource（当前资源）、Tasks（当前待执行任务列表）。  
并给出功能菜单（Select action），依次为：  

1. 更换控制器
2. 更换资源
3. 添加任务
4. 移动任务
5. 删除任务
6. 运行任务
7. 退出

确定 Tasks 部分配置完成便可在输入 6 并回车后运行任务。

## 进阶使用

- 在命令行中添加 `-d` 参数运行即可跳过交互直接运行任务，如 `./MaaPiCli.exe -d`
- 2.0 版本已支持 mumu 后台保活，会在 run task 时获取 mumu 最前台的 tab，并始终使用这个 tab（即使之后被切到后台了）
