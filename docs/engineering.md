# 故宫知识图谱项目工程文档

> 项目地址：https://github.com/migubird/gugong.github.io
> 在线访问：https://migubird.github.io/gugong.github.io/
> 参考项目：https://github.com/baojie/shiji-kb

---

## 一、项目概述

故宫知识图谱是一个以空间为核心维度的历史文化知识图谱项目。与 shiji-kb 以文本（史记）为核心不同，本项目的核心节点是 **宫殿**，围绕宫殿关联皇帝、人物、事件、时间等维度。

**核心设计理念**：从"谁在什么时间做了什么"变为"什么空间里发生了什么，涉及谁，在什么时间"。

---

## 二、目录结构

```
gugong/
├── README.md                  # 项目说明
├── index.html                 # 首页入口
├── .gitignore
│
├── docs/                      # 项目文档
│   ├── roadmap.md             # 改造方案文档（本文档的兄弟文档）
│   └── engineering.md         # 本文件
│
├── data/                      # 数据层（MVP 阶段，向后兼容）
│   ├── palaces.json           # 宫殿数据（10 座）
│   ├── emperors.json          # 皇帝数据（10 位）
│   ├── figures.json           # 人物数据（30 位）
│   ├── events.json            # 事件数据（15 个）
│   ├── relations.json         # 关系数据（80+ 条）
│   ├── ontology.json          # 本体定义
│   └── index.html             # 数据目录页
│
├── kg/                        # 知识图谱层（扩展中）
│   └── ontology/
│       └── ontology.json      # 图谱本体定义
│
├── app/                       # 前端应用
│   └── map/                   # 交互式宫殿地图
│       ├── index.html         # 地图页面
│       ├── style.css          # 样式
│       ├── main.js            # 交互逻辑
│       └── map-data.js        # 地图数据（JS 格式）
│
├── wiki/                      # Wiki 页面
│   ├── index.html             # Wiki 首页
│   ├── index.md               # Wiki 索引
│   ├── palaces/               # 宫殿页面
│   │   ├── taihe-dian.html    # 太和殿
│   │   ├── taihe-dian.md
│   │   └── ...
│   └── emperors/              # 皇帝页面
│       ├── zhu-yuanzhang.html # 朱元璋
│       ├── zhu-yuanzhang.md
│       └── ...
│
├── scripts/                   # 工具脚本
│   ├── generate_wiki.py       # 生成 Wiki 页面
│   └── fix_coords.py          # 坐标修正工具
│
└── resources/                 # 资源文件（图片等）
```

---

## 三、数据模型

### 3.1 宫殿（Palace）

```json
{
  "id": "taihe-dian",
  "name": "太和殿",
  "aliases": ["金銮殿", "奉天殿", "皇极殿"],
  "zone": "前朝",
  "built_year": 1420,
  "rebuilt_years": [1441, 1695],
  "description": "紫禁城核心建筑...",
  "coordinates": {"x": 500, "y": 520},
  "image": "resources/taihe-dian.jpg"
}
```

**字段说明**：
- `id`: 唯一标识符（小写英文，连字符连接）
- `aliases`: 历史名称/别称数组
- `zone`: 所属区域（前朝/内廷/花园/祭祀/防御）
- `built_year`: 始建年份（公元纪年）
- `rebuilt_years`: 重建/修缮年份数组
- `coordinates`: SVG 地图中的坐标

### 3.2 皇帝（Emperor）

```json
{
  "id": "emperor-zhudi",
  "name": "朱棣",
  "title": "明成祖",
  "era_name": "永乐",
  "reign_start": 1402,
  "reign_end": 1424,
  "dynasty": "明",
  "birth_year": 1360,
  "death_year": 1424,
  "description": "明朝第三位皇帝...",
  "portrait": "resources/zhudi.jpg"
}
```

### 3.3 人物（Figure）

```json
{
  "id": "figure-zhangjuyu",
  "name": "张居正",
  "aliases": ["张江陵", "太岳"],
  "role": "大臣",
  "category": "内阁首辅",
  "dynasty": "明",
  "birth_year": 1525,
  "death_year": 1582,
  "description": "明代著名政治家..."
}
```

**人物分类**：
- 皇帝
- 后妃
- 大臣
- 太监
- 工匠
- 文人
- 武将

### 3.4 事件（Event）

```json
{
  "id": "event-construction-1420",
  "name": "紫禁城建成",
  "type": "建造",
  "year": 1420,
  "description": "永乐十八年，紫禁城基本建成...",
  "related_palaces": ["taihe-dian", "zhonghe-dian", "baohe-dian"],
  "related_figures": ["emperor-zhudi"]
}
```

**事件类型**：
- 建造
- 重建
- 火灾
- 地震
- 典礼
- 政变
- 迁都

### 3.5 关系（Relation）

```json
{
  "from": "emperor-zhudi",
  "to": "palace-taihe-dian",
  "type": "主持修建",
  "year": "1420",
  "note": "永乐十八年建成"
}
```

**关系类型**：
- 父子（血缘）
- 夫妻（血缘）
- 兄弟（血缘）
- 君臣（政治）
- 辅佐（政治）
- 敌对（政治）
- 主持修建（空间）
- 居住于（空间）
- 发生于（空间）
- 同时代（时间）
- 师承（社会）
- 家族（血缘）

