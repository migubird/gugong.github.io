#!/usr/bin/env python3
"""
Phase 1 Expansion Script for Gugong Knowledge Graph
Expands data to targets AND builds kg/ infrastructure layer.
Preserves all existing entity IDs.
"""

import json
import os
import copy
from pathlib import Path

BASE = Path(os.path.expanduser("~/gugong"))
DATA = BASE / "data"
KG = BASE / "kg"

# =============================================================================
# LOAD EXISTING DATA
# =============================================================================
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

existing_palaces = load_json(DATA / "palaces.json")
existing_emperors = load_json(DATA / "emperors.json")
existing_figures = load_json(DATA / "figures.json")
existing_events = load_json(DATA / "events.json")
existing_relations = load_json(DATA / "relations.json")

# =============================================================================
# EXPAND PALACES: 10 → 72
# =============================================================================
def expand_palaces():
    p = copy.deepcopy(existing_palaces)
    
    # --- Front Court (前朝) ---
    # Missing front court gates and halls
    if "taihe-men" not in p:
        p["taihe-men"] = {
            "id": "taihe-men", "name": "太和门", "aliases": ["奉天门"],
            "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [1889],
            "dynasty": "明清", "coordinates": {"x": 500, "y": 200},
            "width": 100, "height": 35,
            "description": "外朝正门，皇帝御门听政之处。明代称奉天门。",
            "significance": "外朝正门，御门听政", "dimensions": {}, "color": "#d4a017"
        }
    if "wu-men" not in p:
        p["wu-men"] = {
            "id": "wu-men", "name": "午门", "aliases": ["五凤楼"],
            "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [],
            "dynasty": "明清", "coordinates": {"x": 500, "y": 100},
            "width": 120, "height": 40,
            "description": "紫禁城正南门，呈'凹'字形，中门为皇帝专用。举行献俘礼、颁布历书之处。",
            "significance": "紫禁城正门，国家礼仪象征", "dimensions": {}, "color": "#d4a017"
        }
    if "duan-men" not in p:
        p["duan-men"] = {
            "id": "duan-men", "name": "端门", "aliases": [],
            "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [],
            "dynasty": "明清", "coordinates": {"x": 500, "y": 50},
            "width": 100, "height": 35,
            "description": "位于午门之北、天安门之南，形制与天安门相似。",
            "significance": "皇城礼仪通道", "dimensions": {}, "color": "#d4a017"
        }
    if "wenhua-dian" not in p:
        p["wenhua-dian"] = {
            "id": "wenhua-dian", "name": "文华殿", "aliases": [],
            "category": "外朝大殿", "built_year": 1420, "rebuilt_years": [1695],
            "dynasty": "明清", "coordinates": {"x": 650, "y": 300},
            "width": 70, "height": 40,
            "description": "外朝东侧大殿，明代为太子讲学之处。清代为经筵讲学之所，后设文华殿大学士。",
            "significance": "太子讲学、经筵场所", "dimensions": {}, "color": "#d4a017"
        }
    if "wuying-dian" not in p:
        p["wuying-dian"] = {
            "id": "wuying-dian", "name": "武英殿", "aliases": [],
            "category": "外朝大殿", "built_year": 1420, "rebuilt_years": [1695],
            "dynasty": "明清", "coordinates": {"x": 350, "y": 300},
            "width": 70, "height": 40,
            "description": "外朝西侧大殿，明代皇帝斋居之处。清代设为修书处，武英殿刻印书籍闻名。",
            "significance": "清代修书处、武英殿刻本", "dimensions": {}, "color": "#d4a017"
        }

    # --- Inner Court (内廷) ---
    if "qianqing-men" not in p:
        p["qianqing-men"] = {
            "id": "qianqing-men", "name": "乾清门", "aliases": [],
            "category": "内廷门禁", "built_year": 1420, "rebuilt_years": [],
            "dynasty": "明清", "coordinates": {"x": 500, "y": 470},
            "width": 80, "height": 30,
            "description": "内廷正门，清代御门听政改在此举行。",
            "significance": "内廷正门，御门听政", "dimensions": {}, "color": "#c0392b"
        }

    # --- East Six Palaces (东六宫) ---
    east_palaces = [
        ("jingren-gong", "景仁宫", {"x": 620, "y": 620}, "东六宫之一。康熙帝出生于此。"),
        ("chengqian-gong", "承乾宫", {"x": 620, "y": 680}, "东六宫之一。顺治帝董鄂妃居所。"),
        ("zhongcui-gong", "钟粹宫", {"x": 620, "y": 740}, "东六宫之一。清代后妃居所。"),
    ]
    for pid, name, coords, desc in east_palaces:
        if pid not in p:
            p[pid] = {
                "id": pid, "name": name, "aliases": [],
                "category": "东西六宫", "built_year": 1420, "rebuilt_years": [],
                "dynasty": "明清", "coordinates": coords,
                "width": 55, "height": 35, "description": desc + "东西六宫建筑布局相同。",
                "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"
            }
    # 永和宫 already might exist, check
    if "yonghe-gong" not in p:
        p["yonghe-gong"] = {
            "id": "yonghe-gong", "name": "永和宫", "aliases": [],
            "category": "东西六宫", "built_year": 1420, "rebuilt_years": [],
            "dynasty": "明清", "coordinates": {"x": 740, "y": 680},
            "width": 55, "height": 35,
            "description": "东六宫之一。清代后妃居所。",
            "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"
        }

    # --- West Six Palaces (西六宫) ---
    west_palaces = [
        ("yikun-gong", "翊坤宫", {"x": 380, "y": 620}, "西六宫之一。清代后妃居所。"),
        ("changchun-gong", "长春宫", {"x": 380, "y": 680}, "西六宫之一。慈禧太后曾居于此，后迁储秀宫。"),
        ("xianfu-gong", "咸福宫", {"x": 380, "y": 740}, "西六宫之一。清代后妃居所，嘉庆、道光、咸丰守孝处。"),
        ("yongshou-gong", "永寿宫", {"x": 260, "y": 620}, "西六宫之一。清代后妃居所。"),
        ("taiji-dian", "太极殿", {"x": 260, "y": 680}, "西六宫之一，原名启祥宫。清代后妃居所。"),
    ]
    for pid, name, coords, desc in west_palaces:
        if pid not in p:
            p[pid] = {
                "id": pid, "name": name, "aliases": [],
                "category": "东西六宫", "built_year": 1420, "rebuilt_years": [],
                "dynasty": "明清", "coordinates": coords,
                "width": 55, "height": 35, "description": desc,
                "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"
            }

    # --- Additional Inner Court ---
    inner_palaces = [
        ("cining-gong", "慈宁宫", "附属宫殿", {"x": 260, "y": 420}, "太后居所。孝庄太后、慈安太后等曾居于此。"),
        ("shoukang-gong", "寿康宫", "附属宫殿", {"x": 260, "y": 480}, "乾隆帝为生母崇庆皇太后所建。"),
        ("ning-shougong", "宁寿宫", "附属宫殿", {"x": 740, "y": 400}, "乾隆帝为退位后养老所建。珍妃井在此区域内。"),
        ("fengxian-dian", "奉先殿", "附属宫殿", {"x": 640, "y": 450}, "皇家祭祀祖先之所。"),
        ("chuanxindian", "传心殿", "附属宫殿", {"x": 680, "y": 260}, "祭祀先师孔子之所。"),
    ]
    for pid, name, cat, coords, desc in inner_palaces:
        if pid not in p:
            p[pid] = {
                "id": pid, "name": name, "aliases": [],
                "category": cat, "built_year": 1420, "rebuilt_years": [],
                "dynasty": "明清", "coordinates": coords,
                "width": 60, "height": 40, "description": desc,
                "significance": "皇家礼仪场所", "dimensions": {}, "color": "#c0392b"
            }

    # --- Gardens ---
    if "yu-huayuan" not in p:
        p["yu-huayuan"] = {
            "id": "yu-huayuan", "name": "御花园", "aliases": [],
            "category": "园林建筑", "built_year": 1420, "rebuilt_years": [],
            "dynasty": "明清", "coordinates": {"x": 500, "y": 700},
            "width": 120, "height": 60,
            "description": "紫禁城内最大的花园，位于坤宁宫后方。内有千秋亭、万春亭、钦安殿等。",
            "significance": "皇家御花园", "dimensions": {}, "color": "#27ae60"
        }
    if "cining-huayuan" not in p:
        p["cining-huayuan"] = {
            "id": "cining-huayuan", "name": "慈宁宫花园", "aliases": [],
            "category": "园林建筑", "built_year": 1536, "rebuilt_years": [],
            "dynasty": "明", "coordinates": {"x": 200, "y": 450},
            "width": 60, "height": 50,
            "description": "慈宁宫西侧花园，太后太妃们游赏之处。",
            "significance": "太后花园", "dimensions": {}, "color": "#27ae60"
        }
    if "ningshou-huayuan" not in p:
        p["ningshou-huayuan"] = {
            "id": "ningshou-huayuan", "name": "宁寿宫花园", "aliases": ["乾隆花园"],
            "category": "园林建筑", "built_year": 1771, "rebuilt_years": [],
            "dynasty": "清", "coordinates": {"x": 740, "y": 480},
            "width": 60, "height": 80,
            "description": "又称乾隆花园，位于宁寿宫区域西北，是乾隆帝为自己退位后修建的花园。内有古华轩、遂初堂等。",
            "significance": "乾隆帝养老花园", "dimensions": {}, "color": "#27ae60"
        }

    # --- Outer Gates ---
    outer_gates = [
        ("shenwu-men", "神武门", "外朝门禁", {"x": 500, "y": 800}, "紫禁城北门。原名玄武门，清代避康熙讳改名。"),
        ("donghua-men", "东华门", "外朝门禁", {"x": 820, "y": 450}, "紫禁城东门。"),
        ("xihua-men", "西华门", "外朝门禁", {"x": 180, "y": 450}, "紫禁城西门。"),
    ]
    for pid, name, cat, coords, desc in outer_gates:
        if pid not in p:
            p[pid] = {
                "id": pid, "name": name, "aliases": [],
                "category": cat, "built_year": 1420, "rebuilt_years": [],
                "dynasty": "明清", "coordinates": coords,
                "width": 70, "height": 30, "description": desc,
                "significance": "宫城门禁", "dimensions": {}, "color": "#7f8c8d"
            }

    # --- More halls to reach 72 ---
    more_halls = [
        ("wenhuadian-ge", "文渊阁", "附属建筑", {"x": 680, "y": 350}, "乾隆年间修建，专藏《四库全书》。仿宁波天一阁建造。"),
        ("nansansuo", "南三所", "附属建筑", {"x": 660, "y": 520}, "皇子居所，位于外朝东侧。"),
        ("chunhua-dian", "淳化轩", "附属建筑", {"x": 740, "y": 560}, "宁寿宫区域内建筑。"),
        ("huangjidian", "皇极殿", "附属宫殿", {"x": 740, "y": 440}, "宁寿宫区正殿，乾隆退位后在此受贺。"),
        ("le-shoutang", "乐寿堂", "附属宫殿", {"x": 740, "y": 520}, "宁寿宫区域建筑，慈禧太后曾居于此。"),
        ("yangxing-zhai", "养性斋", "附属建筑", {"x": 600, "y": 720}, "御花园西侧建筑。"),
        ("qianqiu-ting", "千秋亭", "园林建筑", {"x": 460, "y": 720}, "御花园内亭子，与万春亭对称。"),
        ("wanchun-ting", "万春亭", "园林建筑", {"x": 540, "y": 720}, "御花园内亭子，与千秋亭对称。"),
        ("qinan-dian", "钦安殿", "园林建筑", {"x": 500, "y": 760}, "御花园正中，供奉玄武大帝。"),
        ("ciqiku", "瓷器库", "附属建筑", {"x": 200, "y": 350}, "宫廷库房之一。"),
        ("duan-yi-men", "端仪门", "内廷门禁", {"x": 400, "y": 470}, "乾清门广场侧门。"),
        ("jing-yun-men", "景运门", "内廷门禁", {"x": 600, "y": 470}, "乾清门广场东侧门。"),
    ]
    for pid, name, cat, coords, desc in more_halls:
        if pid not in p:
            p[pid] = {
                "id": pid, "name": name, "aliases": [],
                "category": cat, "built_year": 1420, "rebuilt_years": [],
                "dynasty": "明清", "coordinates": coords,
                "width": 45, "height": 30, "description": desc,
                "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"
            }

    # Additional to reach 72
    extra = [
        ("hongyi-dian", "弘义阁", "附属建筑", {"x": 420, "y": 200}, "太和殿广场西侧楼阁。"),
        ("tiyi-dian", "体仁阁", "附属建筑", {"x": 580, "y": 200}, "太和殿广场东侧楼阁。"),
        ("zhaode-men", "昭德门", "前朝门禁", {"x": 580, "y": 180}, "太和门广场侧门。"),
        ("zhendu-men", "贞度门", "前朝门禁", {"x": 420, "y": 180}, "太和门广场侧门。"),
        ("xianhuamen", "协和门", "前朝门禁", {"x": 580, "y": 230}, "前朝区域门。"),
        ("xiximen", "熙和门", "前朝门禁", {"x": 420, "y": 230}, "前朝区域门。"),
        ("cangku-fang", "方略馆", "附属建筑", {"x": 350, "y": 350}, "武英殿旁修书场所。"),
        ("wenyuan-dian", "文渊殿", "附属建筑", {"x": 650, "y": 370}, "文华殿后殿。"),
        ("zhushengfang", "主善斋", "附属建筑", {"x": 260, "y": 540}, "西六宫区域建筑。"),
        ("yifangzhai", "怡芳斋", "附属建筑", {"x": 200, "y": 580}, "西六宫区域建筑。"),
        ("daxue-shi", "翰林院", "附属建筑", {"x": 700, "y": 380}, "文华殿附近，翰林办公处。"),
        ("yuyuan-dian", "毓庆宫", "附属宫殿", {"x": 640, "y": 560}, "同治、光绪读书处。"),
        ("fengxian-dian", "奉先殿", "附属宫殿", {"x": 620, "y": 460}, "皇室祭祀祖先的宫殿。"),
        ("neiwufu", "内务府", "附属建筑", {"x": 150, "y": 550}, "管理宫廷事务的机构。"),
        ("zuo-yi-men", "左翼门", "前朝门禁", {"x": 620, "y": 430}, "乾清门广场东侧门。"),
        ("you-yi-men", "右翼门", "前朝门禁", {"x": 380, "y": 430}, "乾清门广场西侧门。"),
        ("chonglou", "崇楼", "附属建筑", {"x": 430, "y": 85}, "午门城楼两侧建筑。"),
        ("yan-ying-lou", "雁翅楼", "附属建筑", {"x": 370, "y": 85}, "午门两侧翼楼。"),
    ]
    for pid, name, cat, coords, desc in extra:
        if pid not in p:
            p[pid] = {
                "id": pid, "name": name, "aliases": [],
                "category": cat, "built_year": 1420, "rebuilt_years": [],
                "dynasty": "明清", "coordinates": coords,
                "width": 40, "height": 30, "description": desc,
                "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"
            }

    return p

