# Anki Helper - 英语学习助手

一款面向英语口语学习者的 Anki 辅助工具。支持中英双向查词、口语句型练习、自动发音，通过 Web 可视化界面一键将学习内容添加到 Anki 牌组，配合间隔重复高效记忆。

## 特性

- **中英双向查词** — 输入英文查中文释义，输入中文查对应英文表达
- **口语句型练习** — 输入中文自动翻译为英文，支持手动修正后添加
- **自动发音** — 单词和整句均自动下载美式真人发音，Anki 复习时自动播放
- **牌组管理** — 自由选择已有牌组或新建牌组，支持查看和删除已添加内容
- **Web 界面** — 浏览器操作，无需记命令
- **命令行** — 支持快速添加和批量导入

## 截图

```
┌─────────────────────────────────────────────┐
│  Anki 单词助手                              │
│  [添加单词]  [口语句型]  [单词列表]          │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────┐  ┌────┐   │
│  │ 输入英文或中文...           │  │查词│   │
│  └─────────────────────────────┘  └────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ abandon          /əˈbændən/    🔊   │   │
│  │                                     │   │
│  │ v. 抛弃，遗弃；放弃                 │   │
│  │ The captain gave the order to       │   │
│  │ abandon ship.                       │   │
│  │                                     │   │
│  │ 牌组: [English Vocabulary ▾]        │   │
│  │ 备注: [________________]  [添加]    │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## 前置条件

1. [Python](https://www.python.org/downloads/) 3.8+
2. [Anki](https://apps.ankiweb.net/) 桌面版（2.1+）
3. [AnkiConnect](https://ankiweb.net/shared/info/2055492159) 插件

### 安装 AnkiConnect 插件

打开 Anki → 工具 → 插件 → 获取插件 → 输入代码 `2055492159` → 确定 → 重启 Anki

## 安装

```bash
git clone https://github.com/shao-qi-king/anki-helper.git
cd anki-helper
python -m pip install -r requirements.txt
```

依赖很少，只需要 `requests`、`flask`、`colorama`。

## 使用

### Web 界面（推荐）

```bash
python web.py
```

浏览器打开 http://localhost:5000 ，确保 Anki 在后台运行。

### 三个功能模块

#### 1. 添加单词

输入英文或中文 → 自动查询音标、释义、例句 → 选择牌组 → 一键添加

- 支持英文查中文（如输入 `abandon`）
- 支持中文查英文（如输入 `放弃`）
- 查词后自动播放发音
- 添加到 Anki 时自动下载发音音频

**Anki 卡片效果：**

| 正面 | 背面 |
|------|------|
| 单词 + 音标 + 自动播放发音 | 单词 + 音标 + 发音 + 中文释义 + 例句 |

#### 2. 口语句型

专为口语练习设计。输入你想表达的中文 → 自动翻译成英文 → 可手动修正 → 添加到 Anki。

使用流程：
1. 输入中文（如"这里春天总是晴天"）
2. 点"翻译"，自动生成英文（It is always sunny here in spring）
3. 如果翻译不准确，手动修改英文
4. 可选填语法点（如"It is + adj + 地点 + in + 季节"）
5. 选择牌组，点添加

**Anki 卡片效果：**

| 正面 | 背面 |
|------|------|
| 中文句子 + 语法提示 | 英文整句 + 自动播放发音 + 语法说明 |

复习时：看到中文 → 试着说出英文 → 翻面对答案并听发音。

#### 3. 单词列表

- 按牌组切换查看已添加的内容
- 每个单词显示：单词 + 音标 + 发音按钮
- 点击卡片展开查看释义和例句
- 支持删除

### 命令行

```bash
# 查词并添加到默认牌组
python anki_helper.py add hello

# 附加备注
python anki_helper.py add ephemeral -n "阅读文章时遇到的"

# 只查词不添加
python anki_helper.py search abandon

# 批量导入（文件一行一个单词）
python anki_helper.py batch words.txt
```

## 配置

编辑 `config.py` 可自定义：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `DECK_NAME` | 单词默认牌组 | English Vocabulary |
| `SENTENCE_DECK_NAME` | 句型默认牌组 | English Sentences |
| `MODEL_NAME` | 单词卡片模型名 | English Vocabulary |
| `SENTENCE_MODEL_NAME` | 句型卡片模型名 | English Sentences |
| `CARD_CSS` | 单词卡片样式 | — |
| `SENTENCE_CSS` | 句型卡片样式 | — |

## 项目结构

```
anki-helper/
├── web.py                # Web 服务入口（Flask）
├── anki_helper.py        # 命令行入口
├── youdao.py             # 有道词典 API（中英双向查词）
├── anki_connect.py       # AnkiConnect API 封装（卡片管理、发音下载）
├── config.py             # 配置（牌组名、卡片模板、CSS 样式）
├── requirements.txt      # Python 依赖
├── anki.bat              # Windows 快捷启动脚本
├── static/
│   └── index.html        # Web 前端（单页应用）
└── docs/
    └── english-grammar.md # 英语语法参考手册（从基础到进阶）
```

## 工作原理

```
用户输入 → 有道词典/翻译 API → 查询结果展示
                                      ↓
                               用户确认添加
                                      ↓
                        有道 TTS API → 下载发音 MP3
                                      ↓
                        AnkiConnect → 存储音频 + 创建卡片
                                      ↓
                              Anki 牌组中出现新卡片
```

**发音来源：**
- 单词发音：有道词典 dictvoice 接口（美式发音）
- 整句发音：有道翻译 aidemo TTS 接口（支持任意英文句子）

## 适用场景

- 跟课复习：学完多邻国/其他课程后，把核心句型录入 Anki 巩固
- 主动积累：日常遇到想说但不会的表达，随手录入练习
- 单词积累：阅读/看视频时遇到的生词，一键添加带发音的卡片

## 注意事项

- 使用时需保持 Anki 桌面版运行（AnkiConnect 依赖 Anki 进程）
- 首次添加会自动创建对应的卡片模型和牌组，无需手动配置
- 同一牌组内不会重复添加相同单词/句子，不同牌组间互不影响
- Anki 复习时需开启"自动播放音频"：工具 → 首选项 → 勾选 Automatically play audio
- 发音依赖有道在线 API，需要联网

## 技术栈

- **后端**：Python + Flask
- **前端**：原生 HTML/CSS/JS（无框架依赖）
- **词典 API**：有道词典（免费，无需 API Key）
- **TTS**：有道翻译 aidemo 接口（免费）
- **Anki 通信**：AnkiConnect REST API

## License

MIT
