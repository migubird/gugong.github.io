# 故宫知识图谱改造方案

> 基于 shiji-kb (https://github.com/baojie/shiji-kb) 架构深度分析
> 项目地址：https://github.com/migubird/gugong.github.io

---

## 一、shiji-kb 架构分析

### 项目概况

| 指标 | 数值 |
|------|------|
| 文件数 | 55,399 |
| 实体数 | 14,065 |
| Stars | 1,179 |
| 标注次数 | 126,441 |
| 事件数 | 3,198 |
| 关系数 | 7,637 |
| 时间线 | 130 条 |

### 核心架构（5 层）

```
corpus/ (原始文本：史记 130 篇)
  └─> kg/ (知识图谱层)
        └─> wiki/ (展示层)
              └─> app/ (可视化应用)
                    └─> docs/ (静态页面)
```

### 核心创新点

**1. Agentic Ontology（AI 驱动的本体论）**
- 传统方式：专家设计本体 -> 人工标注数据（自上而下，数周一轮）
- Agentic 方式：AI 从文本提取知识 -> 人类校准（自下而上，数小时一轮）
- 核心转变：本体不再是预设蓝图，而是从数据中生长、由人类修剪的有机结构

**2. SKU 知识单元系统**
- 每章拆分为 Facts（事实）和 Skills（技能/模式）
- 存储在 `kg/ontology/` 中
- 每个 SKU 是可独立引用的知识原子

**3. 22 类实体语法高亮**
- 18 类名词：人名/地名/官职/身份/时间/邦国/氏族/名物/族群/器物/天文/神话/生物/数量/典籍/礼仪/刑法/思想
- 4 类动词：军事/刑罚/政治/经济
- 带 Purple Numbers 段落编号，支持精确引用

**4. 史记地铁图**
- 130 条线路 x 3,197 站点的交互式时间线
- 位于 `app/metro/`

**5. 知识度量（K 值）**
- `K = log2(1+bytes) * (1+links_density) * type_weight * quality_norm`

**6. 工作流自动化**
- Claude Code Agent + `.claude/skills/` + `butler` 脚本

### 关键文件结构

```
shiji-kb/
├── kg/                          # 知识图谱核心
│   ├── entities/                # 实体索引
│   │   ├── data/
│   │   │   ├── entity_index.json (8.8MB，14065 实体)
│   │   │   ├── entity_aliases.json (1MB，3489 别名)
│   │   │   ├── person_categories.json
│   │   │   ├── place_categories.json
│   │   │   └── official_categories.json
│   │   └── scripts/
│   │       ├── build_entity_index.py
│   │       ├── classify_persons.py
│   │       ├── classify_places.py
│   │       └── disambiguate_names.py
│   │
│   ├── events/                  # 事件索引
│   │   ├── data/
│   │   │   ├── 001_五帝本纪_事件索引.md
│   │   │   ├── event_relations.json (1.5MB)
│   │   │   └── wars.json (976KB)
│   │   └── scripts/
│   │       └── export_events.py
│   │
│   ├── relations/               # 关系网络
│   │   ├── data/
│   │   │   ├── 01_父子关系.md
│   │   │   ├── 11_政治关系_君臣.md
│   │   │   └── 31_对立关系_敌对.md
│   │   ├── all_relations.json (380KB)
│   │   ├── family_relations.json (3MB)
│   │   └── causal_relations.json (938KB)
│   │
│   ├── chronology/              # 编年数据
│   │   └── data/
│   │       ├── year_ce_map.json (767KB)
│   │       ├── reign_periods.json
│   │       └── person_lifespan_events.json
│   │
│   ├── ontology/ontology-v2/    # SKU 知识单元
│   │   └── chapters/
│   │       └── chapter_001/
│   │           ├── README.md
│   │           ├── eureka.md
│   │           ├── mapping.md
│   │           └── skus/
│   │               ├── facts/fact_001.md
│   │               └── skills/skill_001.md
│   │
│   └── vocabularies/            # 词表
│       ├── 01_人名词表.md
│       ├── 02_地名词表.md
│       └── 03_官职词表.md
│
├── wiki/                        # 展示层
│   ├── scripts/
│   │   ├── build_registry.py    # 构建 pages.json 注册表
│   │   ├── build_wanted_pages.py
│   │   ├── compute_knowledge.py # 计算知识量 K 值
│   │   └── render_html.py
│   └── server/                  # API 服务
│
├── app/                         # 可视化应用
│   ├── metro/                   # 地铁图时间线
│   │   ├── metro.js
│   │   ├── metro.css
│   │   └── data/metro_map_data.json (4.2MB)
│   └── game/                    # 互动游戏
│
├── docs/                        # 静态页面（42,121 文件）
├── corpus/                      # 原始文本（1,005 文件）
├── chapter_md/                  # 标注后的章节（131 文件，.tagged.md）
├── scripts/                     # 工具脚本（333 文件）
└── .claude/skills/              # AI Agent 技能定义
    ├── butler/SKILL.md
    ├── enrich/SKILL.md
    ├── map/SKILL.md
    └── quote/SKILL.md
```

---

## 二、故宫知识图谱仿造方案

### 现状（MVP）

```
gugong-kb/ (已实现)
├── data/
│   ├── palaces.json       # 10 座宫殿
│   ├── emperors.json      # 10 位皇帝
│   ├── figures.json       # 30 位人物
│   ├── events.json        # 15 个事件
│   ├── relations.json     # 80+ 关系
│   └── ontology.json      # 本体定义
├── app/map/               # 交互式 SVG 地图
├── wiki/                  # Markdown + HTML 页面
├── scripts/
│   ├── generate_wiki.py
│   └── fix_coords.py
└── index.html             # 首页
```

### 目标架构（对标 shiji-kb）

```
gugong-kb/
├── corpus/                    # 原始史料
│   ├── 明史-宫殿志.md
│   ├── 明实录-摘录.md
│   └── 清史稿-宫殿志.md
│
├── kg/                        # 知识图谱层（核心扩展）
│   ├── entities/              # 实体索引
│   │   ├── data/
│   │   │   ├── palaces_index.json      # 72 座宫殿全量索引
│   │   │   ├── emperors_index.json     # 明清 24 帝索引
│   │   │   ├── figures_index.json      # 人物索引（200+）
│   │   │   ├── artifacts_index.json    # 文物/藏品索引
│   │   │   ├── halls_index.json        # 殿/宫/门/阁索引
│   │   │   ├── alias_map.json          # 别名映射
│   │   │   ├── person_categories.json  # 人物分类（皇帝/后妃/大臣/太监/工匠）
│   │   │   └── place_categories.json   # 空间分类（前朝/内廷/花园/祭祀）
│   │   └── scripts/
│   │       ├── build_entity_index.py
│   │       └── disambiguate_names.py
│   │
│   ├── events/                # 事件索引
│   │   ├── data/
│   │   │   ├── construction.json       # 建造/重建事件
│   │   │   ├── ceremonies.json         # 典礼/仪式
│   │   │   ├── coups.json             # 政变/兵变
│   │   │   ├── disasters.json         # 火灾/地震
│   │   │   └── events_relations.json  # 事件间因果/时间关系
│   │   └── scripts/
│   │       ├── extract_events.py
│   │       └── validate_dates.py
│   │
│   ├── relations/             # 关系网络
│   │   ├── data/
│   │   │   ├── family.json           # 家族关系（父子/夫妻/兄弟）
│   │   │   ├── political.json        # 政治关系（君臣/辅佐/敌对）
│   │   │   ├── spatial.json          # 空间关系（居住于/办公于/主持修建）
│   │   │   └── temporal.json         # 时间关系（同时代/先后继位）
│   │   ├── all_relations.json        # 汇总
│   │   └── causal_relations.json     # 因果关系
│   │
│   ├── chronology/            # 编年数据
│   │   └── data/
│   │       ├── year_ce_map.json      # 年号 -> 公元纪年
│   │       ├── reign_periods.json    # 在位时间线
│   │       └── palace_timeline.json  # 宫殿建造/修缮时间线
│   │
│   ├── ontology/              # SKU 知识单元（可选）
│   │   └── chapters/
│   │       ├── 永乐朝/
│   │       ├── 康熙朝/
│   │       └── 乾隆朝/
│   │
│   └── vocabularies/          # 词表
│       ├── 01_宫殿词表.md
│       ├── 02_人物词表.md
│       ├── 03_年号词表.md
│       ├── 04_文物词表.md
│       └── 05_建筑术语词表.md
│
├── docs/                      # 静态展示页面
│   ├── palaces/               # 宫殿详情页
│   │   ├── taihe-dian.md      # 太和殿
│   │   ├── qianqing-gong.md   # 乾清宫
│   │   └── ...
│   ├── emperors/              # 皇帝详情页
│   │   ├── zhu-yuanzhang.md   # 朱元璋
│   │   ├── zhu-di.md          # 朱棣
│   │   └── ...
│   ├── figures/               # 人物详情页
│   ├── events/                # 事件详情页
│   ├── pages.json             # 页面注册表（wikilink 跳转用）
│   └── index.html             # 文档首页
│
├── app/                       # 可视化应用
│   ├── map/                   # 交互式宫殿地图（已有，升级）
│   │   ├── index.html
│   │   ├── style.css
│   │   ├── main.js
│   │   └── map-data.js
│   ├── metro/                 # 故宫时间线地铁图（新增）
│   │   ├── index.html
│   │   ├── metro.css
│   │   ├── metro.js
│   │   └── data/
│   │       └── metro_map_data.json
│   └── relations/             # 人物关系图谱（新增）
│       └── index.html
│
├── scripts/                   # 工具脚本
│   ├── generate_wiki.py       # 已有
│   ├── build_registry.py      # 新增：构建 pages.json
│   ├── compute_knowledge.py   # 新增：知识量度量
│   ├── build_entity_index.py  # 新增：实体索引
│   └── generate_entity_pages.py # 新增：批量生成页面
│
├── data/                      # 旧数据层（保留兼容）
│   ├── palaces.json
│   ├── emperors.json
│   ├── figures.json
│   ├── events.json
│   ├── relations.json
│   └── ontology.json
│
└── wiki/                      # 旧 Wiki（保留兼容）
    └── ...
```

---

## 三、实施路线图

### Phase 0：基础设施（1-2 天）

| 任务 | 说明 |
|------|------|
| 创建目录结构 | 按目标架构创建 kg/, docs/, corpus/ 等目录 |
| 迁移旧数据 | 将 data/*.json 映射到 kg/ 新结构 |
| 建立别名系统 | alias_map.json，解决同名人/别名问题 |
| 年号-公元转换 | year_ce_map.json，支持时间线计算 |

### Phase 1：知识图谱深化（3-5 天）

| 任务 | 说明 |
|------|------|
| 宫殿扩展 | 10 -> 72 座，含位置/功能/建造时间/修缮记录 |
| 皇帝扩展 | 10 -> 24 位（明清全量），含在位时间/政绩/关系 |
| 人物扩展 | 30 -> 200+，分类为皇帝/后妃/大臣/太监/工匠/文人 |
| 关系拆分 | 将 relations.json 拆为 family/political/spatial/temporal |
| 事件扩展 | 15 -> 200+，按建造/典礼/政变/火灾分类 |

### Phase 2：语法高亮 Wiki（3-5 天）

| 任务 | 说明 |
|------|------|
| 实体分类体系 | 定义 10-15 类实体（人名/地名/建筑/时间/官职/文物/事件） |
| 带 wikilink 的页面 | 每页用 `[[实体名]]` 语法，支持点击跳转 |
| pages.json 注册表 | 构建 alias_index 支持模糊搜索 |
| 语法高亮 CSS | 每类实体不同颜色，开关控制 |
| 批量生成脚本 | generate_entity_pages.py 从 kg/ 数据自动生成 |

### Phase 3：可视化升级（5-7 天）

| 任务 | 说明 |
|------|------|
| 地图交互升级 | 选皇帝高亮相关宫殿，选年份展示当时状态 |
| 故宫地铁图 | 仿 shiji-kb app/metro/，时间线可视化 |
| 人物关系图 | 力导向图展示皇帝-大臣-后妃网络 |
| 移动端适配 | 确保所有页面移动端可用 |

### Phase 4：AI Agent 自动化（持续）

| 任务 | 说明 |
|------|------|
| SKILL 系统 | `.claude/skills/` 定义提取宫殿/人物/事件技能 |
| 自动提取 pipeline | 输入史料 -> AI 提取实体 -> 建立关系 -> 人工审核 |
| 质量校验 | 日期校验、关系一致性检查、实体消歧 |
| 知识度量 | compute_knowledge.py 追踪知识库增长 |

---

## 四、实体分类体系（建议）

### 名词类（12 类）

| 类型 | 颜色 | 示例 |
|------|------|------|
| 人名 | #3498db | 朱棣、张居正、魏忠贤 |
| 建筑/宫殿 | #27ae60 | 太和殿、乾清宫、午门 |
| 地名 | #e74c3c | 北京、南京、盛京 |
| 时间/年号 | #f39c12 | 永乐十八年、康熙三十四年 |
| 官职 | #9b59b6 | 大学士、太监、工部尚书 |
| 身份 | #1abc9c | 皇帝、皇后、太子、工匠 |
| 文物 | #e67e22 | 金瓯永固杯、清明上河图 |
| 事件 | #c0392b | 靖难之役、崇祯自缢 |
| 建筑术语 | #7f8c8d | 歇山顶、斗拱、琉璃瓦 |
| 典籍 | #2980b9 | 明史、永乐大典 |
| 族群 | #8e44ad | 满族、蒙古族、汉族 |
| 数量 | #95a5a6 | 九千九百九十九间半 |

### 关系类型（12 种）

| 类型 | 说明 | 示例 |
|------|------|------|
| 父子 | 血缘 | 朱元璋 -> 朱棣 |
| 夫妻 | 血缘 | 朱棣 -> 徐皇后 |
| 兄弟 | 血缘 | 朱标 - 朱棣 |
| 君臣 | 政治 | 康熙 - 张廷玉 |
| 辅佐 | 政治 | 张居正 -> 万历 |
| 敌对 | 政治 | 魏忠贤 - 东林党 |
| 主持修建 | 空间 | 朱棣 -> 太和殿 |
| 居住于 | 空间 | 雍正 -> 养心殿 |
| 发生于 | 空间 | 土木堡之变 -> 奉天殿 |
| 同时代 | 时间 | 张居正 - 万历 |
| 师承 | 社会 | 刘基 - 宋濂 |
| 家族 | 血缘 | 杨廷和 - 杨慎 |

---

## 五、技术选型

| 层级 | 技术 | 说明 |
|------|------|------|
| 数据存储 | JSON | 与现有 MVP 一致，无需引入数据库 |
| 页面生成 | Python + 模板 | generate_wiki.py 升级 |
| 前端渲染 | 原生 HTML/CSS/JS | 无框架，GitHub Pages 友好 |
| 地图 | SVG + JS | 已有，继续扩展 |
| 时间线 | Canvas/JS | 参考 shiji-kb app/metro/ |
| 关系图 | D3.js (CDN) | 力导向图 |
| 部署 | GitHub Pages | 已有 |

---

## 六、数据示例

### 别名映射（alias_map.json）

```json
{
  "朱棣": {
    "canonical_id": "emperor-zhudi",
    "aliases": ["明成祖", "永乐帝", "燕王", "太宗"],
    "type": "emperor"
  },
  "太和殿": {
    "canonical_id": "palace-taihe-dian",
    "aliases": ["金銮殿", "奉天殿", "皇极殿"],
    "type": "palace"
  }
}
```

### 宫殿索引（palaces_index.json）

```json
{
  "palace-taihe-dian": {
    "name": "太和殿",
    "aliases": ["金銮殿", "奉天殿"],
    "location": {"x": 500, "y": 520},
    "zone": "前朝",
    "built": "1420",
    "rebuilt": ["1441", "1695"],
    "function": "大典礼",
    "description": "紫禁城核心建筑，皇帝登基、大婚、命将出征之地...",
    "related_emperors": ["emperor-zhudi", "emperor-kangxi"],
    "related_events": ["event-construction-1420", "event-fire-1440"]
  }
}
```

### 关系（relations/spatial.json）

```json
{
  "relations": [
    {
      "from": "emperor-zhudi",
      "to": "palace-taihe-dian",
      "type": "主持修建",
      "year": "1420",
      "source": "明史-宫殿志",
      "note": "永乐十八年建成"
    },
    {
      "from": "emperor-yongzheng",
      "to": "palace-yangxin-dian",
      "type": "居住于",
      "year": "1724",
      "source": "清实录",
      "note": "自雍正起，养心殿成为皇帝寝宫"
    }
  ]
}
```

### 年号-公元映射（chronology/year_ce_map.json）

```json
{
  "永乐": {"start": 1403, "end": 1424, "emperor": "emperor-zhudi"},
  "康熙": {"start": 1662, "end": 1722, "emperor": "emperor-kangxi"},
  "乾隆": {"start": 1736, "end": 1795, "emperor": "emperor-qianlong"}
}
```

---

## 七、与现有 MVP 的衔接

| 现有文件 | 新位置 | 操作 |
|----------|--------|------|
| data/palaces.json | kg/entities/data/palaces_index.json | 扩展字段 + 迁移 |
| data/emperors.json | kg/entities/data/emperors_index.json | 扩展字段 + 迁移 |
| data/figures.json | kg/entities/data/figures_index.json | 扩展字段 + 迁移 |
| data/events.json | kg/events/data/ | 按类型拆分 |
| data/relations.json | kg/relations/ | 按类型拆分 |
| data/ontology.json | kg/ontology/ | 重构为 SKU 格式 |
| app/map/ | app/map/ | 保持不变，升级数据源 |
| scripts/generate_wiki.py | scripts/ | 升级支持 wikilink |
| wiki/ | wiki/ | 保留兼容，逐步迁移到 docs/ |

---

## 八、下一步

建议从 **Phase 0 + Phase 1** 开始：

1. 建立别名系统（alias_map.json）
2. 构建年号-公元映射
3. 扩展宫殿/皇帝/人物数据
4. 拆分关系数据
5. 生成带 wikilink 的详情页

这些改动不大但效果立竿见影，用户可以立即体验到点击跳转、别名搜索等功能。