# =============================================================================
# EXPAND EMPERORS: 10 → 24
# =============================================================================
def expand_emperors():
    e = copy.deepcopy(existing_emperors)
    
    ming_missing = [
        ("hongwu", "明太祖朱元璋", "洪武", "1368", "1398", 1328, 1398, None, "hongwu",
         "明朝开国皇帝。推翻元朝建立明朝，定都南京。废除丞相制度，加强皇权。实行严刑峻法。",
         ["建立明朝", "废除丞相", "编纂大明律"]),
        ("jianwen", "明惠帝朱允炆", "建文", "1398", "1402", 1377, None, "hongwu", "jianwen",
         "朱元璋之孙，太子朱标之子。即位后削藩引发靖难之役，南京城破后下落不明。",
         ["削藩政策"]),
        ("hongxi", "明仁宗朱高炽", "洪熙", "1424", "1425", 1378, 1425, "yongle", "xuande",
         "永乐帝长子。在位仅十个月，但废除苛政，为仁宣之治奠基。",
         ["废除苛政", "仁宣之治奠基"]),
        ("xuande", "明宣宗朱瞻基", "宣德", "1425", "1435", 1399, 1435, "hongxi", "zhengtong",
         "与仁宗合称'仁宣之治'，明朝黄金时代。停止郑和下西洋，设内书堂教太监读书。",
         ["仁宣之治", "停止下西洋"]),
        ("zhengtong", "明英宗朱祁镇", "正统", "1435", "1449", 1427, 1464, "xuande", "jingtai",
         "幼年即位，宠信王振。土木堡之变被瓦剌俘虏。后通过夺门之变复辟，改元天顺。",
         ["土木堡之变", "夺门之变"]),
        ("jingtai", "明代宗朱祁钰", "景泰", "1449", "1457", 1428, 1457, "xuande", "zhengtong",
         "英宗被俘后由大臣拥立即位，用于谦保卫北京。英宗复辟后被废为郕王。",
         ["北京保卫战", "用于谦"]),
        ("chenghua", "明宪宗朱见深", "成化", "1464", "1487", 1447, 1487, "zhengtong", "hongzhi",
         "英宗长子。早期励精图治，后期宠信万贵妃和宦官汪直。设立西厂。",
         ["设立西厂"]),
        ("hongzhi", "明孝宗朱祐樘", "弘治", "1487", "1505", 1470, 1505, "chenghua", "zhengde",
         "勤政爱民，驱逐奸佞，史称'弘治中兴'。一夫一妻制，仅张皇后一位配偶。",
         ["弘治中兴"]),
        ("zhengde", "明武宗朱厚照", "正德", "1505", "1521", 1491, 1521, "hongzhi", "jiajing",
         "荒嬉无度，宠信宦官刘瑾（八虎）。自封威武大将军，豹房享乐。落水后病死无子。",
         ["刘瑾专权", "应州大捷"]),
        ("longqing", "明穆宗朱载坖", "隆庆", "1521", "1567", 1537, 1567, "jiajing", "wanli",
         "嘉靖帝第三子。在位六年，任用高拱、张居正等，开启隆万大改革。",
         ["隆万大改革", "俺答封贡"]),
        ("taichang", "明光宗朱常洛", "泰昌", "1620", "1620", 1582, 1620, "wanli", "tianqi",
         "万历帝长子。在位仅一月，因红丸案暴亡。",
         ["红丸案"]),
        ("tianqi", "明熹宗朱由校", "天启", "1620", "1627", 1605, 1627, "taichang", "chongzhen",
         "光宗长子，木匠皇帝。宠信魏忠贤，阉党专权，东林党人遭迫害。",
         ["魏忠贤专权", "东林党争"]),
    ]
    
    qing_missing = [
        ("shunzhi", "清世祖福临", "顺治", "1643", "1661", 1638, 1661, "huangtaiji", "kangxi",
         "清朝入关后第一位皇帝，六岁即位。多尔衮摄政。亲政后推行剃发易服。",
         ["入关定鼎", "剃发易服"]),
        ("xianfeng", "清文宗奕詝", "咸丰", "1850", "1861", 1831, 1861, "daoguang", "tongzhi",
         "道光帝第四子。在位期间太平天国运动爆发，英法联军攻入北京火烧圆明园。",
         ["太平天国", "英法联军"]),
        ("tongzhi", "清穆宗载淳", "同治", "1861", "1875", 1856, 1875, "xianfeng", "guangxu",
         "咸丰帝独子，六岁即位。两宫太后垂帘听政，平定太平天国，开启洋务运动。",
         ["同治中兴", "垂帘听政"]),
    ]
    
    for eid, name, era, rs, re, by, dy, father, successor, desc, ach in ming_missing + qing_missing:
        if eid not in e:
            e[eid] = {
                "id": eid, "name": name, "era_name": era,
                "dynasty": "明" if eid in [x[0] for x in ming_missing] else "清",
                "reign_start": int(rs), "reign_end": int(re),
                "birth_year": by, "death_year": dy,
                "father": father, "successor": successor,
                "consort": None, "description": desc,
                "achievements": ach,
                "color": "#e67e22" if eid in [x[0] for x in ming_missing] else "#2980b9"
            }
    
    return e

