# 数据来源说明 (Data Sources)

> 故宫知识图谱所有数据条目的信息来源标注。每个实体通过 `sources` 字段记录其数据来源。

## 来源类型

| 类型 | 说明 | 可信度 |
|------|------|--------|
| `official` | 故宫博物院官网 (dpm.org.cn) | ⭐⭐⭐⭐⭐ 最高 |
| `book` | 正史（《明史》《清史稿》等） | ⭐⭐⭐⭐⭐ 最高 |
| `wikipedia` | 维基百科中文 (zh.wikipedia.org) | ⭐⭐⭐⭐ 高 |
| `academic` | 学术论文（故宫博物院院刊等） | ⭐⭐⭐⭐ 高 |
| `ai_generated` | AI 辅助生成，需人工核实 | ⭐⭐ 待核实 |

## 主要数据来源

### 1. 故宫博物院官网 (dpm.org.cn)
- **网址**: https://www.dpm.org.cn/
- **覆盖范围**: 建筑概述、宫廷历史、文物保护
- **关键页面**:
  - `/explore/buildings.html` — 故宫建筑概述（外朝/内廷/三大殿/后三宫）
  - `/explore/ancients.html` — 宫廷历史
  - `/explore/cultures.html` — 文化专题
  - `/explore/protects.html` — 故宫文物医院
  - `/about/about_chron.html` — 院史编年
- **数字资源**:
  - 数字文物库: https://digicol.dpm.org.cn/
  - 全景故宫: https://pano.dpm.org.cn/
  - 在线订票: https://ticket.dpm.org.cn/

### 2. 正史文献
- **《明史》** — 张廷玉等撰，清朝官修，记载明代皇帝、大臣、事件
- **《清史稿》** — 赵尔巽等撰，记载清代皇帝、大臣、事件
- **覆盖字段**: 皇帝年号、在位时间、人物生平、事件记录、关系（君臣/父子等）

### 3. 维基百科中文
- **网址**: https://zh.wikipedia.org/
- **覆盖范围**: 宫殿建筑、历史人物、历史事件的百科条目
- **覆盖字段**: 建筑尺寸、别名、人物描述、事件详情

### 4. 学术论文
- **故宫博物院院刊** — https://www.dpm.org.cn/Research.html
- 涵盖建筑研究、文物修复、宫廷历史等领域

## 数据标注格式

每个数据实体包含 `sources` 字段，示例：

```json
{
  "id": "taihe-dian",
  "name": "太和殿",
  "description": "...",
  "sources": [
    {
      "type": "official",
      "name": "故宫博物院官网",
      "url": "https://www.dpm.org.cn/explore/buildings.html",
      "note": "官方建筑概述",
      "fields": ["description"]
    },
    {
      "type": "wikipedia",
      "name": "维基百科 - 太和殿",
      "url": "https://zh.wikipedia.org/wiki/太和殿",
      "note": "百科参考",
      "fields": ["dimensions", "description", "aliases"]
    }
  ]
}
```

### fields 字段说明
`fields` 数组标明该来源具体提供了哪些字段的信息，便于追溯和验证。

## 数据统计

| 数据集 | 条目数 | 来源标注率 |
|--------|--------|-----------|
| data/palaces.json | 72 | 100% |
| data/emperors.json | 26 | 100% |
| data/figures.json | 221 | 100% |
| data/events.json | 82 | 100% |
| kg/entities/ | 319 | 100% |
| kg/events/ | 286 | 100% |
| kg/relations/ | 727 | 100% |
| kg/chronology/ | 52 | 100% |
| **总计** | **1,556+** | **100%** |

## 官网已抓取的权威信息

### 故宫建筑概述（来源: dpm.org.cn/explore/buildings.html）

> 紫禁城南北长961米，东西宽753米，四面围有高10米的城墙，城外有宽52米的护城河，真可谓有金城汤池之固。紫禁城有四座城门，南面为午门，北面为神武门，东面为东华门，西面为西华门。城墙的四角，各有一座风姿绰约的角楼，民间有九梁十八柱七十二条脊之说，形容其结构的复杂。

> 紫禁城内的建筑分为外朝和内廷两部分。外朝的中心为太和殿、中和殿、保和殿，统称三大殿，是国家举行大典礼的地方。三大殿左右两翼辅以文华殿、武英殿两组建筑。内廷的中心是乾清宫、交泰殿、坤宁宫，统称后三宫，是皇帝和皇后居住的正宫。其后为御花园。后三宫两侧排列着东、西六宫，是后妃们居住休息的地方。

## 待补充来源

- [ ] 百度百科（补充宫殿和人物详细信息）
- [ ] 故宫博物院出版的图书
- [ ] 中国第一历史档案馆资料
- [ ] 更多学术论文（院刊文章全文）

## 更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-05-10 | 首次建立来源标注体系，为所有 1,556+ 条实体添加 sources 字段 |
