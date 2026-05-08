# Knowledge Enrichment Skill

自动丰富现有实体数据，补充缺失信息。

## Trigger
当发现实体信息不完整或需要扩展时激活。

## Steps
1. 加载 `kg/entities/data/` 下所有实体索引
2. 识别信息缺失的实体：
   - 缺少 aliases
   - 缺少 description
   - 缺少 time_range
   - 缺少 related_entities
3. 为每个缺失实体补充信息：
   - 查询历史文献
   - 交叉验证已有关系数据
   - 补充别称和描述
4. 运行 `scripts/validate_data.py` 校验一致性
5. 运行 `scripts/build_registry.py` 更新 pages.json

## Enrichment Rules
- **皇帝**：庙号、谥号、年号、在位时间、陵墓、主要政绩
- **宫殿**：建造时间、重建记录、功能、位置坐标、相关人物
- **人物**：生卒年、官职变迁、主要事迹、关联宫殿
- **事件**：时间、地点、参与者、前因后果、影响

## Quality Check
- 时间一致性：事件发生时间必须在参与者生存时间内
- 空间一致性：居住关系必须有对应宫殿
- 关系对称性：父子关系应有反向的"被父子"关系
- 别名唯一性：一个别名只能指向一个 canonical entity