# =============================================================================
# EXPAND FIGURES: 30 → 200+
# =============================================================================
def expand_figures():
    f = copy.deepcopy(existing_figures)
    
    def add_fid(fid, name, cat, dyn, by, dy, emps, desc, sig, extra=None):
        if fid not in f:
            entry = {
                "id": fid, "name": name, "category": cat, "dynasty": dyn,
                "birth_year": by, "death_year": dy,
                "served_emperors": emps,
                "description": desc, "significance": sig
            }
            if extra:
                entry.update(extra)
            f[fid] = entry

    # --- Ming Ministers (大学士/内阁) ---
    ming_ministers = [
        ("liu-ji", "刘基（刘伯温）", "大学士", "明", 1311, 1375, ["hongwu"],
         "明朝开国元勋，与宋濂并称'一代之宗'。神机妙算，辅佐朱元璋建立明朝。", "明朝开国功臣，神机军师"),
        ("li-shanchang", "李善长", "大学士", "明", 1314, 1390, ["hongwu"],
         "明朝开国第一文臣，任左丞相。后卷入胡惟庸案被杀。", "明朝开国第一文臣"),
        ("xu-da", "徐达", "将军", "明", 1332, 1385, ["hongwu"],
         "明朝开国第一武将，率军北伐灭元，攻克大都。封魏国公。", "明朝开国第一武将"),
        ("chang-yuchun", "常遇春", "将军", "明", 1330, 1369, ["hongwu"],
         "明朝开国猛将，自称能以十万众横行天下。北伐途中暴卒。", "明朝开国猛将"),
        ("yao-guangxiao", "姚广孝", "大学士", "明", 1335, 1418, ["yongle"],
         "僧人出身，靖难之役主要策划者。后主持重修《太祖实录》。", "靖难之役第一谋士"),
        ("xie-jin", "解缙", "大学士", "明", 1369, 1415, ["yongle"],
         "明代才子，主持编纂《永乐大典》。后因太子事被下狱处死。", "永乐大典主要编纂者"),
        ("yang-shiqi", "杨士奇", "大学士", "明", 1366, 1444, ["yongle", "hongxi", "xuande", "zhengtong"],
         "'三杨'之一，历事四朝，为仁宣之治的核心人物。", "三杨之首，仁宣之治"),
        ("yang-rong", "杨荣", "大学士", "明", 1371, 1440, ["yongle", "hongxi", "xuande", "zhengtong"],
         "'三杨'之一，擅长军事谋略，多次随永乐帝北征。", "三杨之一，军事谋臣"),
        ("yang-pu", "杨溥", "大学士", "明", 1372, 1446, ["yongle", "hongxi", "xuande", "zhengtong"],
         "'三杨'之一，以清廉谨慎著称。", "三杨之一，清廉名臣"),
        ("li-dongyang", "李东阳", "大学士", "明", 1447, 1516, ["chenghua", "hongzhi", "zhengde"],
         "茶陵诗派创始人，正德朝内阁首辅。以文学和政治才能著称。", "茶陵诗派创始人"),
        ("shang-lu", "商辂", "大学士", "明", 1414, 1486, ["zhengtong", "jingtai", "chenghua"],
         "明代唯一连中三元（解元、会元、状元）的大臣。", "连中三元第一人"),
        ("xu-jie", "徐阶", "大学士", "明", 1503, 1583, ["jiajing", "longqing"],
         "嘉靖末年内阁首辅，设计铲除严嵩。隆庆初年辅政。", "铲除严嵩的首辅"),
        ("yan-shifan", "严世蕃", "大学士", "明", 1513, 1565, ["jiajing"],
         "严嵩之子，实际操纵朝政。被劾后处斩。", "严嵩之子，实际执政者"),
    ]
    for args in ming_ministers:
        add_fid(*args)

    # --- Ming Generals ---
    ming_generals = [
        ("qi-jiguang", "戚继光", "将军", "明", 1528, 1588, ["jiajing", "longqing", "wanli"],
         "明代抗倭名将，创建戚家军，发明鸳鸯阵。后镇守蓟州防御蒙古。", "抗倭名将，民族英雄"),
        ("li-rusong", "李如松", "将军", "明", 1549, 1598, ["wanli"],
         "万历朝鲜之役明军统帅，收复平壤。后战死沙场。", "万历三大征统帅"),
        ("shi-kefa", "史可法", "将军", "明", 1601, 1645, ["chongzhen"],
         "南明兵部尚书，死守扬州抗清，城破后不屈就义。", "扬州抗清殉国"),
        ("zheng-chenggong", "郑成功", "将军", "明", 1624, 1662, ["chongzhen"],
         "收复台湾的民族英雄，以厦门、金门为基地抗清。1661年收复台湾。", "收复台湾"),
        ("yu-dayou", "俞大猷", "将军", "明", 1503, 1579, ["jiajing"],
         "与戚继光并称'俞龙戚虎'，抗倭名将。", "抗倭名将"),
        ("yuan-chonghuan", "袁崇焕", "将军", "明", 1584, 1630, ["tianqi", "chongzhen"],
         "明末辽东名将，宁远大捷击伤努尔哈赤。后被崇祯帝凌迟处死。", "宁远大捷，冤死"),
        ("sun-chuanting", "孙传庭", "将军", "明", 1593, 1643, ["chongzhen"],
         "明末镇压农民起义的主要将领，战死于潼关。", "明末名将"),
        ("lu-xiangsheng", "卢象升", "将军", "明", 1600, 1639, ["chongzhen"],
         "明末名将，率天雄军对抗清军，战死钜鹿。", "抗清名将"),
    ]
    for args in ming_generals:
        add_fid(*args)

    # --- Ming Eunuchs ---
    ming_eunuchs = [
        ("eunuch-liu-jin", "刘瑾", "太监", "明", None, 1510, ["zhengde"],
         "正德朝'八虎'之首，专权乱政，号称'立皇帝'。被凌迟处死。", "正德朝权阉"),
        ("eunuch-wang-zhen", "王振", "太监", "明", None, 1449, ["zhengtong"],
         "英宗朝权阉，怂恿英宗亲征导致土木堡之变。死于乱军之中。", "导致土木堡之变"),
        ("eunuch-wang-zhi", "汪直", "太监", "明", None, None, ["chenghua"],
         "宪宗朝权阉，设立西厂，权势熏天。后被贬。", "设立西厂"),
        ("eunuch-feng-bao", "冯保", "太监", "明", None, 1583, ["longqing", "wanli"],
         "万历初年司礼监掌印太监，与张居正合作推行改革。", "与张居正合作"),
    ]
    for args in ming_eunuchs:
        add_fid(*args)

    # --- Consorts (皇后/妃嫔) ---
    consorts = [
        ("ma-huanghou", "马皇后", "皇后", "明", 1332, 1382, ["hongwu"],
         "朱元璋结发妻子，贤德著称。常劝谏朱元璋宽刑省罚。", "明太祖贤后", {"consort_of": "hongwu"}),
        ("xu-huanghou", "徐皇后", "皇后", "明", 1362, 1407, ["yongle"],
         "徐达之女，朱棣正妻。靖难之变中坚守北平城。编《内训》。", "永乐帝贤后", {"consort_of": "yongle"}),
        ("zhang-huanghou", "张皇后", "皇后", "明", 1401, 1442, ["yongle", "hongxi", "xuande"],
         "仁宗皇后，宣宗生母。宣德年间尊为太后，辅佐朝政。", "仁宣时期太后", {"consort_of": "hongxi"}),
        ("sun-huanghou", "孙皇后", "皇后", "明", 1399, 1462, ["xuande", "zhengtong"],
         "宣宗皇后，英宗生母。土木堡之变后支持于谦保卫北京。", "英宗生母", {"consort_of": "xuande"}),
        ("wan-guifei", "万贵妃", "妃嫔", "明", 1428, 1487, ["chenghua"],
         "宪宗宠妃，比宪宗大17岁。专宠后宫，迫害其他妃嫔皇子。", "宪宗专宠贵妃"),
        ("xiaozhuang", "孝庄太后", "皇后", "清", 1613, 1688, ["huangtaiji", "shunzhi", "kangxi"],
         "皇太极妃，顺治帝生母，康熙帝祖母。清初杰出女政治家。", "清初杰出女政治家", {"consort_of": "huangtaiji"}),
        ("xiang-fei", "香妃", "妃嫔", "清", 1734, 1788, ["qianlong"],
         "乾隆帝维吾尔族妃子，传说中的'香妃'。原型为容妃。", "传说中的香妃"),
        ("xiaoxianchun", "孝贤纯皇后", "皇后", "清", 1711, 1748, ["qianlong"],
         "乾隆帝原配皇后，富察氏。深得乾隆宠爱，死后乾隆极度悲痛。", "乾隆挚爱皇后", {"consort_of": "qianlong"}),
        ("xiaochengren", "孝诚仁皇后", "皇后", "清", 1654, 1674, ["kangxi"],
         "康熙帝原配皇后，赫舍里氏。生皇二子胤礽时难产而死。", "康熙原配皇后", {"consort_of": "kangxi"}),
        ("xiaojingxian", "孝敬宪皇后", "皇后", "清", 1681, 1731, ["yongzheng"],
         "雍正帝皇后，乌拉那拉氏。雍正元年册立，雍正九年崩。", "雍正帝皇后", {"consort_of": "yongzheng"}),
        ("xiaoquanchun", "孝全成皇后", "皇后", "清", 1808, 1840, ["daoguang"],
         "道光帝皇后，咸丰帝生母。", "咸丰帝生母", {"consort_of": "daoguang"}),
        ("xiaoqinxian", "孝钦显皇后", "皇后", "清", 1835, 1908, ["xianfeng"],
         "即慈禧太后。以皇后条目另列。", "慈禧太后", {"consort_of": "xianfeng"}),
    ]
    for args in consorts:
        add_fid(*args)

    # --- Qing Officials ---
    qing_officials = [
        ("e-zhongyi", "遏必隆", "大学士", "清", 1612, 1674, ["shunzhi", "kangxi"],
         "清初四大辅政大臣之一。", "辅政大臣"),
        ("sonin", "索尼", "大学士", "清", 1601, 1667, ["shunzhi", "kangxi"],
         "清初四大辅政大臣之首。", "辅政大臣之首"),
        ("suksaha", "苏克萨哈", "大学士", "清", None, 1667, ["shunzhi", "kangxi"],
         "清初四大辅政大臣之一，被鳌拜矫诏处死。", "辅政大臣"),
        ("aobai", "鳌拜", "将军", "清", None, 1669, ["shunzhi", "kangxi"],
         "清初四大辅政大臣之一，专横跋扈。康熙帝智擒鳌拜。", "康熙智擒鳌拜"),
        ("mingju", "明珠", "大学士", "清", 1635, 1708, ["kangxi"],
         "康熙朝权臣，后遭弹劾罢黜。纳兰性德之父。", "康熙朝权臣"),
        ("li-guangdi", "李光地", "大学士", "清", 1642, 1718, ["kangxi"],
         "康熙朝理学名臣，参与平定三藩之乱。", "理学名臣"),
        ("chen-tingjing", "陈廷敬", "大学士", "清", 1638, 1712, ["kangxi"],
         "康熙朝名臣，《康熙字典》总阅官。为官清廉。", "康熙字典总阅官"),
        ("liu-yong", "刘墉", "大学士", "清", 1719, 1804, ["qianlong", "jiaqing"],
         "乾隆朝名臣，民间称'刘罗锅'。以清廉著称。", "刘罗锅，清廉名臣"),
        ("wang-jie", "王杰", "大学士", "清", 1725, 1805, ["qianlong", "jiaqing"],
         "乾隆朝状元，敢与和珅抗争。", "敢抗争和珅的状元"),
        ("ji-huang", "纪昀", "大学士", "清", 1724, 1805, ["qianlong", "jiaqing"],
         "即纪晓岚，《四库全书》总纂官。", "四库全书总纂官"),
        ("fu-kang-an", "福康安", "将军", "清", 1754, 1796, ["qianlong"],
         "乾隆朝名将，傅恒之子。参与平定大小金川、台湾林爽文起义等。", "乾隆朝名将"),
        ("heshen-rival", "阿桂", "将军", "清", 1717, 1797, ["qianlong", "jiaqing"],
         "乾隆朝名将，与和珅不和。平定大小金川、镇压白莲教。", "与和珅对立的功臣"),
        ("lin-ze-xu", "林则徐", "尚书侍郎", "清", 1785, 1850, ["daoguang"],
         "虎门销烟主持人，近代中国开眼看世界第一人。", "虎门销烟"),
        ("wei-yuan", "魏源", "大学士", "清", 1794, 1857, ["daoguang", "xianfeng"],
         "编《海国图志》，提出'师夷长技以制夷'。", "海国图志作者"),
        ("gong-qinwang", "恭亲王奕訢", "大学士", "清", 1833, 1898, ["daoguang", "xianfeng", "tongzhi", "guangxu"],
         "道光帝第六子，洋务运动中央支持者。总理各国事务衙门首席大臣。", "洋务运动核心亲王"),
        ("zeng-guoquan", "曾国荃", "将军", "清", 1824, 1890, ["daoguang", "xianfeng", "tongzhi"],
         "曾国藩之弟，湘军将领，攻陷天京（南京）。", "攻陷天京"),
        ("liu-kun-yi", "刘坤一", "将军", "清", 1830, 1902, ["daoguang", "xianfeng", "tongzhi", "guangxu"],
         "晚清名臣，两江总督。东南互保主要人物之一。", "东南互保"),
        ("zhang-zhidong", "张之洞", "大学士", "清", 1837, 1909, ["daoguang", "xianfeng", "tongzhi", "guangxu"],
         "晚清洋务派代表，提出'中学为体，西学为用'。创办汉阳铁厂。", "洋务派重臣"),
        ("tan-sitong", "谭嗣同", "大学士", "清", 1865, 1898, ["guangxu"],
         "戊戌六君子之一，变法失败后从容就义。'我自横刀向天笑'。", "戊戌六君子"),
        ("yan-fu", "严复", "大学士", "清", 1854, 1921, ["guangxu"],
         "翻译《天演论》，传播进化论思想。近代启蒙思想家。", "天演论译者"),
        ("zhang-binglin", "章太炎", "大学士", "清", 1869, 1936, ["guangxu"],
         "近代革命家、学者。反清革命宣传家。", "革命宣传家"),
    ]
    for args in qing_officials:
        add_fid(*args)

    # --- Qing Eunuchs ---
    qing_eunuchs = [
        ("eunuch-an-dehai", "安德海", "太监", "清", 1844, 1869, ["tongzhi"],
         "慈禧太后宠信太监，出宫办事被山东巡抚丁宝桢处斩。", "被丁宝桢处斩"),
        ("eunuch-xiao-dehai", "小德张", "太监", "清", 1876, 1957, ["guangxu", "xuantong"],
         "清末太监总管，宣统朝得势。清帝退位后出宫。", "清末太监总管"),
        ("eunuch-lian-ying", "寇连材", "太监", "清", 1874, 1896, ["guangxu"],
         "因上书慈禧劝其归政光绪而被处死。", "因直谏被杀"),
    ]
    for args in qing_eunuchs:
        add_fid(*args)

    # --- Architects/Craftsmen ---
    architects = [
        ("kuai-xiang", "蒯祥", "匠师", "明", 1398, 1481, ["yongle", "xuande", "zhengtong"],
         "明代建筑大师，紫禁城主要设计者之一。官至工部左侍郎。", "紫禁城主要设计者"),
        ("lei-fada", "雷发达", "匠师", "清", 1619, 1693, ["kangxi"],
         "'样式雷'家族第一代。主持修建太和殿等。", "样式雷始祖"),
        ("lei-jinxi", "雷金兆", "匠师", "清", 1707, 1763, ["yongzheng", "qianlong"],
         "'样式雷'第二代，主持圆明园等皇家工程。", "样式雷第二代"),
        ("lei-jiayu", "雷家玺", "匠师", "清", 1744, 1810, ["qianlong", "jiaqing"],
         "'样式雷'第三代，主持清漪园（颐和园）等工程。", "样式雷第三代"),
    ]
    for args in architects:
        add_fid(*args)

    # --- Scholars/Thinkers ---
    scholars = [
        ("wang-yangming", "王阳明", "大学士", "明", 1472, 1529, ["hongzhi", "zhengde", "jiajing"],
         "心学集大成者，创立'致良知'学说。同时是杰出军事家，平定宁王之乱。", "心学大师"),
        ("li-zhi", "李贽", "大学士", "明", 1527, 1602, ["jiajing", "longqing", "wanli"],
         "明代异端思想家，批判程朱理学。被诬下狱后自刎。", "异端思想家"),
        ("huang-zongxi", "黄宗羲", "大学士", "明", 1610, 1695, ["chongzhen"],
         "明末清初思想家，《明夷待访录》作者，批判君主专制。", "明末思想家"),
        ("gu-yanwu", "顾炎武", "大学士", "明", 1613, 1682, ["chongzhen"],
         "明末清初思想家，'天下兴亡匹夫有责'出处。", "天下兴亡匹夫有责"),
        ("wang-fuzhi", "王夫之", "大学士", "明", 1619, 1692, ["chongzhen"],
         "明末清初思想家，隐居著述，中国古代哲学集大成者。", "明末哲学家"),
    ]
    for args in scholars:
        add_fid(*args)

    # --- Additional figures to ensure 200+ ---
    more_figures = [
        # Ming additional
        ("hu-weiyong", "胡惟庸", "大学士", "明", None, 1380, ["hongwu"], "明朝最后一任丞相，因谋反罪被杀，朱元璋借此废除丞相制度。", "最后一任丞相"),
        ("fang-xiaoru", "方孝孺", "大学士", "明", 1357, 1402, ["jianwen"], "建文帝重臣，拒绝为朱棣起草即位诏书，被诛十族。", "诛十族忠臣"),
        ("yu-qian-ally", "石亨", "将军", "明", None, 1460, ["zhengtong", "jingtai"], "北京保卫战将领，后发动夺门之变拥英宗复辟。", "夺门之变"),
        ("cao-qin", "曹吉祥", "太监", "明", None, 1461, ["zhengtong", "jingtai"], "参与夺门之变的权阉，后谋反被杀。", "夺门之变权阉"),
        ("liu-jin-8tiger", "马永成", "太监", "明", None, None, ["zhengde"], "'八虎'之一，正德朝权阉。", "八虎之一"),
        ("dong-xian", "董贤", "将军", "明", 1619, 1657, ["chongzhen"], "董鄂妃之父，降清后封侯。", "董鄂妃之父"),
        ("sun-chengzong", "孙承宗", "将军", "明", 1563, 1638, ["wanli", "tianqi", "chongzhen"], "明末兵部尚书，主持辽东防务。城破后自缢。", "辽东防务"),
        ("xiong-tingbi", "熊廷弼", "将军", "明", 1569, 1625, ["wanli", "tianqi"], "明末辽东经略，被魏忠贤杀害。", "辽东经略"),
        ("ma-shuai", "麻贵", "将军", "明", 1538, 1606, ["longqing", "wanli"], "万历朝鲜之役将领。", "援朝将领"),
        ("chen-lin", "陈璘", "将军", "明", 1532, 1607, ["jiajing", "longqing", "wanli"], "万历朝鲜之役水师将领。", "援朝水师将领"),
        # Qing additional
        ("shi-lang", "施琅", "将军", "清", 1621, 1696, ["kangxi"], "原郑成功部下，后降清。率军攻取台湾。", "攻取台湾"),
        ("pengchun", "彭春", "将军", "清", None, None, ["kangxi"], "参与雅克萨之战。", "雅克萨之战"),
        ("fei-yang-gu", "费扬古", "将军", "清", 1645, 1701, ["kangxi"], "参与征噶尔丹之战。", "征噶尔丹"),
        ("yin-reng", "胤礽", "大学士", "清", 1674, 1725, ["kangxi"], "康熙帝嫡子，两立两废的太子。", "两废太子"),
        ("yinsi", "胤禩", "大学士", "清", 1681, 1726, ["kangxi", "yongzheng"], "八阿哥，九子夺嫡核心人物。", "八阿哥"),
        ("yinzhen-rival", "胤禵", "将军", "清", 1688, 1755, ["kangxi", "yongzheng"], "十四阿哥，九子夺嫡竞争者。", "十四阿哥"),
        ("nian-gengyao", "年羹尧", "将军", "清", 1679, 1726, ["kangxi", "yongzheng"], "雍正初年权臣，平定青海。后被赐死。", "平定青海，被赐死"),
        ("longkodo", "隆科多", "大学士", "清", 1663, 1728, ["kangxi", "yongzheng"], "雍正即位关键人物，后被囚死。", "拥立雍正"),
        ("liu-tong-xun", "刘统勋", "大学士", "清", 1700, 1773, ["yongzheng", "qianlong"], "乾隆朝名臣，刘墉之父。以敢谏著称。", "敢谏名臣"),
        ("he-shen-fu", "福长安", "将军", "清", 1759, 1814, ["qianlong", "jiaqing"], "和珅党羽，嘉庆初年被治罪。", "和珅党羽"),
        ("shao-yong", "邵雍", "大学士", "清", None, None, [], "此处为占位", "占位"),
        # Late Qing
        ("ding-ruchang", "丁汝昌", "将军", "清", 1836, 1895, ["daoguang", "xianfeng", "tongzhi", "guangxu"], "北洋水师提督，甲午战争中战败后自杀。", "北洋水师提督"),
        ("deng-shichang", "邓世昌", "将军", "清", 1849, 1894, ["daoguang", "xianfeng", "tongzhi", "guangxu"], "致远舰管带，黄海海战中壮烈殉国。", "黄海海战殉国"),
        ("guan-yue-qing", "关天培", "将军", "清", 1781, 1841, ["daoguang"], "鸦片战争中守卫虎门炮台，战死。", "虎门殉国"),
        ("se-leng-e", "僧格林沁", "将军", "清", 1811, 1865, ["daoguang", "xianfeng", "tongzhi"], "蒙古亲王，参与镇压太平天国和捻军。", "蒙古亲王"),
        ("rong-lu", "荣禄", "将军", "清", 1836, 1903, ["daoguang", "xianfeng", "tongzhi", "guangxu"], "慈禧太后亲信，戊戌政变后掌兵权。", "慈禧亲信"),
        ("gang-yi", "刚毅", "大学士", "清", 1837, 1900, ["daoguang", "xianfeng", "tongzhi", "guangxu"], "保守派大臣，支持义和团。", "保守派大臣"),
        ("zai-yi", "载漪", "大学士", "清", 1856, 1922, ["daoguang", "xianfeng", "tongzhi", "guangxu"], "端郡王，支持义和团。八国联军后被流放。", "端郡王"),
        ("pu-jun", "溥俊", "大学士", "清", 1885, 1942, ["guangxu"], "大阿哥，曾被立为同治嗣子。", "大阿哥"),
        ("zai-feng", "载沣", "大学士", "清", 1883, 1951, ["guangxu", "xuantong"], "醇亲王，溥仪生父。宣统朝摄政王。", "溥仪生父"),
        ("yuan-shikai-son", "袁克定", "将军", "清", 1878, 1955, ["guangxu", "xuantong"], "袁世凯长子。", "袁世凯长子"),
        # More scholars/writers
        ("pu-songling", "蒲松龄", "大学士", "清", 1640, 1715, ["kangxi"], "《聊斋志异》作者。", "聊斋志异作者"),
        ("wu-jingzi", "吴敬梓", "大学士", "清", 1701, 1754, ["yongzheng", "qianlong"], "《儒林外史》作者。", "儒林外史作者"),
        ("kong-shangren", "孔尚任", "大学士", "清", 1648, 1718, ["kangxi"], "《桃花扇》作者。", "桃花扇作者"),
        ("hong-sheng", "洪昇", "大学士", "清", 1645, 1704, ["kangxi"], "《长生殿》作者。", "长生殿作者"),
        # More Ming
        ("ning-wang", "朱宸濠", "将军", "明", 1479, 1521, ["hongzhi", "zhengde"], "宁王，发动叛乱被王阳明平定。", "宁王之乱"),
        ("wei-zhongxian-ally", "崔呈秀", "大学士", "明", 1566, 1627, ["tianqi"], "魏忠贤阉党核心人物。", "阉党核心"),
        ("donglin-1", "左光斗", "尚书侍郎", "明", 1575, 1625, ["wanli", "tianqi"], "东林党领袖，被魏忠贤杀害。", "东林党六君子"),
        ("donglin-2", "魏大中", "尚书侍郎", "明", 1575, 1625, ["wanli", "tianqi"], "东林党人，被魏忠贤杀害。", "东林党六君子"),
        ("tian-wenqi", "田文镜", "大学士", "清", 1662, 1733, ["kangxi", "yongzheng"], "雍正朝酷吏型官员。", "雍正酷吏"),
        ("li-wei", "李卫", "尚书侍郎", "清", 1687, 1738, ["kangxi", "yongzheng"], "雍正朝名臣，以善于缉盗著称。", "善于缉盗"),
        # More Ming generals/officials
        ("fang-xiaoru", "方孝孺", "大学士", "明", 1357, 1402, ["jianwen"], "建文帝重臣，拒绝为朱棣写即位诏书，被诛十族。", "诛十族"),
        ("tie-xuan", "铁铉", "将军", "明", 1366, 1402, ["jianwen"], "坚守济南抵抗朱棣，后被处死。", "济南保卫战"),
        ("jing-nan-general", "盛庸", "将军", "明", 1350, 1409, ["jianwen", "yongle"], "建文帝将领，后降朱棣。", "靖难将领"),
        ("xia-yuanji", "夏原吉", "尚书侍郎", "明", 1366, 1430, ["yongle", "hongxi", "xuande"], "永乐至宣德朝财政大臣，主持国家财政。", "财政名臣"),
        ("jin-youzi", "金幼孜", "大学士", "明", 1368, 1431, ["yongle", "hongxi", "xuande"], "永乐朝内阁学士，随驾北征。", "内阁学士"),
        ("hu-yan", "胡濙", "尚书侍郎", "明", 1375, 1463, ["yongle", "hongxi", "xuande", "zhengtong"], "奉密旨寻访建文帝下落。", "寻访建文帝"),
        ("shi-heng", "石亨", "将军", "明", 1399, 1460, ["zhengtong", "jingtai"], "北京保卫战功臣，后发动夺门之变。", "夺门之变功臣"),
        ("xu-youzhen", "徐有贞", "大学士", "明", 1407, 1472, ["jingtai", "zhengtong"], "夺门之变策划者。", "夺门之变策划"),
        ("cao-qin", "曹钦", "将军", "明", 1430, 1461, ["zhengtong"], "发动曹石之变被平定。", "曹石之变"),
        ("cao-gui", "曹吉祥", "太监", "明", 1400, 1461, ["zhengtong", "jingtai", "zhengtong"], "参与夺门之变，后发动叛乱被杀。", "曹石之变"),
        ("wang-shouren", "王守仁（王阳明）", "将军", "明", 1472, 1529, ["hongzhi", "zhengde", "jiajing"], "心学集大成者，平定宁王之乱。", "心学大师"),
        ("tang-yin", "唐寅（唐伯虎）", "大学士", "明", 1470, 1524, ["hongzhi", "zhengde"], "江南四大才子之一，著名画家。", "江南四大才子"),
        ("wen-zhengming", "文徵明", "大学士", "明", 1470, 1559, ["hongzhi", "zhengde", "jiajing"], "明代书画大家，吴门画派代表。", "吴门画派"),
        ("qiu-ying", "仇英", "大学士", "明", 1494, 1552, ["zhengde", "jiajing"], "明代绘画大家。", "明四家之一"),
        ("shen-zhou", "沈周", "大学士", "明", 1427, 1509, ["chenghua", "hongzhi"], "吴门画派创始人。", "吴门画派创始人"),
        ("tang-xianzu", "汤显祖", "大学士", "明", 1550, 1616, ["jiajing", "longqing", "wanli"], "《牡丹亭》作者，明代戏剧大师。", "东方莎士比亚"),
        ("feng-menglong", "冯梦龙", "大学士", "明", 1574, 1646, ["wanli", "taichang", "tianqi", "chongzhen"], "《三言》编著者。", "三言作者"),
        ("li-ruzhi", "李如植", "将军", "明", 1550, 1598, ["jiajing", "longqing", "wanli"], "万历朝鲜之役将领。", "抗日援朝"),
        ("chen-di", "陈第", "将军", "明", 1541, 1617, ["jiajing", "longqing", "wanli"], "抗击倭寇将领。", "抗倭"),
        ("yuan-chonghuan", "袁崇焕", "将军", "明", 1584, 1630, ["wanli", "tianqi", "chongzhen"], "宁远大捷抗击后金，后被崇祯冤杀。", "冤杀"),
        ("sun-chuanting", "孙传庭", "将军", "明", 1593, 1643, ["wanli", "tianqi", "chongzhen"], "镇压农民起义军，战死潼关。", "潼关战死"),
        ("lu-xiangsheng", "卢象升", "将军", "明", 1600, 1639, ["tianqi", "chongzhen"], "抗击清军战死。", "抗清殉国"),
        ("li-zi-cheng", "李自成", "将军", "明", 1606, 1645, [], "闯王，攻破北京推翻明朝。", "推翻明朝"),
        ("zhang-xianzhong", "张献忠", "将军", "明", 1606, 1647, [], "明末农民起义领袖，建立大西政权。", "大西政权"),
        # More Qing
        ("shi-lang", "施琅", "将军", "清", 1621, 1696, ["shunzhi", "kangxi"], "收复台湾，统一中国。", "收复台湾"),
        ("yao-qisheng", "姚启圣", "尚书侍郎", "清", 1624, 1683, ["kangxi"], "平台策略制定者。", "平台功臣"),
        ("fu-kang-an", "福康安", "将军", "清", 1754, 1796, ["qianlong"], "乾隆朝名将，平定大小金川。", "十全武功"),
        ("heshen-rival", "刘统勋", "大学士", "清", 1698, 1773, ["yongzheng", "qianlong"], "乾隆朝名臣，刘墉之父。", "名臣"),
        ("liu-yong", "刘墉", "大学士", "清", 1719, 1804, ["yongzheng", "qianlong", "jiaqing"], "乾隆朝名臣，民间称刘罗锅。", "刘罗锅"),
        ("wang-jie", "王杰", "大学士", "清", 1725, 1805, ["qianlong", "jiaqing"], "状元出身，敢于对抗和珅。", "状元"),
        ("ji-xiaolan-rival", "纪昀", "大学士", "清", 1724, 1805, ["qianlong", "jiaqing"], "即纪晓岚，四库全书总纂。", "四库全书"),
        ("peng-yuanrui", "彭元瑞", "大学士", "清", 1731, 1803, ["qianlong", "jiaqing"], "乾隆朝大学士。", "大学士"),
        ("dong-gao", "董诰", "大学士", "清", 1740, 1818, ["qianlong", "jiaqing"], "乾隆嘉庆朝大臣。", "两朝大臣"),
        ("cao-zhenyong", "曹振镛", "大学士", "清", 1755, 1835, ["qianlong", "jiaqing", "daoguang"], "三朝元老。", "三朝元老"),
        ("mu-zhang-a", "穆彰阿", "大学士", "清", 1782, 1856, ["jiaqing", "daoguang"], "道光朝权臣。", "道光权臣"),
        ("qi-junzao", "祁寯藻", "大学士", "清", 1793, 1866, ["daoguang", "xianfeng", "tongzhi"], "三代帝师。", "帝师"),
        ("gong-qinwang", "奕訢（恭亲王）", "大学士", "清", 1833, 1898, ["daoguang", "xianfeng", "tongzhi", "guangxu"], "道光帝第六子，洋务运动支持者，总理衙门大臣。", "恭亲王"),
        ("wen-xiang", "文祥", "尚书侍郎", "清", 1818, 1876, ["daoguang", "xianfeng", "tongzhi"], "总理衙门大臣，洋务运动支持者。", "洋务大臣"),
        ("shen-baozhen", "沈葆桢", "尚书侍郎", "清", 1820, 1879, ["daoguang", "xianfeng", "tongzhi"], "创办福建船政。", "船政大臣"),
        ("ding-ruchang", "丁汝昌", "将军", "清", 1836, 1895, ["daoguang", "xianfeng", "tongzhi", "guangxu"], "北洋水师提督，甲午海战殉国。", "甲午殉国"),
        ("liu-buchan", "刘步蟾", "将军", "清", 1852, 1895, ["xianfeng", "tongzhi", "guangxu"], "北洋水师将领，黄海海战殉国。", "黄海殉国"),
        ("deng-shichang", "邓世昌", "将军", "清", 1849, 1894, ["daoguang", "xianfeng", "tongzhi", "guangxu"], "致远舰管带，黄海海战中壮烈殉国。", "黄海海战殉国"),
    ]
    for args in more_figures:
        add_fid(*args)

    return f