### 3.6 本体（Ontology）

```json
{
  "entity_types": {
    "palace": {"label": "宫殿", "color": "#27ae60"},
    "emperor": {"label": "皇帝", "color": "#f39c12"},
    "figure": {"label": "人物", "color": "#3498db"},
    "event": {"label": "事件", "color": "#c0392b"}
  },
  "relation_types": {
    "主持修建": {"domain": "emperor", "range": "palace"},
    "居住于": {"domain": "figure", "range": "palace"},
    "父子": {"domain": "figure", "range": "figure"},
    "发生于": {"domain": "event", "range": "palace"}
  }
}
```

---

## 四、前端架构

### 4.1 交互式地图（app/map/）

**数据流**：
```
data/*.json -> scripts/generate_wiki.py -> app/map/map-data.js -> SVG 渲染
```

**交互功能**：
- 鼠标悬停宫殿 -> 显示信息卡片
- 点击宫殿 -> 跳转到 Wiki 详情页
- 选择皇帝 -> 高亮相关宫殿
- 选择年份 -> 筛选该时间存在的宫殿

**坐标系统**：
- SVG viewBox: `0 0 1000 800`
- Y 轴翻转：`newY = 800 - oldY`（确保南在下，北在上）
- 午门（Wu Men）在底部（y=730）

### 4.2 Wiki 页面生成

**脚本**：`scripts/generate_wiki.py`

**功能**：
1. 读取 `data/*.json` 数据
2. 为每个实体生成 Markdown 页面
3. 同时生成 HTML 版本（用于 GitHub Pages）
4. 生成索引页面

**模板格式**：
```html
<!DOCTYPE html>
<html>
<head><title>{{title}}</title></head>
<body>
<h1>{{title}}</h1>
{{body}}
<a href="../">返回索引</a>
</body>
</html>
```

---

## 五、部署与发布

### 5.1 GitHub Pages

- 仓库：https://github.com/migubird/gugong.github.io
- 访问地址：https://migubird.github.io/gugong.github.io/
- 分支：main
- 类型：静态站点（无构建步骤）

### 5.2 推送方式

由于网络环境限制，git push 到 github.com:443 经常超时。备选方案：

**方案 A：GitHub REST API 推送**
```python
# 通过 API 创建 blob -> tree -> commit -> 更新 ref
import requests
headers = {"Authorization": "token GITHUB_TOKEN"}
# 1. POST /repos/{owner}/{repo}/git/blobs
# 2. POST /repos/{owner}/{repo}/git/trees
# 3. POST /repos/{owner}/{repo}/git/commits
# 4. PATCH /repos/{owner}/{repo}/git/refs/heads/main
```

**方案 B：直接在 GitHub 网页编辑**
- 适合小改动
- 自动触发 Pages 构建

### 5.3 触发 Pages 构建

```bash
# 推送空 commit 触发重建
git commit --allow-empty -m "trigger pages build" && git push
```

---

## 六、已知问题与环境限制

### 6.1 浏览器限制

- Playwright/Chromium 不可用（缺少 libatk-1.0.so.0）
- 所有页面测试需通过终端 API 或手动验证

### 6.2 网络限制

- Google/DuckDuckGo 不可达
- GitHub API (api.github.com) 可用
- Git push 到 github.com:443 不稳定

### 6.3 认证

- GitHub PAT 已配置（存储在 git remote URL 中）
- 注意：PAT 不应在代码中硬编码，应使用环境变量

---

## 七、开发规范

### 7.1 文件命名

- ID 格式：小写英文，连字符连接（如 `taihe-dian`, `emperor-zhudi`）
- 中文名称用 `name` 字段存储
- JSON 文件用 UTF-8 编码

### 7.2 数据校验

每次修改数据后应运行：
```bash
# 检查 JSON 格式
python3 -c "import json; json.load(open('data/palaces.json'))"

# 重新生成 Wiki
python3 scripts/generate_wiki.py

# 检查关系一致性
python3 -c "
import json
relations = json.load(open('data/relations.json'))
for r in relations:
    assert 'from' in r and 'to' in r and 'type' in r
print('All relations valid')
"
```

### 7.3 编码规范

- Python 脚本使用 Python 3
- 避免 f-string 中使用反斜杠（某些 Python 版本不支持）
- 模板使用 `.replace()` 占位符而非 f-string

---

## 八、扩展计划

### 8.1 短期（Phase 0-1）

- [ ] 建立别名系统（alias_map.json）
- [ ] 构建年号-公元映射
- [ ] 扩展宫殿数据（10 -> 72）
- [ ] 扩展人物数据（30 -> 200+）
- [ ] 拆分关系数据

### 8.2 中期（Phase 2-3）

- [ ] 语法高亮 Wiki 页面
- [ ] pages.json 注册表
- [ ] 时间线地铁图
- [ ] 人物关系图谱
- [ ] 移动端适配优化

### 8.3 长期（Phase 4）

- [ ] AI Agent 知识提取
- [ ] SKILL 系统
- [ ] 知识度量系统
- [ ] 质量自动校验

---

## 九、参考资料

- shiji-kb: https://github.com/baojie/shiji-kb
- 故宫博物院官网: https://www.dpm.org.cn
- 明史（二十四史之一）
- 清史稿
- 明实录
- 国朝宫史（清代）

---

*最后更新：2026-05-05*
