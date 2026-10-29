<div align="center">

<img src="docs/logo.png" alt="" width="96">

# Halo Battery

**把你的无线鼠标、键盘、耳机和手柄的电量，直接放进 Windows 托盘。**<br>
每个设备一个图标，不需要任何厂商软件。

[![Latest release](https://img.shields.io/github/v/release/HeyOkay/HaloBattery?label=release&color=2ea043)](../../releases/latest)
[![Downloads](https://img.shields.io/github/downloads/HeyOkay/HaloBattery/total?color=2ea043)](../../releases)
[![Windows 10 / 11](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D4)](#安装)
[![License: MIT](https://img.shields.io/github/license/HeyOkay/HaloBattery?color=lightgrey)](LICENSE)

### [⬇ 下载最新版本](../../releases/latest)

<img src="docs/icons.png" alt="各种图标状态：耳机、鼠标、键盘、手柄和蓝牙设备，从 100% 到 15%，以及充电中和休眠中" width="560">

[English](README.md) | **简体中文**

</div>

## 功能

- **一眼看清。** 每个设备一个圆环，按电量填充；接近提醒阈值时变琥珀色，低于阈值变红色，充电时绿色呼吸。
- **不装厂商软件。** Synapse、G HUB、NGENUITY 这些都可以关掉：Halo Battery 直接和接收器、数据线或 Windows 蓝牙通信。
- **30 多个品牌。** Razer、罗技、赛睿、HyperX、海盗船、华硕 ROG、索尼、Xbox、任天堂、8BitDo、Pulsar、Keychron [以及更多](docs/devices.md)。
- **不打扰你。** 全屏游戏没退出之前不弹提醒，游戏期间也会降低轮询频率。
- **原生外观。** Windows 11 风格菜单，任意缩放比例下都清晰，支持浅色和深色。
- **自动更新。** 新版本在托盘菜单里一键安装。

<p align="center"><img src="docs/charging.gif" alt="充电动画：绿色圆弧缓缓呼吸" width="300"></p>

## 安装

1. 从 **[最新发布](../../releases/latest)** 下载 `HaloBattery-<version>.zip`。
2. 解压到一个独立的文件夹，例如 `C:\Tools`，然后运行 `HaloBattery\HaloBattery.exe`。整个文件夹要放在一起：exe 需要旁边的 `_internal` 目录。
3. 右键托盘图标，选择 **开机启动**。

文件没有代码签名，所以 Windows SmartScreen 可能会提示"无法识别的应用"：点 **更多信息 → 仍要运行**。发布包由 GitHub Actions 直接从本仓库构建，构建日志公开。

右键任意图标可以重命名设备、隐藏它、设置提醒阈值、修改首选项或生成诊断报告。**[全部功能与设置 →](docs/features.md)**（另有便携模式和从源码运行的说明）

## 界面语言

界面跟随 Windows 显示语言：中文 Windows 自动使用中文，其他语言用英文。也可以在 **首选项 → 界面语言** 里手动切换。选择会保存在 `%APPDATA%\HaloBattery\config.json` 的 `"language"` 里（`"auto"` 跟随系统，`"en"` 英文，`"zh-CN"` 简体中文，有对应文件时还支持 `"zh-TW"` 繁体中文）。

翻译就是 [`lang/`](lang/) 目录下的普通 JSON 文件。英文原文是 key，缺条目时自动回退英文，所以加一种语言只需要把 `lang/<code>.json` 放到程序目录（打包版放进 `_internal`）。

> 本 fork 增加了简体中文翻译。自动更新仍然指向上游发布，如果新版本会覆盖中文界面，请到首选项里关掉 **检查更新**。

## 支持的设备

鼠标、键盘、耳机和手柄，走 2.4 GHz 接收器、USB 数据线或蓝牙。
**[查看完整列表 →](docs/devices.md)** 里面标注了连接方式和每个设备是否在真实硬件上测试过。

## 添加你的设备

设备没被识别，或者电量显示不对？发一份诊断报告，大约一分钟：

1. 关掉厂商软件（Synapse、G HUB、网页驱动等），并唤醒设备（动一下鼠标、按一个键）。
2. 右键 Halo Battery 图标，选择 **诊断…**。"未找到设备"的图标上也有这一项。

   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="docs/contributing/diagnostics-menu-dark.png">
     <img src="docs/contributing/diagnostics-menu-light.png" alt="设备托盘菜单，诊断项已标出" width="381">
   </picture>

3. 报告 `diagnostics.txt` 会用记事本打开。[提交 issue](../../issues/new?template=device.yml)，写上设备名称和连接方式（接收器、数据线或蓝牙），把文件拖进评论框。文件在 `%APPDATA%\HaloBattery`。

报告里包含蓝牙 MAC 地址和设备序列号，发布前可以把它们替换成 `xx`。[CONTRIBUTING.md](.github/CONTRIBUTING.md) 说明了报告内容、怎么录制厂商软件的 USB 抓包，以及怎么提交 pull request。

<details>
<summary><b>疑难解答</b></summary>

1. 关掉 Synapse、WLmouse 网页驱动和其他电池工具：它们可能占着接收器。
2. 移动鼠标把它唤醒。
3. 从托盘菜单选择 **诊断…**，按 [添加你的设备](#添加你的设备) 的说明把报告发出来。
4. **提示"python312.dll was not found"**，或者 **开机启动** 说程序是从临时文件夹运行的：说明程序是直接从 ZIP 里启动的，或者只把 `HaloBattery.exe` 单独拷了出来。把整个 ZIP 解压到一个独立文件夹，再从那里运行 `HaloBattery.exe`。

设置、日志和诊断报告都在 `%APPDATA%\HaloBattery`（[便携模式](docs/features.md#portable-mode)下在程序自己的文件夹里）。诊断报告的第一行会写明使用的是哪个文件夹。

</details>

## 致谢

设备协议来自 OpenRazer、HeadsetControl、Solaar、rivalcfg、G-Helper 等开源项目，以及社区提交的抓包和测试运行记录。**[完整致谢 →](docs/credits.md)**

MIT 许可证，见 [LICENSE](LICENSE)。
