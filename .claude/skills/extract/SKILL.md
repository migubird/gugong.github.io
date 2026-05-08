# Entity Extraction Skill

从史料文本中自动提取故宫知识图谱的实体和关系。

## Trigger
当用户提供一段历史文本（明史、清史稿、明实录等）需要提取知识时激活。

## Steps
1. 读取 `corpus/` 下的原始史料文件
2. 按实体类型提取：
   - **人名**：皇帝、后妃、大臣、太监、工匠等
   - **建筑**：宫殿、门、阁、亭、花园等
   - **事件**：建造、典礼、政变、火灾、大婚等
   - **官职**：大学士、尚书、太监等
   - **时间**：年号纪年（永乐十八年等）
3. 建立关系：
   - 父子/夫妻/兄弟（血缘）
   - 君臣/辅佐/敌对（政治）
   - 居住于/办公于/主持修建（空间）
   - 发生于（事件-地点关联）
4. 输出到 `kg/` 对应目录

## Output Format
### 实体格式 (kg/entities/data/)
```json
{
  "entity-id": {
    "name": "实体名称",
    "aliases": ["别名1", "别名2"],
    "type": "emperor|palace|figure|event",
    "category": "子类",
    "description": "描述",
    "time_range": {"start": 1420, "end": 1424},
    "source": "史料来源"
  }
}
```

### 关系格式 (kg/relations/data/)
```json
{
  "relations": [
    {
      "from": "entity-id-1",
      "to": "entity-id-2",
      "type": "关系类型",
      "year": 1420,
      "source": "史料来源",
      "note": "备注"
    }
  ]
}
```

## Pitfalls
- 同名人消歧：明朝和清朝可能有同名人物，用 `era` 字段区分
- 宫殿别名：太和殿=金銮殿=奉天殿=皇极殿，必须建立别名映射
- 年号转换：使用 `kg/chronology/data/year_ce_map.json` 转换为公元纪年
- 事件时间：有些事件时间不精确，用 `year_approx: true` 标记