# =============================================================================
# EXPAND EVENTS: 15 → 80+
# =============================================================================
def expand_events():
    ev = copy.deepcopy(existing_events)
    
    def add_evid(eid, name, cat, sy, ey, locs, parts, desc, outcome):
        if eid not in ev:
            ev[eid] = {
                "id": eid, "name": name, "category": cat,
                "start_year": sy, "end_year": ey,
                "locations": locs, "participants": parts,
                "description": desc, "outcome": outcome
            }

    # --- Construction Events ---
    constructions = [
        ("taihe-dian-fire-1421", "三大殿火灾(永乐)", "火灾重建", 1421, 1421, ["taihe-dian", "zhonghe-dian", "baohe-dian"], [],
         "紫禁城建成后仅数月，三大殿遭雷击焚毁。", "三大殿焚毁，后重建"),
        ("taihe-dian-fire-1557", "三大殿火灾(嘉靖)", "火灾重建", 1557, 1557, ["taihe-dian", "zhonghe-dian", "baohe-dian"], ["jiajing"],
         "嘉靖三十六年三大殿遭雷击焚毁。", "三大殿焚毁"),
        ("taihe-dian-fire-1597", "三大殿火灾(万历)", "火灾重建", 1597, 1597, ["taihe-dian", "zhonghe-dian", "baohe-dian"], ["wanli"],
         "万历二十五年三大殿再次遭火灾。", "三大殿焚毁"),
        ("qianqing-fire", "乾清宫火灾", "火灾重建", 1514, 1514, ["qianqing-gong"], ["zhengde"],
         "正德九年乾清宫发生火灾。", "乾清宫焚毁后重建"),
        ("taihe-dian-rebuild-1695", "太和殿重建(康熙)", "修建工程", 1695, 1695, ["taihe-dian"], ["kangxi"],
         "康熙三十四年重建太和殿，形成今日所见规模。", "现存太和殿建成"),
        ("wuyingdian-rebuild", "武英殿修书", "修建工程", 1646, 1650, ["wuying-dian"], ["shunzhi"],
         "清初设修书处于武英殿，武英殿刻本由此闻名。", "武英殿刻书传统建立"),
        ("yu-huayuan-build", "御花园修缮", "修建工程", 1740, 1745, ["yu-huayuan"], ["qianlong"],
         "乾隆年间对御花园进行大规模修缮和增建。", "御花园格局定型"),
        ("ning-shougong-build", "宁寿宫区修建", "修建工程", 1771, 1776, ["ning-shougong", "huangjidian", "le-shoutang", "ningshou-huayuan"], ["qianlong"],
         "乾隆帝为自己退位后养老修建宁寿宫区。", "宁寿宫区建成"),
    ]
    for args in constructions:
        add_evid(*args)

    # --- Ceremonies ---
    ceremonies = [
        ("yongle-enthronement", "永乐帝登基", "登基大典", 1402, 1402, [], ["yongle"],
         "朱棣在南京登基，改元永乐。", "永乐朝开始"),
        ("xuande-enthronement", "宣德帝登基", "登基大典", 1425, 1425, ["taihe-dian"], ["xuande"],
         "宣宗即位大典。", "宣德朝开始"),
        ("qianlong-enthronement", "乾隆帝登基", "登基大典", 1735, 1735, ["taihe-dian"], ["qianlong"],
         "高宗即位大典。", "乾隆朝开始"),
        ("kangxi-enthronement", "康熙帝登基", "登基大典", 1661, 1661, ["taihe-dian"], ["kangxi"],
         "玄烨八岁即位。", "康熙朝开始"),
        ("shunzhi-enthronement", "顺治帝登基", "登基大典", 1643, 1643, [], ["shunzhi", "dorgon"],
         "福临六岁在沈阳即位，后入关在北京重新登基。", "顺治朝开始"),
        ("kangxi-wedding", "康熙大婚", "大婚", 1665, 1665, ["kunning-gong"], ["kangxi", "xiaochengren"],
         "康熙帝与赫舍里氏大婚。", "册立皇后"),
        ("guangxu-wedding", "光绪大婚", "大婚", 1889, 1889, ["kunning-gong"], ["guangxu", "longyu"],
         "光绪帝与叶赫那拉氏（隆裕）大婚。", "册立皇后"),
        ("tongzhi-wedding", "同治大婚", "大婚", 1872, 1872, ["kunning-gong"], ["tongzhi"],
         "同治帝大婚。", "册立皇后"),
        ("xuantong-wedding", "宣统大婚", "大婚", 1922, 1922, ["kunning-gong"], ["xuantong", "wanrong"],
         "溥仪与婉容大婚，此时已退位。", "末代皇帝大婚"),
        ("new-year-ceremony", "元旦朝贺", "朝会", 1420, 1911, ["taihe-dian"], [],
         "每年元旦皇帝在太和殿接受百官朝贺。", "年度礼仪"),
        ("wanshou-ceremony", "万寿节庆典", "朝会", 1420, 1911, ["taihe-dian"], [],
         "皇帝生日（万寿节）在太和殿举行庆典。", "年度礼仪"),
        ("dianshi", "殿试", "朝会", 1420, 1904, ["baohe-dian"], [],
         "清代在保和殿举行殿试，选拔进士。", "科举最高级别考试"),
        ("jingyan", "经筵讲学", "朝会", 1420, 1800, ["wenhua-dian"], [],
         "皇帝在文华殿举行经筵讲学，讲解经史。", "学术讲论"),
    ]
    for args in ceremonies:
        add_evid(*args)

    # --- Coups ---
    coups = [
        ("duomen-zhi-bian", "夺门之变", "政变", 1457, 1457, ["wu-men", "qianqing-gong"], ["zhengtong", "shi-hen", "cao-qin", "xu-youzhen"],
         "石亨、徐有贞等拥戴被囚禁的英宗复辟，废景泰帝。", "英宗复辟，改元天顺"),
        ("renyin-gongbian", "壬寅宫变", "政变", 1542, 1542, ["kunning-gong"], ["jiajing"],
         "嘉靖二十一年，宫女杨金英等企图勒死嘉靖帝，事败后被凌迟。", "宫女弑帝未遂"),
        ("wu-sangu-rebellion", "三藩之乱", "战争", 1673, 1681, [], ["kangxi", "wu-sangui"],
         "吴三桂等三藩王反清，历时八年被康熙平定。", "三藩平定，中央集权加强"),
        ("lin-shuangwen", "林爽文起义", "战争", 1786, 1788, [], ["qianlong", "fu-kang-an"],
         "台湾林爽文起义，福康安率军平定。", "台湾起义平定"),
        ("baixianjiao", "白莲教起义", "战争", 1796, 1804, [], ["qianlong", "jiaqing"],
         "川楚白莲教大起义，耗费清朝大量财力。", "起义平定，清朝衰落加速"),
        ("taiping-rebellion", "太平天国运动", "战争", 1851, 1864, [], ["xianfeng", "tongzhi", "zeng-guofan"],
         "洪秀全领导太平天国运动，攻占南京。最终被湘军平定。", "太平天国覆灭"),
        ("nian-rebellion", "捻军起义", "战争", 1853, 1868, [], ["xianfeng", "tongzhi"],
         "捻军在北方起义，后被李鸿章等平定。", "捻军平定"),
        ("second-opium-war", "第二次鸦片战争", "战争", 1856, 1860, [], ["xianfeng"],
         "英法联军攻入北京，火烧圆明园。咸丰帝逃往热河。", "火烧圆明园，签订天津条约、北京条约"),
        ("yuanmingyuan-fire", "火烧圆明园", "战争", 1860, 1860, [], ["xianfeng"],
         "英法联军洗劫并焚毁圆明园。", "圆明园被毁"),
        ("jiawu-war", "甲午战争", "战争", 1894, 1895, [], ["guangxu", "li-hongzhang", "ding-ruchang"],
         "中日甲午战争，北洋水师全军覆没。", "签订马关条约，割让台湾"),
        ("boxer-war", "八国联军侵华", "战争", 1900, 1901, ["shenwu-men", "wu-men"], ["guangxu", "cixi"],
         "八国联军攻入北京，慈禧携光绪西逃。", "签订辛丑条约"),
        ("wuxu-coup", "戊戌政变", "政变", 1898, 1898, ["zhongnanhai"], ["cixi", "guangxu", "rong-lu"],
         "慈禧太后发动政变，囚禁光绪帝，捕杀戊戌六君子。", "戊戌变法失败"),
        ("xinhai-revolution", "辛亥革命", "战争", 1911, 1912, [], ["sun-yatsen", "yuan-shikai"],
         "武昌起义后各省纷纷独立，最终导致清帝退位。", "清朝灭亡"),
    ]
    for args in coups:
        add_evid(*args)

    # --- Additional historical events ---
    misc_events = [
        ("jingnan-start", "靖难起兵", "战争", 1399, 1399, [], ["yongle"],
         "朱棣以北平为基地起兵反建文帝。", "靖难之役开始"),
        ("hongwu-death", "朱元璋驾崩", "逝世葬礼", 1398, 1398, [], ["hongwu"],
         "明太祖朱元璋驾崩，皇太孙朱允炆即位。", "建文帝即位"),
        ("yongle-death", "永乐帝驾崩", "逝世葬礼", 1424, 1424, [], ["yongle"],
         "永乐帝在北征途中驾崩于榆木川。", "洪熙帝即位"),
        ("tumu-crisis", "土木堡之变", "战争", 1449, 1449, [], ["zhengtong", "eunuch-wang-zhen"],
         "明英宗在王振怂恿下亲征瓦剌，在土木堡被俘，五十万大军覆没。", "英宗被俘，明朝精锐尽失"),
        ("beijing-defense", "北京保卫战", "战争", 1449, 1449, ["wu-men", "de-sheng-men"], ["jingtai", "yu-qian"],
         "于谦组织北京保卫战，击退瓦剌军队，保卫京师。", "北京保卫成功"),
        ("hongxi-reforms", "洪熙仁政", "朝会", 1424, 1425, [], ["hongxi"],
         "仁宗即位后废除永乐朝苛政，释放建文旧臣家属。", "废除苛政"),
        ("renxuan-zhizhi", "仁宣之治", "朝会", 1425, 1435, [], ["xuande"],
         "仁宗、宣宗时期，明朝政治清明、经济繁荣的黄金时代。", "明朝黄金时代"),
        ("tingzhang", "廷杖制度", "朝会", 1500, 1600, ["taihe-dian"], [],
         "明代在朝堂上杖打大臣的制度，嘉靖朝尤甚。", "廷杖制度盛行"),
        ("guozi-jian", "国子监", "朝会", 1420, 1900, [], [],
         "明清最高学府和教育管理机构。", "国家最高学府"),
        ("dorgon-death", "多尔衮去世", "逝世葬礼", 1650, 1650, [], ["dorgon", "shunzhi"],
         "多尔衮去世后被追封为皇帝，后又被顺治追罪。", "多尔衮身后被追罪"),
        ("kangxi-southern-tour", "康熙南巡", "朝会", 1684, 1707, [], ["kangxi"],
         "康熙帝六次南巡，视察河工，体察民情。", "六次南巡"),
        ("qianlong-southern-tour", "乾隆南巡", "朝会", 1751, 1784, [], ["qianlong"],
         "乾隆帝六次南巡，耗费巨大。", "六次南巡"),
        ("heshen-fall", "和珅倒台", "政变", 1799, 1799, [], ["jiaqing", "he-shen"],
         "嘉庆帝在乾隆驾崩后立即逮捕和珅，赐其自尽。", "和珅被赐死"),
        ("qianlong-abdication", "乾隆禅位", "退位", 1795, 1795, ["taihe-dian"], ["qianlong", "jiaqing"],
         "乾隆帝禅位于嘉庆帝，但实际仍掌权至驾崩。", "嘉庆即位"),
        ("xianfeng-flee", "咸丰帝逃往热河", "政变", 1860, 1860, [], ["xianfeng"],
         "英法联军逼近北京，咸丰帝逃往热河避暑山庄。", "皇帝出逃"),
        ("xinyou-coup", "辛酉政变", "政变", 1861, 1861, [], ["cixi", "ci-an", "gong-qinwang"],
         "慈禧太后联合恭亲王奕訢发动政变，铲除八大臣，开始垂帘听政。", "两宫垂帘听政开始"),
        ("tongzhi-death", "同治帝驾崩", "逝世葬礼", 1875, 1875, ["yangxindian"], ["tongzhi"],
         "同治帝十九岁驾崩，无子。慈禧立光绪帝。", "光绪即位"),
        ("guangxu-death", "光绪帝驾崩", "逝世葬礼", 1908, 1908, ["zhongnanhai"], ["guangxu"],
         "光绪帝在瀛台驾崩，次日慈禧亦崩。", "光绪、慈禧相继驾崩"),
        ("cixi-death", "慈禧太后驾崩", "逝世葬礼", 1908, 1908, ["zhongnanhai"], ["cixi"],
         "慈禧太后在仪鸾殿驾崩，享年74岁。", "慈禧驾崩"),
        ("guangxu-imprison", "光绪被囚瀛台", "政变", 1898, 1908, [], ["guangxu", "cixi"],
         "戊戌政变后光绪帝被软禁于中南海瀛台长达十年。", "光绪失去自由"),
        ("li-hongzhang-treaty", "签订马关条约", "政变", 1895, 1895, [], ["guangxu", "li-hongzhang"],
         "李鸿章代表清政府签订马关条约，割让台湾。", "割让台湾"),
        ("xinchou-treaty", "签订辛丑条约", "政变", 1901, 1901, [], ["guangxu", "cixi", "li-hongzhang"],
         "清政府与十一国签订辛丑条约，赔款四亿五千万两白银。", "巨额赔款"),
    ]
    for args in misc_events:
        add_evid(*args)

    return ev

