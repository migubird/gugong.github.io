# Map Data Generation Skill

生成和更新交互式故宫平面图的数据文件。

## Trigger
当新增宫殿、调整宫殿位置、或需要更新地图数据时激活。

## Steps
1. 从 `kg/entities/data/palaces_index.json` 读取所有宫殿数据
2. 为每个宫殿计算或更新位置坐标：
   - 前朝区域：中轴线（x=500），从上到下：太和门、太和殿、中和殿、保和殿
   - 内廷区域：乾清门、乾清宫、交泰殿、坤宁宫
   - 东西六宫：左右对称分布
   - 其他建筑：按实际位置排列
3. 生成 `app/map/map-data.js` 格式：
```javascript
const mapData = {
  palaces: [
    {
      id: "palace-taihe-dian",
      name: "太和殿",
      x: 500, y: 520,
      w: 80, h: 50,
      zone: "前朝",
      info: { built: "1420", function: "大典礼" }
    }
  ],
  zones: [
    { name: "前朝", color: "#c9a227", bounds: {x1, y1, x2, y2} },
    { name: "内廷", color: "#27ae60", bounds: {x1, y1, x2, y2} }
  ]
};
```
4. 运行 `scripts/fix_coords.py` 检测重叠坐标
5. 确保所有宫殿在 `docs/palaces/` 有对应页面

## Coordinate System
- 画布：1000x800
- 中轴线：x=500
- 前朝：y=300-600
- 内廷：y=600-800
- 东西六宫：x=200-400（东）/ x=600-800（西）

## Pitfalls
- 新增宫殿必须检查坐标是否与现有宫殿重叠
- 区域划分必须与实际故宫布局一致
- 坐标更新后必须同步更新 SVG 中的 shape 定义
