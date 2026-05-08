# Phase 4: AI Agent 自动化系统

## 架构概览

```
gugong-kb/
├── .claude/skills/          # AI Agent 技能定义
│   ├── extract/             # 实体提取技能
│   ├── enrich/              # 知识丰富技能
│   ├── validate/            # 数据校验技能
│   └── map/                 # 地图数据生成技能
│
├── corpus/                  # 原始史料
│   └── 明史-宫殿志-节选.md
│
├── scripts/
│   ├── extract_entities.py  # 从史料自动提取实体和关系
│   ├── build_registry.py    # 构建 pages.json 页面注册表
│   ├── validate_data.py     # 数据一致性校验
│   ├── compute_knowledge.py # 知识度量（K值）
│   └── generate_entity_pages.py  # 批量生成 Wiki 页面
│
└── kg/
    ├── validation_report.json   # 校验报告
    └── knowledge_report.json    # 知识度量报告
```

## 工作流

### 1. 史料提取
```bash
# 提取单个文件
python3 scripts/extract_entities.py corpus/明史-宫殿志-节选.md

# 提取所有语料
python3 scripts/extract_entities.py --all
```

### 2. 数据校验
```bash
# 全量校验
python3 scripts/validate_data.py

# 快速校验
python3 scripts/validate_data.py --quick

# 自动修复
python3 scripts/validate_data.py --fix
```

### 3. 知识度量
```bash
python3 scripts/compute_knowledge.py
```

### 4. 页面生成
```bash
# 生成所有页面
python3 scripts/generate_entity_pages.py

# 生成特定类型
python3 scripts/generate_entity_pages.py --type emperor

# 预览（不写入）
python3 scripts/generate_entity_pages.py --dry-run
```

### 5. 注册表更新
```bash
python3 scripts/build_registry.py
```

## SKILL 系统

每个 skill 定义了 AI Agent 处理特定任务的规则、步骤和注意事项：

| 技能 | 触发条件 | 功能 |
|------|---------|------|
| extract | 提供历史文本 | 自动提取实体和关系 |
| enrich | 实体信息不完整 | 补充缺失信息 |
| validate | 数据修改后 | 校验一致性 |
| map | 新增宫殿/调整位置 | 更新地图数据 |

## 知识度量

K 值计算公式：
```
K = log2(1 + bytes) × (1 + links_density) × type_weight × quality_norm
```

当前知识总量：**36,570.74 K**
- 实体 K 值：2,273.01
- 页面 K 值：34,297.73
- 页面数：401
- 实体数：319

## 数据质量

| 指标 | 数值 |
|------|------|
| 错误 | 0 |
| 警告 | 4（关系类型） |
| 实体 | 319 |
| 关系 | 1,454 |
| 年号映射 | 26 |
| 别名 | 401 |
