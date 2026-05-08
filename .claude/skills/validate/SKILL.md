# Data Validation Skill

校验故宫知识图谱数据的一致性和完整性。

## Trigger
数据修改后、批量导入前、或用户要求校验时激活。

## Validation Rules

### 1. 实体校验
- 所有 entity ID 必须在对应索引文件中存在
- 别名不能指向不存在的实体
- type 必须是: emperor, palace, figure, event, artifact, title
- category 必须符合预定义的分类体系

### 2. 关系校验
- from 和 to 必须都是有效实体
- 关系类型必须是预定义类型之一：父子/夫妻/兄弟/君臣/辅佐/敌对/主持修建/居住于/发生于/同时代/师承/家族
- 时间字段：如果有 year 值，必须为合理年份（1368-1912 明清范围内）
- 循环检测：父子关系不应有循环

### 3. 事件校验
- 事件时间必须在参与者生存时间范围内
- 发生于关系的地点必须是 palace 类型
- 事件必须有至少一个参与者

### 4. 时间线校验
- 皇帝在位时间不能重叠（同一年只能有一个皇帝）
- 年号映射必须覆盖所有使用年号的事件
- 事件时间顺序必须合理

## Usage
```bash
python3 scripts/validate_data.py          # 全量校验
python3 scripts/validate_data.py --quick  # 快速校验（仅结构）
python3 scripts/validate_data.py --fix    # 自动修复可修复的问题
```

## Output
校验报告输出到 stdout，同时写入 `kg/validation_report.json`。