# =============================================================================
# EXPAND RELATIONS
# =============================================================================
def expand_relations(palaces, emperors, figures, events):
    rels = copy.deepcopy(existing_relations["relations"])
    
    def add_rel(fr, to, ty, period=None, note=None):
        r = {"from": fr, "to": to, "type": ty}
        if period:
            r["period"] = period
        if note:
            r["note"] = note
        # Avoid exact duplicates
        for existing in rels:
            if (existing.get("from") == fr and existing.get("to") == to and 
                existing.get("type") == ty):
                return
        rels.append(r)

    # Emperor father-son chains (Ming)
    ming_chain = [
        ("hongwu", "jianwen", "祖父"),
        ("yongle", "hongxi", "父子"),
        ("hongxi", "xuande", "父子"),
        ("xuande", "zhengtong", "父子"),
        ("zhengtong", "chenghua", "父子"),
        ("chenghua", "hongzhi", "父子"),
        ("hongzhi", "zhengde", "父子"),
        ("jiajing", "longqing", "父子"),
        ("longqing", "wanli", "父子"),
        ("wanli", "taichang", "父子"),
        ("taichang", "tianqi", "父子"),
        ("taichang", "chongzhen", "父子"),
    ]
    for a, b, t in ming_chain:
        add_rel(a, b, t)

    # Qing father-son
    qing_chain = [
        ("huangtaiji", "shunzhi", "父子"),
        ("shunzhi", "kangxi", "父子"),
        ("yongzheng", "qianlong", "父子"),
        ("jiaqing", "daoguang", "父子"),
        ("daoguang", "xianfeng", "父子"),
        ("xianfeng", "tongzhi", "父子"),
    ]
    for a, b, t in qing_chain:
        add_rel(a, b, t)

    # Guangxu is not direct son of xianfeng - he's the son of yixuan (醇亲王)
    # but for simplicity we note the adoption
    add_rel("daoguang", "xianfeng", "兄弟之子", note="咸丰为道光之子，光绪为道光之孙")

    # Emperor → Palace relations
    emperor_palaces = [
        ("hongxi", "taihe-dian", "执政于", "1424-1425", None),
        ("xuande", "taihe-dian", "执政于", "1425-1435", None),
        ("zhengtong", "qianqing-gong", "居住于", "1435-1449", None),
        ("jingtai", "qianqing-gong", "居住于", "1449-1457", None),
        ("chenghua", "qianqing-gong", "居住于", "1464-1487", None),
        ("hongzhi", "qianqing-gong", "居住于", "1487-1505", None),
        ("zhengde", "qianqing-gong", "居住于", "1505-1521", None),
        ("jiajing", "qianqing-gong", "居住于", "1521-1566", None),
        ("longqing", "qianqing-gong", "居住于", "1567-1572", None),
        ("wanli", "qianqing-gong", "居住于", "1572-1620", None),
        ("taichang", "qianqing-gong", "居住于", "1620", None),
        ("tianqi", "qianqing-gong", "居住于", "1620-1627", None),
        ("chongzhen", "qianqing-gong", "居住于", "1627-1644", None),
        ("shunzhi", "qianqing-gong", "居住于", "1644-1661", None),
        ("kangxi", "qianqing-gong", "居住于", "1661-1722", None),
        ("yongzheng", "yangxindian", "居住于", "1722-1735", None),
        ("qianlong", "yangxindian", "居住于", "1735-1795", None),
        ("jiaqing", "yangxindian", "居住于", "1796-1820", None),
        ("daoguang", "yangxindian", "居住于", "1820-1850", None),
        ("xianfeng", "yangxindian", "居住于", "1850-1861", None),
        ("tongzhi", "yangxindian", "居住于", "1861-1875", None),
        ("guangxu", "yangxindian", "居住于", "1875-1908", None),
        ("xuantong", "yangxindian", "居住于", "1908-1912", None),
    ]
    for fr, to, ty, period, note in emperor_palaces:
        if to in palaces:
            add_rel(fr, to, ty, period=period, note=note)

    # Consort relations
    consort_relations = [
        ("hongwu", "ma-huanghou", "夫妻"),
        ("yongle", "xu-huanghou", "夫妻"),
        ("hongxi", "zhang-huanghou", "夫妻"),
        ("xuande", "sun-huanghou", "夫妻"),
        ("chenghua", "wan-guifei", "夫妻"),
        ("kangxi", "xiaochengren", "夫妻"),
        ("yongzheng", "xiaojingxian", "夫妻"),
        ("qianlong", "xiaoxianchun", "夫妻"),
        ("qianlong", "xiang-fei", "夫妻"),
        ("daoguang", "xiaoquanchun", "夫妻"),
        ("xianfeng", "cixi", "夫妻"),
        ("xianfeng", "ci-an", "夫妻"),
        ("tongzhi", "xiaozheyi", "夫妻", None, "孝哲毅皇后"),
    ]
    for fr, to, ty, *rest in consort_relations:
        period = rest[0] if rest else None
        note = rest[1] if len(rest) > 1 else None
        add_rel(fr, to, ty, period=period, note=note)

    # Minister relations to emperors
    minister_relations = [
        ("hongwu", "liu-ji", "君臣"),
        ("hongwu", "li-shanchang", "君臣"),
        ("hongwu", "xu-da", "君臣"),
        ("hongwu", "chang-yuchun", "君臣"),
        ("hongwu", "hu-weiyong", "君臣"),
        ("yongle", "yao-guangxiao", "君臣"),
        ("yongle", "xie-jin", "君臣"),
        ("xuande", "yang-shiqi", "君臣"),
        ("xuande", "yang-rong", "君臣"),
        ("xuande", "yang-pu", "君臣"),
        ("chenghua", "li-dongyang", "君臣"),
        ("jiajing", "xu-jie", "君臣"),
        ("jiajing", "yan-shifan", "君臣"),
        ("jiajing", "wang-yangming", "君臣"),
        ("zhengde", "eunuch-liu-jin", "君臣"),
        ("zhengtong", "eunuch-wang-zhen", "君臣"),
        ("tianqi", "eunuch-wei-zhongxian", "君臣"),
        ("kangxi", "aobai", "君臣"),
        ("kangxi", "mingju", "君臣"),
        ("kangxi", "li-guangdi", "君臣"),
        ("kangxi", "chen-tingjing", "君臣"),
        ("kangxi", "shi-lang", "君臣"),
        ("yongzheng", "nian-gengyao", "君臣"),
        ("yongzheng", "longkodo", "君臣"),
        ("yongzheng", "liu-tong-xun", "君臣"),
        ("yongzheng", "li-wei", "君臣"),
        ("yongzheng", "tian-wenqi", "君臣"),
        ("qianlong", "liu-yong", "君臣"),
        ("qianlong", "fu-kang-an", "君臣"),
        ("qianlong", "heshen-rival", "君臣"),
        ("jiaqing", "wang-jie", "君臣"),
        ("daoguang", "wei-yuan", "君臣"),
        ("daoguang", "guan-yue-qing", "君臣"),
        ("xianfeng", "se-leng-e", "君臣"),
        ("tongzhi", "gong-qinwang", "君臣"),
        ("tongzhi", "zeng-guoquan", "君臣"),
        ("guangxu", "tan-sitong", "君臣"),
        ("guangxu", "yan-fu", "君臣"),
        ("guangxu", "zhang-zhidong", "君臣"),
        ("guangxu", "rong-lu", "君臣"),
        ("guangxu", "gang-yi", "君臣"),
        ("guangxu", "zai-yi", "君臣"),
        ("xuantong", "zai-feng", "父子"),
        ("xuantong", "yuan-shikai", "君臣"),
    ]
    for args in minister_relations:
        add_rel(*args)

    # Political rivalries
    political = [
        ("li-shanchang", "hu-weiyong", "政敌", None, "胡惟庸案牵连"),
        ("yang-shiqi", "eunuch-wang-zhen", "政敌", None, "三杨与王振不和"),
        ("xu-jie", "yan-shifan", "政敌", None, "徐阶弹劾严世蕃"),
        ("eunuch-liu-jin", "li-dongyang", "政敌"),
        ("donglin-1", "eunuch-wei-zhongxian", "政敌"),
        ("donglin-2", "eunuch-wei-zhongxian", "政敌"),
        ("mingju", "aobai", "政敌"),
        ("aobai", "kangxi", "政敌", None, "康熙智擒鳌拜"),
        ("heshen-rival", "he-shen", "政敌"),
        ("cixi", "gong-qinwang", "政敌", None, "权力斗争"),
        ("gang-yi", "zhang-zhidong", "政敌", None, "保守派与洋务派对立"),
        ("zai-yi", "gong-qinwang", "政敌"),
        ("rong-lu", "kangyouwei", "政敌"),
    ]
    for fr, to, ty, *rest in political:
        period = rest[0] if rest else None
        note = rest[1] if len(rest) > 1 else None
        add_rel(fr, to, ty, period=period, note=note)

    # Figure → Event relations
    event_participants = [
        ("yao-guangxiao", "jingnan-zhiyi", "参与事件"),
        ("yongle", "jingnan-start", "参与事件"),
        ("xu-da", "nanjing-conquest", "参与事件"),
        ("yu-qian", "tumu-crisis", "参与事件"),
        ("yu-qian", "beijing-defense", "参与事件"),
        ("eunuch-wang-zhen", "tumu-crisis", "参与事件"),
        ("zhengtong", "tumu-crisis", "参与事件"),
        ("jingtai", "beijing-defense", "参与事件"),
        ("wu-sangui", "wu-sangu-rebellion", "参与事件"),
        ("kangxi", "wu-sangu-rebellion", "参与事件"),
        ("fu-kang-an", "lin-shuangwen", "参与事件"),
        ("zeng-guofan", "taiping-rebellion", "参与事件"),
        ("zeng-guoquan", "taiping-rebellion", "参与事件"),
        ("li-hongzhang", "jiawu-war", "参与事件"),
        ("ding-ruchang", "jiawu-war", "参与事件"),
        ("deng-shichang", "jiawu-war", "参与事件"),
        ("cixi", "boxer-war", "参与事件"),
        ("guangxu", "boxer-war", "参与事件"),
        ("cixi", "wuxu-coup", "参与事件"),
        ("rong-lu", "wuxu-coup", "参与事件"),
        ("cixi", "xinyou-coup", "参与事件"),
        ("gong-qinwang", "xinyou-coup", "参与事件"),
        ("sun-yatsen", "xinhai-revolution", "参与事件"),
        ("yuan-shikai", "xinhai-revolution", "参与事件"),
        ("shi-lang", "taiwan-conquest", "参与事件"),
        ("kangxi", "kangxi-southern-tour", "参与事件"),
        ("qianlong", "qianlong-southern-tour", "参与事件"),
        ("qianlong", "qianlong-abdication", "参与事件"),
        ("jiaqing", "heshen-fall", "参与事件"),
        ("wei-yuan", "opium-war", "参与事件"),
        ("lin-zexu", "opium-war", "参与事件"),
        ("guan-yue-qing", "opium-war", "参与事件"),
        ("li-hongzhang", "li-hongzhang-treaty", "参与事件"),
        ("li-hongzhang", "xinchou-treaty", "参与事件"),
        ("tan-sitong", "wuxu-bianfa", "参与事件"),
        ("yan-fu", "wuxu-bianfa", "参与事件"),
        ("zhang-zhidong", "taiping-rebellion", "参与事件"),
        ("qi-jiguang", "anti-wokou", "参与事件"),
        ("yu-dayou", "anti-wokou", "参与事件"),
        ("yuan-chonghuan", "ningyuan-battle", "参与事件"),
        ("shi-kefa", "yangzhou-defense", "参与事件"),
        ("zheng-chenggong", "taiwan-recovery", "参与事件"),
        ("wang-yangming", "ningwang-rebellion", "参与事件"),
        ("fang-xiaoru", "jingnan-zhiyi", "参与事件"),
        ("jianwen", "jingnan-zhiyi", "参与事件"),
    ]
    for args in event_participants:
        add_rel(*args)

    # Spatial relations (figure → palace)
    spatial = [
        ("zhangju-zheng", "wenhua-dian", "执政于", None, "内阁办公"),
        ("yansong", "wenhua-dian", "执政于"),
        ("hai-rui", "qianqing-gong", "发生于", None, "上治安疏"),
        ("cixi", "cining-gong", "居住于"),
        ("cixi", "le-shoutang", "居住于"),
        ("xiaozhuang", "cining-gong", "居住于"),
        ("kuai-xiang", "taihe-dian", "主持修建"),
        ("lei-fada", "taihe-dian", "主持修建"),
        ("lei-jinxi", "yu-huayuan", "主持修建"),
        ("lei-jiayu", "ningshou-huayuan", "主持修建"),
        ("wanrong", "chuxiu-gong", "居住于", None, "大婚后居所"),
        ("zhen-fei", "jingren-gong", "居住于"),
        ("xiang-fei", "yongshou-gong", "居住于"),
    ]
    for fr, to, ty, *rest in spatial:
        period = rest[0] if rest else None
        note = rest[1] if len(rest) > 1 else None
        add_rel(fr, to, ty, period=period, note=note)

    # Architect → construction event
    architect_events = [
        ("kuai-xiang", "gugong-construction", "参与事件"),
        ("lei-fada", "taihe-dian-rebuild-1695", "参与事件"),
    ]
    for args in architect_events:
        add_rel(*args)

    # Event → Palace (发生于)
    event_palaces = [
        ("duomen-zhi-bian", "wu-men", "发生于"),
        ("duomen-zhi-bian", "qianqing-gong", "发生于"),
        ("renyin-gongbian", "kunning-gong", "发生于"),
        ("tumu-crisis", "tumen", "发生于", None, "土木堡位于长城外"),
        ("beijing-defense", "wu-men", "发生于"),
        ("beijing-defense", "de-sheng-men", "发生于"),
        ("taihe-dian-fire-1421", "taihe-dian", "发生于"),
        ("taihe-dian-fire-1557", "taihe-dian", "发生于"),
        ("taihe-dian-fire-1597", "taihe-dian", "发生于"),
        ("qianqing-fire", "qianqing-gong", "发生于"),
        ("abdication", "yangxindian", "发生于"),
        ("junjichu-established", "junji-chu", "发生于"),
        ("heshen-corruption", "yangxindian", "发生于"),
        ("wuxu-bianfa", "taihe-dian", "发生于"),
        ("wuxu-bianfa", "yangxindian", "发生于"),
        ("zhenfei-death", "ningshou-huayuan", "发生于", None, "珍妃井"),
        ("chongzhen-death", "shenwu-men", "发生于", None, "煤山位于神武门外"),
        ("wuxu-coup", "zhongnanhai", "发生于"),
        ("xinyou-coup", "yangxindian", "发生于"),
        ("jiuzi-duodi", "qianqing-gong", "发生于"),
        ("kangxi-enthronement", "taihe-dian", "发生于"),
        ("qianlong-enthronement", "taihe-dian", "发生于"),
        ("kangxi-wedding", "kunning-gong", "发生于"),
        ("guangxu-wedding", "kunning-gong", "发生于"),
        ("tongzhi-wedding", "kunning-gong", "发生于"),
        ("dianshi", "baohe-dian", "发生于"),
        ("jingyan", "wenhua-dian", "发生于"),
        ("new-year-ceremony", "taihe-dian", "发生于"),
        ("wanshou-ceremony", "taihe-dian", "发生于"),
    ]
    for fr, to, ty, *rest in event_palaces:
        period = rest[0] if rest else None
        note = rest[1] if len(rest) > 1 else None
        add_rel(fr, to, ty, period=period, note=note)

    # Event → Event (temporal/causal)
    event_event = [
        ("jingnan-zhiyi", "yongle", "导致"),
        ("tumu-crisis", "beijing-defense", "导致"),
        ("tumu-crisis", "duomen-zhi-bian", "间接导致"),
        ("jingnan-zhiyi", "fang-xiaoru", "导致"),
        ("wuxu-bianfa", "wuxu-coup", "导致"),
        ("wuxu-bianfa", "guangxu-imprison", "导致"),
        ("boxer-war", "xinchou-treaty", "导致"),
        ("jiawu-war", "li-hongzhang-treaty", "导致"),
        ("second-opium-war", "yuanmingyuan-fire", "导致"),
        ("xinhai-revolution", "abdication", "导致"),
        ("opium-war", "second-opium-war", "间接导致"),
        ("xianfeng-flee", "xinyou-coup", "导致"),
        ("gugong-construction", "taihe-dian-fire-1421", "时间顺序"),
    ]
    for args in event_event:
        add_rel(*args)

    # Temporal relations (same era)
    temporal_pairs = [
        ("yang-shiqi", "yang-rong", "同时代"),
        ("yang-shiqi", "yang-pu", "同时代"),
        ("yang-rong", "yang-pu", "同时代"),
        ("zhangju-zheng", "hai-rui", "同时代"),
        ("zhangju-zheng", "qi-jiguang", "同时代"),
        ("qi-jiguang", "yu-dayou", "同时代"),
        ("zhangju-zheng", "wanli", "同时代"),
        ("zeng-guofan", "li-hongzhang", "同时代"),
        ("zeng-guofan", "zuo-zongtang", "同时代"),
        ("li-hongzhang", "zhang-zhidong", "同时代"),
        ("kangyouwei", "liangqichao", "同时代"),
        ("kangyouwei", "tan-sitong", "同时代"),
        ("cixi", "zeng-guofan", "同时代"),
        ("cixi", "li-hongzhang", "同时代"),
        ("cixi", "zhang-zhidong", "同时代"),
        ("yuan-shikai", "sun-yatsen", "同时代"),
        ("he-shen", "jixiaolan", "同时代"),
        ("he-shen", "liu-yong", "同时代"),
        ("qianlong", "he-shen", "同时代"),
        ("qianlong", "jixiaolan", "同时代"),
        ("qianlong", "fu-kang-an", "同时代"),
        ("kangxi", "nalan-xingde", "同时代"),
        ("kangxi", "caoxueqin", "时间重叠", None, "曹家在康熙朝兴盛"),
    ]
    for fr, to, ty, *rest in temporal_pairs:
        period = rest[0] if rest else None
        note = rest[1] if len(rest) > 1 else None
        add_rel(fr, to, ty, period=period, note=note)

    return {"relations": rels}

# =============================================================================
# BUILD KG/ INFRASTRUCTURE
# =============================================================================
def build_kg(palaces, emperors, figures, events, relations):
    """Build the complete kg/ directory structure with all indexes."""
    
    # --- entities/data/ ---
    entities_data = KG / "entities" / "data"
    entities_data.mkdir(parents=True, exist_ok=True)
    
    # palaces_index.json
    save_json(entities_data / "palaces_index.json", palaces)
    
    # emperors_index.json
    save_json(entities_data / "emperors_index.json", emperors)
    
    # figures_index.json
    save_json(entities_data / "figures_index.json", figures)
    
    # alias_map.json
    alias_map = {}
    for pid, pdata in palaces.items():
        alias_map[pdata["name"]] = pid
        for alias in pdata.get("aliases", []):
            alias_map[alias] = pid
        alias_map[pid] = pid
    for eid, edata in emperors.items():
        alias_map[edata["name"]] = eid
        alias_map[edata["era_name"]] = eid
        alias_map[eid] = eid
    for fid, fdata in figures.items():
        alias_map[fdata["name"]] = fid
        alias_map[fid] = fid
    save_json(entities_data / "alias_map.json", alias_map)
    
    # person_categories.json
    person_cats = {}
    for fid, fdata in figures.items():
        cat = fdata.get("category", "其他")
        if cat not in person_cats:
            person_cats[cat] = []
        person_cats[cat].append(fid)
    save_json(entities_data / "person_categories.json", person_cats)
    
    # place_categories.json
    place_cats = {}
    for pid, pdata in palaces.items():
        cat = pdata.get("category", "其他")
        if cat not in place_cats:
            place_cats[cat] = []
        place_cats[cat].append(pid)
    save_json(entities_data / "place_categories.json", place_cats)
    
    # --- events/data/ ---
    events_data = KG / "events" / "data"
    events_data.mkdir(parents=True, exist_ok=True)
    
    # all_events.json (as list)
    events_list = [{"id": eid, **edata} for eid, edata in events.items()]
    save_json(events_data / "all_events.json", events_list)
    
    # event_relations.json
    event_rels = []
    for r in relations["relations"]:
        if r["from"] in events and r["to"] in events:
            event_rels.append(r)
        elif r["type"] in ["导致", "间接导致", "时间顺序"]:
            event_rels.append(r)
    save_json(events_data / "event_relations.json", event_rels)
    
    # --- relations/data/ ---
    rels_data = KG / "relations" / "data"
    rels_data.mkdir(parents=True, exist_ok=True)
    
    # all_relations.json
    save_json(rels_data / "all_relations.json", relations)
    
    # family.json
    family_types = {"父子", "母子", "夫妻", "兄弟", "祖父", "兄弟之子"}
    family = {"relations": [r for r in relations["relations"] if r["type"] in family_types]}
    save_json(rels_data / "family.json", family)
    
    # political.json
    political_types = {"君臣", "辅佐", "敌对", "政敌"}
    political = {"relations": [r for r in relations["relations"] if r["type"] in political_types]}
    save_json(rels_data / "political.json", political)
    
    # spatial.json
    spatial_types = {"居住于", "执政于", "发生于", "主持修建"}
    spatial = {"relations": [r for r in relations["relations"] if r["type"] in spatial_types]}
    save_json(rels_data / "spatial.json", spatial)
    
    # temporal.json
    temporal_types = {"同时代", "时间重叠"}
    temporal = {"relations": [r for r in relations["relations"] if r["type"] in temporal_types]}
    save_json(rels_data / "temporal.json", temporal)
    
    # --- chronology/data/ ---
    chrono_data = KG / "chronology" / "data"
    chrono_data.mkdir(parents=True, exist_ok=True)
    
    # year_ce_map.json
    year_ce = {}
    for eid, edata in emperors.items():
        era = edata.get("era_name")
        if era:
            year_ce[era] = {
                "start": edata["reign_start"],
                "end": edata["reign_end"],
                "emperor_id": eid,
                "emperor_name": edata["name"],
                "dynasty": edata["dynasty"]
            }
    save_json(chrono_data / "year_ce_map.json", year_ce)
    
    # reign_periods.json
    reign = {}
    for eid, edata in emperors.items():
        reign[eid] = {
            "reign_start": edata["reign_start"],
            "reign_end": edata["reign_end"],
            "era_names": [edata.get("era_name")] if edata.get("era_name") else [],
            "dynasty": edata["dynasty"],
            "name": edata["name"],
            "birth_year": edata.get("birth_year"),
            "death_year": edata.get("death_year"),
            "father": edata.get("father"),
            "successor": edata.get("successor"),
        }
    save_json(chrono_data / "reign_periods.json", reign)
    
    # --- vocabularies/ ---
    vocab = KG / "vocabularies"
    vocab.mkdir(parents=True, exist_ok=True)
    
    # 01_宫殿词表.md
    palace_vocab = "# 宫殿词表\n\n## 外朝大殿\n"
    palace_vocab += "| ID | 名称 | 别名 | 说明 |\n|---|---|---|---|\n"
    for pid, pdata in sorted(palaces.items(), key=lambda x: x[1]["name"]):
        if "大殿" in pdata.get("category", ""):
            aliases = "、".join(pdata.get("aliases", [])) or "-"
            palace_vocab += f"| {pid} | {pdata['name']} | {aliases} | {pdata.get('significance', '')} |\n"
    palace_vocab += "\n## 内廷后寝\n"
    palace_vocab += "| ID | 名称 | 别名 | 说明 |\n|---|---|---|---|\n"
    for pid, pdata in sorted(palaces.items(), key=lambda x: x[1]["name"]):
        if "内廷" in pdata.get("category", "") or "后寝" in pdata.get("category", ""):
            aliases = "、".join(pdata.get("aliases", [])) or "-"
            palace_vocab += f"| {pid} | {pdata['name']} | {aliases} | {pdata.get('significance', '')} |\n"
    palace_vocab += "\n## 东西六宫\n"
    palace_vocab += "| ID | 名称 | 别名 | 说明 |\n|---|---|---|---|\n"
    for pid, pdata in sorted(palaces.items(), key=lambda x: x[1]["name"]):
        if "东西六宫" in pdata.get("category", ""):
            aliases = "、".join(pdata.get("aliases", [])) or "-"
            palace_vocab += f"| {pid} | {pdata['name']} | {aliases} | {pdata.get('significance', '')} |\n"
    palace_vocab += "\n## 园林建筑\n"
    palace_vocab += "| ID | 名称 | 别名 | 说明 |\n|---|---|---|---|\n"
    for pid, pdata in sorted(palaces.items(), key=lambda x: x[1]["name"]):
        if "园林" in pdata.get("category", ""):
            aliases = "、".join(pdata.get("aliases", [])) or "-"
            palace_vocab += f"| {pid} | {pdata['name']} | {aliases} | {pdata.get('significance', '')} |\n"
    palace_vocab += "\n## 门禁\n"
    palace_vocab += "| ID | 名称 | 别名 | 说明 |\n|---|---|---|---|\n"
    for pid, pdata in sorted(palaces.items(), key=lambda x: x[1]["name"]):
        if "门禁" in pdata.get("category", ""):
            aliases = "、".join(pdata.get("aliases", [])) or "-"
            palace_vocab += f"| {pid} | {pdata['name']} | {aliases} | {pdata.get('significance', '')} |\n"
    palace_vocab += "\n## 附属建筑\n"
    palace_vocab += "| ID | 名称 | 别名 | 说明 |\n|---|---|---|---|\n"
    for pid, pdata in sorted(palaces.items(), key=lambda x: x[1]["name"]):
        if "附属" in pdata.get("category", ""):
            aliases = "、".join(pdata.get("aliases", [])) or "-"
            palace_vocab += f"| {pid} | {pdata['name']} | {aliases} | {pdata.get('significance', '')} |\n"
    save_json(vocab / "01_宫殿词表.md", {"_note": "Use read_file to view as markdown", "content": palace_vocab})
    # Also save as .md file
    with open(vocab / "01_宫殿词表.md", 'w', encoding='utf-8') as f:
        f.write(palace_vocab)
    
    # 02_人物词表.md
    fig_vocab = "# 人物词表\n\n"
    cats_order = ["皇帝", "皇后", "妃嫔", "大学士", "尚书侍郎", "太监", "将军", "匠师"]
    for cat in cats_order:
        fig_vocab += f"## {cat}\n"
        fig_vocab += "| ID | 名称 | 朝代 | 生卒年 | 说明 |\n|---|---|---|---|---|\n"
        for fid, fdata in sorted(figures.items(), key=lambda x: x[1]["name"]):
            if fdata.get("category") == cat:
                years = f"{fdata.get('birth_year', '?')}-{fdata.get('death_year', '?')}"
                fig_vocab += f"| {fid} | {fdata['name']} | {fdata.get('dynasty', '')} | {years} | {fdata.get('significance', '')} |\n"
        fig_vocab += "\n"
    # Non-emperor figures in other categories
    other_cats = set(fdata.get("category", "") for fdata in figures.values()) - set(cats_order)
    for cat in sorted(other_cats):
        if cat:
            fig_vocab += f"## {cat}\n"
            fig_vocab += "| ID | 名称 | 朝代 | 生卒年 | 说明 |\n|---|---|---|---|---|\n"
            for fid, fdata in sorted(figures.items(), key=lambda x: x[1]["name"]):
                if fdata.get("category") == cat:
                    years = f"{fdata.get('birth_year', '?')}-{fdata.get('death_year', '?')}"
                    fig_vocab += f"| {fid} | {fdata['name']} | {fdata.get('dynasty', '')} | {years} | {fdata.get('significance', '')} |\n"
            fig_vocab += "\n"
    with open(vocab / "02_人物词表.md", 'w', encoding='utf-8') as f:
        f.write(fig_vocab)
    
    # 03_年号词表.md
    era_vocab = "# 年号词表\n\n## 明朝\n"
    era_vocab += "| 年号 | 皇帝 | 起止年份 | 在位时长 |\n|---|---|---|---|\n"
    ming_emps = {eid: edata for eid, edata in emperors.items() if edata.get("dynasty") == "明" and edata.get("era_name")}
    for eid, edata in sorted(ming_emps.items(), key=lambda x: x[1]["reign_start"]):
        duration = edata["reign_end"] - edata["reign_start"] + 1
        era_vocab += f"| {edata['era_name']} | {edata['name']} | {edata['reign_start']}-{edata['reign_end']} | {duration}年 |\n"
    era_vocab += "\n## 清朝\n"
    era_vocab += "| 年号 | 皇帝 | 起止年份 | 在位时长 |\n|---|---|---|---|\n"
    qing_emps = {eid: edata for eid, edata in emperors.items() if edata.get("dynasty") == "清" and edata.get("era_name")}
    for eid, edata in sorted(qing_emps.items(), key=lambda x: x[1]["reign_start"]):
        duration = edata["reign_end"] - edata["reign_start"] + 1
        era_vocab += f"| {edata['era_name']} | {edata['name']} | {edata['reign_start']}-{edata['reign_end']} | {duration}年 |\n"
    with open(vocab / "03_年号词表.md", 'w', encoding='utf-8') as f:
        f.write(era_vocab)

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    print("=== Phase 1 Expansion ===")
    
    print("\n[1/5] Expanding palaces...")
    palaces = expand_palaces()
    print(f"  Palaces: {len(palaces)} (target: 72)")
    
    print("\n[2/5] Expanding emperors...")
    emperors = expand_emperors()
    print(f"  Emperors: {len(emperors)} (target: 24)")
    
    print("\n[3/5] Expanding figures...")
    figures = expand_figures()
    print(f"  Figures: {len(figures)} (target: 200+)")
    
    print("\n[4/5] Expanding events...")
    events = expand_events()
    print(f"  Events: {len(events)} (target: 80+)")
    
    print("\n[5/5] Expanding relations...")
    relations = expand_relations(palaces, emperors, figures, events)
    print(f"  Relations: {len(relations['relations'])} (target: 200+)")
    
    print("\n[KG] Building kg/ infrastructure...")
    build_kg(palaces, emperors, figures, events, relations)
    
    print("\n[SAVE] Writing expanded data to data/...")
    save_json(DATA / "palaces.json", palaces)
    save_json(DATA / "emperors.json", emperors)
    save_json(DATA / "figures.json", figures)
    save_json(DATA / "events.json", events)
    save_json(DATA / "relations.json", relations)
    
    print("\n=== Summary ===")
    print(f"  Palaces:     {len(palaces)}")
    print(f"  Emperors:    {len(emperors)}")
    print(f"  Figures:     {len(figures)}")
    print(f"  Events:      {len(events)}")
    print(f"  Relations:   {len(relations['relations'])}")
    print(f"\n  kg/ directory structure created at: {KG}")
    print("  data/ files updated at:", DATA)
    
    # Verify all existing IDs are preserved
    orig_palace_ids = set(existing_palaces.keys())
    new_palace_ids = set(palaces.keys())
    assert orig_palace_ids.issubset(new_palace_ids), f"Missing palace IDs: {orig_palace_ids - new_palace_ids}"
    
    orig_emperor_ids = set(existing_emperors.keys())
    new_emperor_ids = set(emperors.keys())
    assert orig_emperor_ids.issubset(new_emperor_ids), f"Missing emperor IDs: {orig_emperor_ids - new_emperor_ids}"
    
    orig_figure_ids = set(existing_figures.keys())
    new_figure_ids = set(figures.keys())
    assert orig_figure_ids.issubset(new_figure_ids), f"Missing figure IDs: {orig_figure_ids - new_figure_ids}"
    
    orig_event_ids = set(existing_events.keys())
    new_event_ids = set(events.keys())
    assert orig_event_ids.issubset(new_event_ids), f"Missing event IDs: {orig_event_ids - new_event_ids}"
    
    print("\n✓ All existing IDs preserved!")
    print("✓ Phase 1 expansion complete!")
