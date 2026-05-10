const PALACES = {
  "taihe-dian": {"id": "taihe-dian", "name": "太和殿", "aliases": ["金銮殿", "奉天殿"], "category": "外朝大殿", "built_year": 1420, "rebuilt_years": [1441, 1695], "dynasty": "明清", "coordinates": {"x": 500, "y": 280}, "width": 100, "height": 55, "description": "故宫最大的宫殿，皇帝登基、大婚、命将出征、万寿节（皇帝生日）等重大典礼场所。殿内正中设金漆雕龙宝座，上悬\"建极绥猷\"匾额。", "significance": "皇权象征，国家最高礼仪中心", "dimensions": {"width_m": 63.5, "depth_m": 37.2, "height_m": 35.05}, "color": "#d4a017"},
  "zhonghe-dian": {"id": "zhonghe-dian", "name": "中和殿", "aliases": ["华盖殿"], "category": "外朝大殿", "built_year": 1420, "rebuilt_years": [1695], "dynasty": "明清", "coordinates": {"x": 500, "y": 350}, "width": 55, "height": 50, "description": "皇帝去太和殿举行大典前在此休息、接受执事官朝拜之处。方形殿，四面开门。", "significance": "大典前的准备场所", "dimensions": {"width_m": 24.15, "depth_m": 24.15, "height_m": 19.7}, "color": "#d4a017"},
  "baohe-dian": {"id": "baohe-dian", "name": "保和殿", "aliases": ["谨身殿"], "category": "外朝大殿", "built_year": 1420, "rebuilt_years": [1695], "dynasty": "明清", "coordinates": {"x": 500, "y": 420}, "width": 90, "height": 50, "description": "明代大典前皇帝更衣之处。清代为除夕、正月十五皇帝宴饮外藩王公及公主额驸的场所，也是殿试考场。", "significance": "殿试场所，宴会厅", "dimensions": {"width_m": 53.4, "depth_m": 27.75, "height_m": 29.5}, "color": "#d4a017"},
  "qianqing-gong": {"id": "qianqing-gong", "name": "乾清宫", "aliases": [], "category": "内廷后寝", "built_year": 1420, "rebuilt_years": [1695, 1798], "dynasty": "明清", "coordinates": {"x": 500, "y": 520}, "width": 90, "height": 45, "description": "明代至清初皇帝的寝宫和处理日常政务之所。清康熙前为皇帝寝宫，雍正后移至养心殿。\"正大光明\"匾后曾藏立储密匣。", "significance": "皇帝寝宫（清初前），理政中心", "dimensions": {"width_m": 45.3, "depth_m": 21.6, "height_m": 20.0}, "color": "#c0392b"},
  "jiaotai-dian": {"id": "jiaotai-dian", "name": "交泰殿", "aliases": [], "category": "内廷后寝", "built_year": 1420, "rebuilt_years": [1695], "dynasty": "明清", "coordinates": {"x": 500, "y": 575}, "width": 50, "height": 40, "description": "皇后生日、元旦、冬至接受朝贺之处。殿内正中设宝座，存放二十五方宝玺。后部设铜壶滴漏和自鸣钟。", "significance": "皇后礼仪场所，存放宝玺", "dimensions": {"width_m": 20.3, "depth_m": 16.8, "height_m": 16.5}, "color": "#c0392b"},
  "kunning-gong": {"id": "kunning-gong", "name": "坤宁宫", "aliases": [], "category": "内廷后寝", "built_year": 1420, "rebuilt_years": [1695], "dynasty": "明清", "coordinates": {"x": 500, "y": 625}, "width": 85, "height": 45, "description": "明代皇后寝宫。清代改为祭神场所，东暖阁为皇帝大婚洞房。殿内设有萨满教祭祀设施，保留满族传统。", "significance": "皇后寝宫（明），祭神场所（清），大婚洞房", "dimensions": {"width_m": 42.8, "depth_m": 16.3, "height_m": 15.8}, "color": "#c0392b"},
  "yanxi-gong": {"id": "yanxi-gong", "name": "延禧宫", "aliases": ["水晶宫"], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [1851, 1909], "dynasty": "明清", "coordinates": {"x": 680, "y": 560}, "width": 60, "height": 40, "description": "东西六宫之一。清代多位妃嫔曾居此。宣统元年（1909）改建为西式三层\"水晶宫\"，因辛亥革命停工。", "significance": "妃嫔居所，晚清西洋建筑尝试", "dimensions": {}, "color": "#8e44ad"},
  "chuxiu-gong": {"id": "chuxiu-gong", "name": "储秀宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [1884], "dynasty": "明清", "coordinates": {"x": 320, "y": 560}, "width": 60, "height": 40, "description": "西六宫之一。慈禧太后入宫时居于此，后为庆祝五十大寿斥巨资修缮。光绪大婚时，慈禧居于此宫。", "significance": "慈禧入宫居所", "dimensions": {}, "color": "#8e44ad"},
  "yangxindian": {"id": "yangxindian", "name": "养心殿", "aliases": [], "category": "内廷后寝", "built_year": 1723, "rebuilt_years": [], "dynasty": "清", "coordinates": {"x": 390, "y": 490}, "width": 70, "height": 50, "description": "雍正起清代皇帝的寝宫和理政中心。\"勤政亲贤\"匾额下是皇帝日常办公之处。晚清慈禧太后在此垂帘听政。", "significance": "清雍正后皇帝实际寝宫，垂帘听政地", "dimensions": {}, "color": "#c0392b"},
  "junji-chu": {"id": "junji-chu", "name": "军机处", "aliases": [], "category": "附属建筑", "built_year": 1729, "rebuilt_years": [], "dynasty": "清", "coordinates": {"x": 450, "y": 450}, "width": 35, "height": 25, "description": "雍正七年（1729）设立，清朝中后期实际最高权力机关。军机大臣在此每日觐见皇帝，处理军国大事。", "significance": "清代中后期最高决策机构", "dimensions": {}, "color": "#7f8c8d"},
  "taihe-men": {"id": "taihe-men", "name": "太和门", "aliases": ["奉天门"], "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [1889], "dynasty": "明清", "coordinates": {"x": 500, "y": 200}, "width": 100, "height": 35, "description": "外朝正门，皇帝御门听政之处。明代称奉天门。", "significance": "外朝正门，御门听政", "dimensions": {}, "color": "#d4a017"},
  "wu-men": {"id": "wu-men", "name": "午门", "aliases": ["五凤楼"], "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 500, "y": 100}, "width": 120, "height": 40, "description": "紫禁城正南门，呈'凹'字形，中门为皇帝专用。举行献俘礼、颁布历书之处。", "significance": "紫禁城正门，国家礼仪象征", "dimensions": {}, "color": "#d4a017"},
  "duan-men": {"id": "duan-men", "name": "端门", "aliases": [], "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 500, "y": 50}, "width": 100, "height": 35, "description": "位于午门之北、天安门之南，形制与天安门相似。", "significance": "皇城礼仪通道", "dimensions": {}, "color": "#d4a017"},
  "wenhua-dian": {"id": "wenhua-dian", "name": "文华殿", "aliases": [], "category": "外朝大殿", "built_year": 1420, "rebuilt_years": [1695], "dynasty": "明清", "coordinates": {"x": 650, "y": 300}, "width": 70, "height": 40, "description": "外朝东侧大殿，明代为太子讲学之处。清代为经筵讲学之所，后设文华殿大学士。", "significance": "太子讲学、经筵场所", "dimensions": {}, "color": "#d4a017"},
  "wuying-dian": {"id": "wuying-dian", "name": "武英殿", "aliases": [], "category": "外朝大殿", "built_year": 1420, "rebuilt_years": [1695], "dynasty": "明清", "coordinates": {"x": 350, "y": 300}, "width": 70, "height": 40, "description": "外朝西侧大殿，明代皇帝斋居之处。清代设为修书处，武英殿刻印书籍闻名。", "significance": "清代修书处、武英殿刻本", "dimensions": {}, "color": "#d4a017"},
  "qianqing-men": {"id": "qianqing-men", "name": "乾清门", "aliases": [], "category": "内廷门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 500, "y": 470}, "width": 80, "height": 30, "description": "内廷正门，清代御门听政改在此举行。", "significance": "内廷正门，御门听政", "dimensions": {}, "color": "#c0392b"},
  "jingren-gong": {"id": "jingren-gong", "name": "景仁宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 620, "y": 620}, "width": 55, "height": 35, "description": "东六宫之一。康熙帝出生于此。东西六宫建筑布局相同。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "chengqian-gong": {"id": "chengqian-gong", "name": "承乾宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 620, "y": 680}, "width": 55, "height": 35, "description": "东六宫之一。顺治帝董鄂妃居所。东西六宫建筑布局相同。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "zhongcui-gong": {"id": "zhongcui-gong", "name": "钟粹宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 620, "y": 740}, "width": 55, "height": 35, "description": "东六宫之一。清代后妃居所。东西六宫建筑布局相同。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "yonghe-gong": {"id": "yonghe-gong", "name": "永和宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 740, "y": 680}, "width": 55, "height": 35, "description": "东六宫之一。清代后妃居所。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "yikun-gong": {"id": "yikun-gong", "name": "翊坤宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 380, "y": 620}, "width": 55, "height": 35, "description": "西六宫之一。清代后妃居所。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "changchun-gong": {"id": "changchun-gong", "name": "长春宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 380, "y": 680}, "width": 55, "height": 35, "description": "西六宫之一。慈禧太后曾居于此，后迁储秀宫。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "xianfu-gong": {"id": "xianfu-gong", "name": "咸福宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 380, "y": 740}, "width": 55, "height": 35, "description": "西六宫之一。清代后妃居所，嘉庆、道光、咸丰守孝处。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "yongshou-gong": {"id": "yongshou-gong", "name": "永寿宫", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 260, "y": 620}, "width": 55, "height": 35, "description": "西六宫之一。清代后妃居所。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "taiji-dian": {"id": "taiji-dian", "name": "太极殿", "aliases": [], "category": "东西六宫", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 260, "y": 680}, "width": 55, "height": 35, "description": "西六宫之一，原名启祥宫。清代后妃居所。", "significance": "妃嫔居所", "dimensions": {}, "color": "#8e44ad"},
  "cining-gong": {"id": "cining-gong", "name": "慈宁宫", "aliases": [], "category": "附属宫殿", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 260, "y": 420}, "width": 60, "height": 40, "description": "太后居所。孝庄太后、慈安太后等曾居于此。", "significance": "皇家礼仪场所", "dimensions": {}, "color": "#c0392b"},
  "shoukang-gong": {"id": "shoukang-gong", "name": "寿康宫", "aliases": [], "category": "附属宫殿", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 260, "y": 480}, "width": 60, "height": 40, "description": "乾隆帝为生母崇庆皇太后所建。", "significance": "皇家礼仪场所", "dimensions": {}, "color": "#c0392b"},
  "ning-shougong": {"id": "ning-shougong", "name": "宁寿宫", "aliases": [], "category": "附属宫殿", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 740, "y": 400}, "width": 60, "height": 40, "description": "乾隆帝为退位后养老所建。珍妃井在此区域内。", "significance": "皇家礼仪场所", "dimensions": {}, "color": "#c0392b"},
  "fengxian-dian": {"id": "fengxian-dian", "name": "奉先殿", "aliases": [], "category": "附属宫殿", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 640, "y": 450}, "width": 60, "height": 40, "description": "皇家祭祀祖先之所。", "significance": "皇家礼仪场所", "dimensions": {}, "color": "#c0392b"},
  "chuanxindian": {"id": "chuanxindian", "name": "传心殿", "aliases": [], "category": "附属宫殿", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 680, "y": 260}, "width": 60, "height": 40, "description": "祭祀先师孔子之所。", "significance": "皇家礼仪场所", "dimensions": {}, "color": "#c0392b"},
  "yu-huayuan": {"id": "yu-huayuan", "name": "御花园", "aliases": [], "category": "园林建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 500, "y": 700}, "width": 120, "height": 60, "description": "紫禁城内最大的花园，位于坤宁宫后方。内有千秋亭、万春亭、钦安殿等。", "significance": "皇家御花园", "dimensions": {}, "color": "#27ae60"},
  "cining-huayuan": {"id": "cining-huayuan", "name": "慈宁宫花园", "aliases": [], "category": "园林建筑", "built_year": 1536, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 200, "y": 450}, "width": 60, "height": 50, "description": "慈宁宫西侧花园，太后太妃们游赏之处。", "significance": "太后花园", "dimensions": {}, "color": "#27ae60"},
  "ningshou-huayuan": {"id": "ningshou-huayuan", "name": "宁寿宫花园", "aliases": ["乾隆花园"], "category": "园林建筑", "built_year": 1771, "rebuilt_years": [], "dynasty": "清", "coordinates": {"x": 740, "y": 480}, "width": 60, "height": 80, "description": "又称乾隆花园，位于宁寿宫区域西北，是乾隆帝为自己退位后修建的花园。内有古华轩、遂初堂等。", "significance": "乾隆帝养老花园", "dimensions": {}, "color": "#27ae60"},
  "shenwu-men": {"id": "shenwu-men", "name": "神武门", "aliases": [], "category": "外朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 500, "y": 800}, "width": 70, "height": 30, "description": "紫禁城北门。原名玄武门，清代避康熙讳改名。", "significance": "宫城门禁", "dimensions": {}, "color": "#7f8c8d"},
  "donghua-men": {"id": "donghua-men", "name": "东华门", "aliases": [], "category": "外朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 820, "y": 450}, "width": 70, "height": 30, "description": "紫禁城东门。", "significance": "宫城门禁", "dimensions": {}, "color": "#7f8c8d"},
  "xihua-men": {"id": "xihua-men", "name": "西华门", "aliases": [], "category": "外朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 180, "y": 450}, "width": 70, "height": 30, "description": "紫禁城西门。", "significance": "宫城门禁", "dimensions": {}, "color": "#7f8c8d"},
  "wenhuadian-ge": {"id": "wenhuadian-ge", "name": "文渊阁", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 680, "y": 350}, "width": 45, "height": 30, "description": "乾隆年间修建，专藏《四库全书》。仿宁波天一阁建造。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "nansansuo": {"id": "nansansuo", "name": "南三所", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 660, "y": 520}, "width": 45, "height": 30, "description": "皇子居所，位于外朝东侧。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "chunhua-dian": {"id": "chunhua-dian", "name": "淳化轩", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 740, "y": 560}, "width": 45, "height": 30, "description": "宁寿宫区域内建筑。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "huangjidian": {"id": "huangjidian", "name": "皇极殿", "aliases": [], "category": "附属宫殿", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 740, "y": 440}, "width": 45, "height": 30, "description": "宁寿宫区正殿，乾隆退位后在此受贺。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "le-shoutang": {"id": "le-shoutang", "name": "乐寿堂", "aliases": [], "category": "附属宫殿", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 740, "y": 520}, "width": 45, "height": 30, "description": "宁寿宫区域建筑，慈禧太后曾居于此。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "yangxing-zhai": {"id": "yangxing-zhai", "name": "养性斋", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 600, "y": 720}, "width": 45, "height": 30, "description": "御花园西侧建筑。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "qianqiu-ting": {"id": "qianqiu-ting", "name": "千秋亭", "aliases": [], "category": "园林建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 460, "y": 720}, "width": 45, "height": 30, "description": "御花园内亭子，与万春亭对称。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "wanchun-ting": {"id": "wanchun-ting", "name": "万春亭", "aliases": [], "category": "园林建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 540, "y": 720}, "width": 45, "height": 30, "description": "御花园内亭子，与千秋亭对称。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "qinan-dian": {"id": "qinan-dian", "name": "钦安殿", "aliases": [], "category": "园林建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 500, "y": 760}, "width": 45, "height": 30, "description": "御花园正中，供奉玄武大帝。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "ciqiku": {"id": "ciqiku", "name": "瓷器库", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 200, "y": 350}, "width": 45, "height": 30, "description": "宫廷库房之一。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "duan-yi-men": {"id": "duan-yi-men", "name": "端仪门", "aliases": [], "category": "内廷门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 400, "y": 470}, "width": 45, "height": 30, "description": "乾清门广场侧门。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "jing-yun-men": {"id": "jing-yun-men", "name": "景运门", "aliases": [], "category": "内廷门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 600, "y": 470}, "width": 45, "height": 30, "description": "乾清门广场东侧门。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "hongyi-dian": {"id": "hongyi-dian", "name": "弘义阁", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 420, "y": 200}, "width": 40, "height": 30, "description": "太和殿广场西侧楼阁。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "tiyi-dian": {"id": "tiyi-dian", "name": "体仁阁", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 580, "y": 200}, "width": 40, "height": 30, "description": "太和殿广场东侧楼阁。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "zhaode-men": {"id": "zhaode-men", "name": "昭德门", "aliases": [], "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 580, "y": 180}, "width": 40, "height": 30, "description": "太和门广场侧门。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "zhendu-men": {"id": "zhendu-men", "name": "贞度门", "aliases": [], "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 420, "y": 180}, "width": 40, "height": 30, "description": "太和门广场侧门。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "xianhuamen": {"id": "xianhuamen", "name": "协和门", "aliases": [], "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 580, "y": 230}, "width": 40, "height": 30, "description": "前朝区域门。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "xiximen": {"id": "xiximen", "name": "熙和门", "aliases": [], "category": "前朝门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 420, "y": 230}, "width": 40, "height": 30, "description": "前朝区域门。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "cangku-fang": {"id": "cangku-fang", "name": "方略馆", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 350, "y": 350}, "width": 40, "height": 30, "description": "武英殿旁修书场所。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "wenyuan-dian": {"id": "wenyuan-dian", "name": "文渊殿", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 650, "y": 370}, "width": 40, "height": 30, "description": "文华殿后殿。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "zhushengfang": {"id": "zhushengfang", "name": "主善斋", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 260, "y": 540}, "width": 40, "height": 30, "description": "西六宫区域建筑。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "yifangzhai": {"id": "yifangzhai", "name": "怡芳斋", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 200, "y": 580}, "width": 40, "height": 30, "description": "西六宫区域建筑。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "daxue-shi": {"id": "daxue-shi", "name": "翰林院", "aliases": [], "category": "附属建筑", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 700, "y": 380}, "width": 40, "height": 30, "description": "文华殿附近，翰林办公处。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "yuyuan-dian": {"id": "yuyuan-dian", "name": "毓庆宫", "aliases": [], "category": "附属宫殿", "built_year": 1420, "rebuilt_years": [], "dynasty": "明清", "coordinates": {"x": 640, "y": 560}, "width": 40, "height": 30, "description": "同治、光绪读书处。", "significance": "宫廷建筑", "dimensions": {}, "color": "#7f8c8d"},
  "nei-wu-fu": {"id": "nei-wu-fu", "name": "内务府", "aliases": ["内务府"], "category": "服务", "built_year": 1420, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 200, "y": 600}, "width": 80, "height": 40, "description": "管理皇室内部事务的机构", "significance": "宫廷行政中心", "dimensions": {"width": 80, "height": 40}, "color": "#808080"},
  "zuoyi-men": {"id": "zuoyi-men", "name": "左翼门", "aliases": ["左翼门"], "category": "门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 450, "y": 550}, "width": 30, "height": 20, "description": "太和殿左侧门", "significance": "礼仪通道", "dimensions": {"width": 30, "height": 20}, "color": "#8B4513"},
  "youyi-men": {"id": "youyi-men", "name": "右翼门", "aliases": ["右翼门"], "category": "门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 550, "y": 550}, "width": 30, "height": 20, "description": "太和殿右侧门", "significance": "礼仪通道", "dimensions": {"width": 30, "height": 20}, "color": "#8B4513"},
  "wuying-men": {"id": "wuying-men", "name": "武英门", "aliases": ["武英门"], "category": "门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 150, "y": 300}, "width": 30, "height": 20, "description": "武英殿正门", "significance": "", "dimensions": {"width": 30, "height": 20}, "color": "#8B4513"},
  "wenhua-men": {"id": "wenhua-men", "name": "文华门", "aliases": ["文华门"], "category": "门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 750, "y": 300}, "width": 30, "height": 20, "description": "文华殿正门", "significance": "", "dimensions": {"width": 30, "height": 20}, "color": "#8B4513"},
  "jingyun-men": {"id": "jingyun-men", "name": "景运门", "aliases": ["景运门"], "category": "门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 600, "y": 500}, "width": 30, "height": 20, "description": "内廷东侧门", "significance": "", "dimensions": {"width": 30, "height": 20}, "color": "#8B4513"},
  "longzong-men": {"id": "longzong-men", "name": "隆宗门", "aliases": ["隆宗门"], "category": "门禁", "built_year": 1420, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 400, "y": 500}, "width": 30, "height": 20, "description": "内廷西侧门", "significance": "", "dimensions": {"width": 30, "height": 20}, "color": "#8B4513"},
  "ning-shou-gong": {"id": "ning-shou-gong", "name": "宁寿宫", "aliases": ["宁寿宫", "宁寿宫区"], "category": "内廷", "built_year": 1695, "rebuilt_years": [1771], "dynasty": "清", "coordinates": {"x": 700, "y": 650}, "width": 60, "height": 35, "description": "乾隆帝退位后居所", "significance": "太上皇宫殿", "dimensions": {"width": 60, "height": 35}, "color": "#B8860B"},
  "huang-ji-dian": {"id": "huang-ji-dian", "name": "皇极殿", "aliases": ["皇极殿"], "category": "内廷", "built_year": 1771, "rebuilt_years": [], "dynasty": "清", "coordinates": {"x": 700, "y": 600}, "width": 55, "height": 30, "description": "宁寿宫区主殿，乾隆禅位后受朝贺处", "significance": "禅位大典", "dimensions": {"width": 55, "height": 30}, "color": "#DAA520"},
  "ci-shou-gong": {"id": "ci-shou-gong", "name": "慈寿宫", "aliases": ["慈寿宫"], "category": "内廷", "built_year": 1536, "rebuilt_years": [], "dynasty": "明", "coordinates": {"x": 300, "y": 750}, "width": 45, "height": 25, "description": "太后居所之一", "significance": "", "dimensions": {"width": 45, "height": 25}, "color": "#CD853F"},
  "shang-shu-fang": {"id": "shang-shu-fang", "name": "尚书房", "aliases": ["尚书房", "上书房"], "category": "服务", "built_year": 1722, "rebuilt_years": [], "dynasty": "清", "coordinates": {"x": 550, "y": 450}, "width": 35, "height": 20, "description": "皇子皇孙读书之所", "significance": "皇家教育场所", "dimensions": {"width": 35, "height": 20}, "color": "#8B6914"},
  "ying-hua-dian": {"id": "ying-hua-dian", "name": "英华殿", "aliases": ["英华殿"], "category": "祭祀", "built_year": 1420, "rebuilt_years": [1597], "dynasty": "明", "coordinates": {"x": 350, "y": 400}, "width": 40, "height": 25, "description": "宫中佛殿，后妃礼佛之所", "significance": "", "dimensions": {"width": 40, "height": 25}, "color": "#CD853F"},
};

const EMPERORS = {
  "yongle": {
    "id": "yongle",
    "name": "明成祖朱棣",
    "era_name": "永乐",
    "dynasty": "明",
    "reign_start": 1402,
    "reign_end": 1424,
    "birth_year": 1360,
    "death_year": 1424,
    "father": "hongwu",
    "successor": "hongxi",
    "consort": "xurenhuanghou",
    "description": "明成祖，朱元璋第四子。通过靖难之役夺取皇位，迁都北京，修建紫禁城（1406-1420），派郑和下西洋，编《永乐大典》。",
    "achievements": [
      "修建故宫",
      "迁都北京",
      "郑和下西洋",
      "编纂永乐大典"
    ],
    "color": "#e67e22"
  },
  "jiajing": {
    "id": "jiajing",
    "name": "明世宗朱厚熜",
    "era_name": "嘉靖",
    "dynasty": "明",
    "reign_start": 1521,
    "reign_end": 1566,
    "birth_year": 1507,
    "death_year": 1566,
    "father": "xingxianwang",
    "successor": "longqing",
    "consort": "xiaojiehuan",
    "description": "明世宗，以藩王身份入继大统。前期励精图治，后期崇信道教，长期不上朝。严嵩专权，海瑞上疏。",
    "achievements": [
      "前期改革",
      "崇道修玄"
    ],
    "color": "#e67e22"
  },
  "wanli": {
    "id": "wanli",
    "name": "明神宗朱翊钧",
    "era_name": "万历",
    "dynasty": "明",
    "reign_start": 1572,
    "reign_end": 1620,
    "birth_year": 1563,
    "death_year": 1620,
    "father": "longqing",
    "successor": "taichang",
    "consort": "xiaoduanxian",
    "description": "明神宗，张居正辅政前十余年励精图治，张居正死后长期怠政，二十八年不上朝。",
    "achievements": [
      "万历三大征",
      "张居正改革(前期)"
    ],
    "color": "#e67e22"
  },
  "chongzhen": {
    "id": "chongzhen",
    "name": "明思宗朱由检",
    "era_name": "崇祯",
    "dynasty": "明",
    "reign_start": 1627,
    "reign_end": 1644,
    "birth_year": 1611,
    "death_year": 1644,
    "father": "taichang",
    "successor": null,
    "consort": "xiaojielie",
    "description": "明朝最后一位皇帝。即位后铲除魏忠贤，但内忧外患不断，李自成攻破北京后自缢于煤山（景山）。",
    "achievements": [
      "铲除阉党"
    ],
    "color": "#e67e22"
  },
  "kangxi": {
    "id": "kangxi",
    "name": "清圣祖玄烨",
    "era_name": "康熙",
    "dynasty": "清",
    "reign_start": 1661,
    "reign_end": 1722,
    "birth_year": 1654,
    "death_year": 1722,
    "father": "shunzhi",
    "successor": "yongzheng",
    "consort": "xiaochengren",
    "description": "清圣祖，中国历史上在位时间最长的皇帝（61年）。平定三藩、收复台湾、亲征噶尔丹、与沙俄签订尼布楚条约。晚年九子夺嫡。",
    "achievements": [
      "在位61年",
      "平定三藩",
      "收复台湾",
      "编康熙字典"
    ],
    "color": "#2980b9"
  },
  "yongzheng": {
    "id": "yongzheng",
    "name": "清世宗胤禛",
    "era_name": "雍正",
    "dynasty": "清",
    "reign_start": 1722,
    "reign_end": 1735,
    "birth_year": 1678,
    "death_year": 1735,
    "father": "kangxi",
    "successor": "qianlong",
    "consort": "xiaojingxian",
    "description": "清世宗，康熙第四子，九子夺嫡胜出。设立军机处，推行摊丁入亩、火耗归公等改革，勤政著称。",
    "achievements": [
      "设立军机处",
      "摊丁入亩",
      "火耗归公"
    ],
    "color": "#2980b9"
  },
  "qianlong": {
    "id": "qianlong",
    "name": "清高宗弘历",
    "era_name": "乾隆",
    "dynasty": "清",
    "reign_start": 1735,
    "reign_end": 1795,
    "birth_year": 1711,
    "death_year": 1799,
    "father": "yongzheng",
    "successor": "jiaqing",
    "consort": "xiaoxianchun",
    "description": "清高宗，中国历史上实际掌权时间最长的皇帝（63年）。前期十全武功，后期宠信和珅，闭关锁国。禅位后仍实际掌权。",
    "achievements": [
      "十全武功",
      "编四库全书",
      "在位60年(实际63年)"
    ],
    "color": "#2980b9"
  },
  "daoguang": {
    "id": "daoguang",
    "name": "清宣宗旻宁",
    "era_name": "道光",
    "dynasty": "清",
    "reign_start": 1820,
    "reign_end": 1850,
    "birth_year": 1782,
    "death_year": 1850,
    "father": "jiaqing",
    "successor": "xianfeng",
    "consort": "xiaoherui",
    "description": "清宣宗，节俭著称。鸦片战争爆发，中国开始沦为半殖民地半封建社会。",
    "achievements": [
      "节俭治国"
    ],
    "color": "#2980b9"
  },
  "guangxu": {
    "id": "guangxu",
    "name": "清德宗载湉",
    "era_name": "光绪",
    "dynasty": "清",
    "reign_start": 1875,
    "reign_end": 1908,
    "birth_year": 1871,
    "death_year": 1908,
    "father": "yixuan",
    "successor": "xuantong",
    "consort": "longyu",
    "description": "清德宗，四岁登基，慈禧太后垂帘听政。亲政后发动戊戌变法，被慈禧镇压后遭软禁于瀛台。",
    "achievements": [
      "戊戌变法"
    ],
    "color": "#2980b9"
  },
  "xuantong": {
    "id": "xuantong",
    "name": "清逊帝溥仪",
    "era_name": "宣统",
    "dynasty": "清",
    "reign_start": 1908,
    "reign_end": 1912,
    "birth_year": 1906,
    "death_year": 1967,
    "father": "zaifeng",
    "successor": null,
    "consort": "wanrong",
    "description": "清朝末代皇帝，三岁登基，六岁退位。中国历史上最后一位皇帝。退位后仍居内廷至1924年被冯玉祥驱逐出宫。",
    "achievements": [],
    "color": "#2980b9"
  }
};

const FIGURES = {
  "zhangju-zheng": {
    "id": "zhangju-zheng",
    "name": "张居正",
    "category": "大学士",
    "dynasty": "明",
    "birth_year": 1525,
    "death_year": 1582,
    "served_emperors": [
      "jiajing",
      "longqing",
      "wanli"
    ],
    "description": "明代政治家，万历初年内阁首辅。推行一条鞭法等改革，使明朝国力一度中兴。死后被万历清算。",
    "significance": "万历前期实际执政者，明代最重要改革家之一"
  },
  "yansong": {
    "id": "yansong",
    "name": "严嵩",
    "category": "大学士",
    "dynasty": "明",
    "birth_year": 1480,
    "death_year": 1567,
    "served_emperors": [
      "jiajing"
    ],
    "description": "嘉靖朝内阁首辅，专权二十余年，贪腐严重。最终被弹劾罢官，家产抄没。",
    "significance": "明代最大贪官之一"
  },
  "hai-rui": {
    "id": "hai-rui",
    "name": "海瑞",
    "category": "尚书侍郎",
    "dynasty": "明",
    "birth_year": 1514,
    "death_year": 1587,
    "served_emperors": [
      "jiajing",
      "longqing",
      "wanli"
    ],
    "description": "明代著名清官，以直言敢谏著称。上《治安疏》痛骂嘉靖帝，被誉为海青天。",
    "significance": "明代清廉典范"
  },
  "wei-zhongxian": {
    "id": "wei-zhongxian",
    "name": "魏忠贤",
    "category": "太监",
    "dynasty": "明",
    "birth_year": 1568,
    "death_year": 1627,
    "served_emperors": [
      "taichang",
      "chongzhen"
    ],
    "description": "明末大太监，天启朝专权，号称九千岁。崇祯即位后被铲除。",
    "significance": "明末最大权阉"
  },
  "zheng-he": {
    "id": "zheng-he",
    "name": "郑和",
    "category": "太监",
    "dynasty": "明",
    "birth_year": 1371,
    "death_year": 1433,
    "served_emperors": [
      "yongle"
    ],
    "description": "明代航海家，七下西洋，最远到达非洲东海岸。中国历史上最伟大的航海家。",
    "significance": "七下西洋，世界航海史先驱"
  },
  "yu-qian": {
    "id": "yu-qian",
    "name": "于谦",
    "category": "尚书侍郎",
    "dynasty": "明",
    "birth_year": 1398,
    "death_year": 1457,
    "served_emperors": [
      "zhengtong",
      "jingtai"
    ],
    "description": "明代名臣，土木堡之变后力主守京师，拥立景泰帝，保全明朝。后被英宗复辟杀害。",
    "significance": "北京保卫战功臣"
  },
  "zhangtingyu": {
    "id": "zhangtingyu",
    "name": "张廷玉",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1672,
    "death_year": 1755,
    "served_emperors": [
      "kangxi",
      "yongzheng",
      "qianlong"
    ],
    "description": "清代名臣，历事三朝，官至保和殿大学士。协助雍正创立军机处制度。",
    "significance": "清代三朝元老"
  },
  "he-shen": {
    "id": "he-shen",
    "name": "和珅",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1750,
    "death_year": 1799,
    "served_emperors": [
      "qianlong"
    ],
    "description": "乾隆朝宠臣，中国历史上最大贪官。嘉庆即位后赐死，抄家所得相当于清政府十余年财政收入。",
    "significance": "中国历史最大贪官"
  },
  "jixiaolan": {
    "id": "jixiaolan",
    "name": "纪昀（纪晓岚）",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1724,
    "death_year": 1805,
    "served_emperors": [
      "qianlong",
      "jiaqing"
    ],
    "description": "清代学者、文学家，总纂《四库全书》。以幽默机智著称，民间传说丰富。",
    "significance": "四库全书总纂官"
  },
  "lin-zexu": {
    "id": "lin-zexu",
    "name": "林则徐",
    "category": "尚书侍郎",
    "dynasty": "清",
    "birth_year": 1785,
    "death_year": 1850,
    "served_emperors": [
      "daoguang"
    ],
    "description": "清代名臣，主持虎门销烟，鸦片战争中被革职流放。近代中国开眼看世界第一人。",
    "significance": "虎门销烟，民族英雄"
  },
  "zuo-zongtang": {
    "id": "zuo-zongtang",
    "name": "左宗棠",
    "category": "将军",
    "dynasty": "清",
    "birth_year": 1812,
    "death_year": 1885,
    "served_emperors": [
      "daoguang",
      "xianfeng",
      "tongzhi",
      "guangxu"
    ],
    "description": "晚清名臣，收复新疆，洋务运动重要人物。",
    "significance": "收复新疆"
  },
  "li-hongzhang": {
    "id": "li-hongzhang",
    "name": "李鸿章",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1823,
    "death_year": 1901,
    "served_emperors": [
      "daoguang",
      "xianfeng",
      "tongzhi",
      "guangxu"
    ],
    "description": "晚清重臣，洋务运动领袖。代表清政府签订多个不平等条约，毁誉参半。",
    "significance": "洋务运动核心人物"
  },
  "cixi": {
    "id": "cixi",
    "name": "慈禧太后",
    "category": "皇后",
    "dynasty": "清",
    "birth_year": 1835,
    "death_year": 1908,
    "served_emperors": [
      "xianfeng",
      "tongzhi",
      "guangxu",
      "xuantong"
    ],
    "description": "咸丰帝懿贵妃，同治、光绪两朝实际最高统治者。垂帘听政近半个世纪，镇压戊戌变法。",
    "significance": "晚清实际统治者",
    "consort_of": "xianfeng"
  },
  "longyu": {
    "id": "longyu",
    "name": "隆裕太后",
    "category": "皇后",
    "dynasty": "清",
    "birth_year": 1868,
    "death_year": 1913,
    "served_emperors": [
      "guangxu",
      "xuantong"
    ],
    "description": "光绪帝皇后。宣统退位诏书的签署者，中国最后一位太后。",
    "significance": "签署清帝退位诏书",
    "consort_of": "guangxu"
  },
  "wanrong": {
    "id": "wanrong",
    "name": "婉容",
    "category": "皇后",
    "dynasty": "清",
    "birth_year": 1906,
    "death_year": 1946,
    "served_emperors": [
      "xuantong"
    ],
    "description": "溥仪皇后，中国最后一位皇后。命运悲惨，最终死于狱中。",
    "significance": "中国末代皇后",
    "consort_of": "xuantong"
  },
  "zhen-fei": {
    "id": "zhen-fei",
    "name": "珍妃",
    "category": "妃嫔",
    "dynasty": "清",
    "birth_year": 1876,
    "death_year": 1900,
    "served_emperors": [
      "guangxu"
    ],
    "description": "光绪帝宠妃，支持戊戌变法。八国联军攻入北京时被慈禧投入井中溺死。",
    "significance": "支持变法，被害殉难",
    "consort_of": "guangxu"
  },
  "ci-an": {
    "id": "ci-an",
    "name": "慈安太后",
    "category": "皇后",
    "dynasty": "清",
    "birth_year": 1837,
    "death_year": 1881,
    "served_emperors": [
      "xianfeng",
      "tongzhi",
      "guangxu"
    ],
    "description": "咸丰帝皇后，与慈禧共同垂帘听政。性情温和，后暴卒死因成谜。",
    "significance": "两宫垂帘之一",
    "consort_of": "xianfeng"
  },
  "eunuch-li-lianying": {
    "id": "eunuch-li-lianying",
    "name": "李莲英",
    "category": "太监",
    "dynasty": "清",
    "birth_year": 1848,
    "death_year": 1911,
    "served_emperors": [
      "xianfeng",
      "tongzhi",
      "guangxu",
      "xuantong"
    ],
    "description": "慈禧太后最信任的太监总管，侍奉慈禧近50年。清朝最有权势的太监之一。",
    "significance": "慈禧贴身太监"
  },
  "wu-sangui": {
    "id": "wu-sangui",
    "name": "吴三桂",
    "category": "将军",
    "dynasty": "明清",
    "birth_year": 1612,
    "death_year": 1678,
    "served_emperors": [
      "chongzhen",
      "kangxi"
    ],
    "description": "明末清初将领，引清兵入关。后反清发动三藩之乱，被康熙平定。",
    "significance": "引清入关，三藩之乱"
  },
  "nalan-xingde": {
    "id": "nalan-xingde",
    "name": "纳兰性德",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1655,
    "death_year": 1685,
    "served_emperors": [
      "kangxi"
    ],
    "description": "清代最著名词人之一，康熙御前侍卫。词风清新婉约，有'清代第一词人'之称。",
    "significance": "清代第一词人"
  },
  "caoxueqin": {
    "id": "caoxueqin",
    "name": "曹雪芹",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1715,
    "death_year": 1763,
    "served_emperors": [
      "kangxi",
      "yongzheng",
      "qianlong"
    ],
    "description": "《红楼梦》作者。曹家为江宁织造，雍正朝被抄家后家道中落。",
    "significance": "红楼梦作者"
  },
  "zeng-guofan": {
    "id": "zeng-guofan",
    "name": "曾国藩",
    "category": "将军",
    "dynasty": "清",
    "birth_year": 1811,
    "death_year": 1872,
    "served_emperors": [
      "daoguang",
      "xianfeng",
      "tongzhi"
    ],
    "description": "晚清名臣，创建湘军镇压太平天国，洋务运动发起人之一。",
    "significance": "湘军统帅，洋务运动发起者"
  },
  "kangyouwei": {
    "id": "kangyouwei",
    "name": "康有为",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1858,
    "death_year": 1927,
    "served_emperors": [
      "guangxu"
    ],
    "description": "戊戌变法领导人，联合公车上书，推动维新运动。变法失败后流亡海外。",
    "significance": "戊戌变法领导者"
  },
  "liangqichao": {
    "id": "liangqichao",
    "name": "梁启超",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1873,
    "death_year": 1929,
    "served_emperors": [
      "guangxu"
    ],
    "description": "戊戌变法重要人物，康有为学生。中国近代启蒙思想家，新文化运动先驱。",
    "significance": "近代启蒙思想家"
  },
  "yuan-shikai": {
    "id": "yuan-shikai",
    "name": "袁世凯",
    "category": "将军",
    "dynasty": "清",
    "birth_year": 1859,
    "death_year": 1916,
    "served_emperors": [
      "guangxu",
      "xuantong"
    ],
    "description": "晚清重臣，北洋新军创建者。逼迫溥仪退位后成为中华民国临时大总统，后称帝失败。",
    "significance": "逼迫清帝退位"
  },
  "sun-yatsen": {
    "id": "sun-yatsen",
    "name": "孙中山",
    "category": "将军",
    "dynasty": "清",
    "birth_year": 1866,
    "death_year": 1925,
    "served_emperors": [],
    "description": "辛亥革命领导人，中华民国国父。虽然未曾在故宫任职，但其领导的革命终结了清朝在故宫的统治。",
    "significance": "辛亥革命领导人"
  },
  "dorgon": {
    "id": "dorgon",
    "name": "多尔衮",
    "category": "大学士",
    "dynasty": "清",
    "birth_year": 1612,
    "death_year": 1650,
    "served_emperors": [
      "shunzhi"
    ],
    "description": "清初摄政王，率清军入关定鼎北京。顺治初年实际掌权者。",
    "significance": "清军入关实际指挥者"
  },
  "eunuch-wang-cheng-en": {
    "id": "eunuch-wang-cheng-en",
    "name": "王承恩",
    "category": "太监",
    "dynasty": "明",
    "birth_year": null,
    "death_year": 1644,
    "served_emperors": [
      "chongzhen"
    ],
    "description": "崇祯帝最信任的太监。李自成攻入北京时随崇祯帝自缢于煤山。",
    "significance": "随崇祯殉国"
  },
  "zhangju-zheng-rival": {
    "id": "gao-gong",
    "name": "高拱",
    "category": "大学士",
    "dynasty": "明",
    "birth_year": 1513,
    "death_year": 1578,
    "served_emperors": [
      "jiajing",
      "longqing",
      "wanli"
    ],
    "description": "隆庆朝内阁首辅，万历初年被张居正排挤出局。",
    "significance": "张居正政敌"
  },
  "eunuch-wei-zhongxian-rival": {
    "id": "yang-lian",
    "name": "杨涟",
    "category": "尚书侍郎",
    "dynasty": "明",
    "birth_year": 1572,
    "death_year": 1625,
    "served_emperors": [
      "wanli",
      "taichang",
      "tianqi"
    ],
    "description": "东林党领袖，上疏弹劾魏忠贤二十四大罪，被魏忠贤杀害。",
    "significance": "东林党领袖，反魏忠贤"
  }
};

const EVENTS = {
  "gugong-construction": {
    "id": "gugong-construction",
    "name": "修建紫禁城",
    "category": "修建工程",
    "start_year": 1406,
    "end_year": 1420,
    "locations": [
      "taihe-dian",
      "zhonghe-dian",
      "baohe-dian",
      "qianqing-gong",
      "kunning-gong"
    ],
    "participants": [
      "yongle"
    ],
    "description": "明成祖朱棣下令修建紫禁城，耗时14年，动用工匠10万、民夫100万。1420年建成，次年正式迁都北京。",
    "outcome": "紫禁城建成，明朝正式迁都北京"
  },
  "jingnan-zhiyi": {
    "id": "jingnan-zhiyi",
    "name": "靖难之役",
    "category": "政变",
    "start_year": 1399,
    "end_year": 1402,
    "locations": [],
    "participants": [
      "yongle"
    ],
    "description": "燕王朱棣以'靖难'为名起兵反叛建文帝，历时四年攻入南京，夺取皇位。",
    "outcome": "朱棣夺位成功，改元永乐"
  },
  "chongzhen-death": {
    "id": "chongzhen-death",
    "name": "崇祯帝自缢",
    "category": "逝世葬礼",
    "start_year": 1644,
    "end_year": 1644,
    "locations": [],
    "participants": [
      "chongzhen",
      "eunuch-wang-cheng-en"
    ],
    "description": "李自成攻破北京，崇祯帝在煤山（今景山）自缢，太监王承恩随行。明朝灭亡。",
    "outcome": "明朝灭亡"
  },
  "qing-enter-beijing": {
    "id": "qing-enter-beijing",
    "name": "清军入关定鼎北京",
    "category": "战争",
    "start_year": 1644,
    "end_year": 1644,
    "locations": [],
    "participants": [
      "dorgon",
      "wu-sangui"
    ],
    "description": "吴三桂引清兵入关，多尔衮率军击败李自成，清军进入北京并定都于此，故宫成为清朝皇宫。",
    "outcome": "清朝定都北京，故宫成为清皇宫"
  },
  "jiuzi-duodi": {
    "id": "jiuzi-duodi",
    "name": "九子夺嫡",
    "category": "政变",
    "start_year": 1708,
    "end_year": 1722,
    "locations": [
      "qianqing-gong",
      "yangxindian"
    ],
    "participants": [
      "kangxi",
      "yongzheng"
    ],
    "description": "康熙晚年诸皇子争夺储位，四阿哥胤禛（雍正）最终胜出即位。",
    "outcome": "胤禛即位为雍正帝"
  },
  "junjichu-established": {
    "id": "junjichu-established",
    "name": "军机处设立",
    "category": "朝会",
    "start_year": 1729,
    "end_year": 1729,
    "locations": [
      "junji-chu",
      "yangxindian"
    ],
    "participants": [
      "yongzheng",
      "zhangtingyu"
    ],
    "description": "雍正七年设立军机处，成为清代中后期最高权力机关，取代议政王大臣会议。",
    "outcome": "军机处成为清代实际最高决策机构"
  },
  "heshen-corruption": {
    "id": "heshen-corruption",
    "name": "和珅被抄家",
    "category": "政变",
    "start_year": 1799,
    "end_year": 1799,
    "locations": [],
    "participants": [
      "qianlong",
      "he-shen",
      "jixiaolan"
    ],
    "description": "乾隆驾崩后十五天，嘉庆帝宣布和珅二十大罪状，赐自尽。抄家所得相当于清政府十余年财政收入。",
    "outcome": "和珅被赐死，家产抄没"
  },
  "opium-war": {
    "id": "opium-war",
    "name": "虎门销烟与鸦片战争",
    "category": "战争",
    "start_year": 1839,
    "end_year": 1842,
    "locations": [],
    "participants": [
      "daoguang",
      "lin-zexu"
    ],
    "description": "林则徐虎门销烟后，英国发动鸦片战争。清军战败，签订南京条约，中国开始沦为半殖民地。",
    "outcome": "签订南京条约，割让香港"
  },
  "wuxu-bianfa": {
    "id": "wuxu-bianfa",
    "name": "戊戌变法",
    "category": "政变",
    "start_year": 1898,
    "end_year": 1898,
    "locations": [],
    "participants": [
      "guangxu",
      "kangyouwei",
      "liangqichao",
      "cixi"
    ],
    "description": "光绪帝支持康有为、梁启超发起维新变法，推行新政。慈禧太后发动戊戌政变，变法失败。",
    "outcome": "变法失败，光绪被软禁"
  },
  "zhenfei-death": {
    "id": "zhenfei-death",
    "name": "珍妃之死",
    "category": "逝世葬礼",
    "start_year": 1900,
    "end_year": 1900,
    "locations": [],
    "participants": [
      "zhen-fei",
      "cixi"
    ],
    "description": "八国联军攻入北京，慈禧太后仓皇出逃前，命太监将珍妃投入井中溺死。",
    "outcome": "珍妃遇害"
  },
  "abdication": {
    "id": "abdication",
    "name": "清帝退位",
    "category": "退位",
    "start_year": 1912,
    "end_year": 1912,
    "locations": [
      "yangxindian"
    ],
    "participants": [
      "xuantong",
      "longyu",
      "yuan-shikai"
    ],
    "description": "隆裕太后在养心殿签署《清帝退位诏书》，溥仪退位。清朝灭亡，中国两千多年帝制终结。",
    "outcome": "清帝退位，帝制终结"
  },
  "pu-yi-expelled": {
    "id": "pu-yi-expelled",
    "name": "溥仪被逐出宫",
    "category": "政变",
    "start_year": 1924,
    "end_year": 1924,
    "locations": [],
    "participants": [
      "xuantong"
    ],
    "description": "冯玉祥发动北京政变，派鹿钟麟率军进入故宫，限令溥仪三小时内离宫。溥仪从此告别紫禁城。",
    "outcome": "溥仪永远离开故宫"
  },
  "wancheng-dadian": {
    "id": "wancheng-dadian",
    "name": "编纂永乐大典",
    "category": "朝会",
    "start_year": 1403,
    "end_year": 1408,
    "locations": [],
    "participants": [
      "yongle"
    ],
    "description": "永乐帝命解缙等编纂《永乐大典》，全书22937卷，是中国古代最大的类书。",
    "outcome": "《永乐大典》编成"
  },
  "zhenghe-voyages": {
    "id": "zhenghe-voyages",
    "name": "郑和下西洋",
    "category": "朝会",
    "start_year": 1405,
    "end_year": 1433,
    "locations": [],
    "participants": [
      "yongle",
      "zheng-he"
    ],
    "description": "郑和七次率庞大船队远航，到达东南亚、南亚、阿拉伯半岛和非洲东海岸。",
    "outcome": "拓展海上丝绸之路，宣扬国威"
  },
  "siku-quanshu": {
    "id": "siku-quanshu",
    "name": "编纂四库全书",
    "category": "朝会",
    "start_year": 1773,
    "end_year": 1782,
    "locations": [],
    "participants": [
      "qianlong",
      "jixiaolan"
    ],
    "description": "乾隆帝命纪昀等总纂《四库全书》，收录图书3503种，是中国古代最大的丛书。",
    "outcome": "《四库全书》编成"
  }
};

const ALL_PERSONS = { ...EMPERORS, ...FIGURES };

const PALACE_RELATIONS = {
  "taihe-dian": {
    "persons": [
      {
        "id": "yongle",
        "name": "明成祖朱棣",
        "type": "执政于",
        "period": "1420-1424",
        "note": "太和殿建成后在此举行大典"
      }
    ],
    "events": [
      {
        "id": "gugong-construction",
        "name": "修建紫禁城",
        "year": 1406,
        "description": "明成祖朱棣下令修建紫禁城，耗时14年，动用工匠10万、民夫100万。1420年建成，次年正式迁都北京。"
      }
    ]
  },
  "zhonghe-dian": {
    "persons": [],
    "events": [
      {
        "id": "gugong-construction",
        "name": "修建紫禁城",
        "year": 1406,
        "description": "明成祖朱棣下令修建紫禁城，耗时14年，动用工匠10万、民夫100万。1420年建成，次年正式迁都北京。"
      }
    ]
  },
  "baohe-dian": {
    "persons": [],
    "events": [
      {
        "id": "gugong-construction",
        "name": "修建紫禁城",
        "year": 1406,
        "description": "明成祖朱棣下令修建紫禁城，耗时14年，动用工匠10万、民夫100万。1420年建成，次年正式迁都北京。"
      }
    ]
  },
  "qianqing-gong": {
    "persons": [
      {
        "id": "yongle",
        "name": "明成祖朱棣",
        "type": "执政于",
        "period": "1420-1424",
        "note": ""
      },
      {
        "id": "jiajing",
        "name": "明世宗朱厚熜",
        "type": "居住于",
        "period": "1521-1566",
        "note": ""
      },
      {
        "id": "wanli",
        "name": "明神宗朱翊钧",
        "type": "居住于",
        "period": "1572-1620",
        "note": ""
      },
      {
        "id": "chongzhen",
        "name": "明思宗朱由检",
        "type": "居住于",
        "period": "1627-1644",
        "note": ""
      },
      {
        "id": "kangxi",
        "name": "清圣祖玄烨",
        "type": "居住于",
        "period": "1662-1722",
        "note": ""
      }
    ],
    "events": [
      {
        "id": "gugong-construction",
        "name": "修建紫禁城",
        "year": 1406,
        "description": "明成祖朱棣下令修建紫禁城，耗时14年，动用工匠10万、民夫100万。1420年建成，次年正式迁都北京。"
      },
      {
        "id": "jiuzi-duodi",
        "name": "九子夺嫡",
        "year": 1708,
        "description": "康熙晚年诸皇子争夺储位，四阿哥胤禛（雍正）最终胜出即位。"
      }
    ]
  },
  "jiaotai-dian": {
    "persons": [],
    "events": []
  },
  "kunning-gong": {
    "persons": [],
    "events": [
      {
        "id": "gugong-construction",
        "name": "修建紫禁城",
        "year": 1406,
        "description": "明成祖朱棣下令修建紫禁城，耗时14年，动用工匠10万、民夫100万。1420年建成，次年正式迁都北京。"
      }
    ]
  },
  "yanxi-gong": {
    "persons": [
      {
        "id": "jiajing",
        "name": "明世宗朱厚熜",
        "type": "执政于",
        "period": "",
        "note": "后期在万寿宫修道"
      }
    ],
    "events": []
  },
  "chuxiu-gong": {
    "persons": [
      {
        "id": "cixi",
        "name": "慈禧太后",
        "type": "居住于",
        "period": "",
        "note": "储秀宫为其重要居所"
      }
    ],
    "events": []
  },
  "yangxindian": {
    "persons": [
      {
        "id": "kangxi",
        "name": "清圣祖玄烨",
        "type": "执政于",
        "period": "1662-1722",
        "note": ""
      },
      {
        "id": "yongzheng",
        "name": "清世宗胤禛",
        "type": "居住于",
        "period": "1722-1735",
        "note": ""
      },
      {
        "id": "qianlong",
        "name": "清高宗弘历",
        "type": "居住于",
        "period": "1735-1795",
        "note": ""
      },
      {
        "id": "daoguang",
        "name": "清宣宗旻宁",
        "type": "居住于",
        "period": "1820-1850",
        "note": ""
      },
      {
        "id": "guangxu",
        "name": "清德宗载湉",
        "type": "居住于",
        "period": "1875-1908",
        "note": ""
      },
      {
        "id": "xuantong",
        "name": "清逊帝溥仪",
        "type": "居住于",
        "period": "1908-1912",
        "note": ""
      },
      {
        "id": "cixi",
        "name": "慈禧太后",
        "type": "执政于",
        "period": "1861-1908",
        "note": "垂帘听政"
      },
      {
        "id": "ci-an",
        "name": "慈安太后",
        "type": "执政于",
        "period": "1861-1881",
        "note": "两宫垂帘"
      }
    ],
    "events": [
      {
        "id": "jiuzi-duodi",
        "name": "九子夺嫡",
        "year": 1708,
        "description": "康熙晚年诸皇子争夺储位，四阿哥胤禛（雍正）最终胜出即位。"
      },
      {
        "id": "junjichu-established",
        "name": "军机处设立",
        "year": 1729,
        "description": "雍正七年设立军机处，成为清代中后期最高权力机关，取代议政王大臣会议。"
      },
      {
        "id": "abdication",
        "name": "清帝退位",
        "year": 1912,
        "description": "隆裕太后在养心殿签署《清帝退位诏书》，溥仪退位。清朝灭亡，中国两千多年帝制终结。"
      }
    ]
  },
  "junji-chu": {
    "persons": [
      {
        "id": "yongzheng",
        "name": "清世宗胤禛",
        "type": "执政于",
        "period": "",
        "note": ""
      }
    ],
    "events": [
      {
        "id": "junjichu-established",
        "name": "军机处设立",
        "year": 1729,
        "description": "雍正七年设立军机处，成为清代中后期最高权力机关，取代议政王大臣会议。"
      }
    ]
  }
};

const PERSON_EVENTS = {
  "yongle": [
    {
      "name": "修建紫禁城",
      "year": 1406,
      "description": "明成祖朱棣下令修建紫禁城，耗时14年，动用工匠10万、民夫100万。1420年建成，次年正式迁都北京。"
    },
    {
      "name": "编纂永乐大典",
      "year": 1403,
      "description": "永乐帝命解缙等编纂《永乐大典》，全书22937卷，是中国古代最大的类书。"
    },
    {
      "name": "郑和下西洋",
      "year": 1405,
      "description": "郑和七次率庞大船队远航，到达东南亚、南亚、阿拉伯半岛和非洲东海岸。"
    },
    {
      "name": "靖难之役",
      "year": 1399,
      "description": "燕王朱棣以'靖难'为名起兵反叛建文帝，历时四年攻入南京，夺取皇位。"
    }
  ],
  "jiajing": [],
  "wanli": [],
  "chongzhen": [
    {
      "name": "崇祯帝自缢",
      "year": 1644,
      "description": "李自成攻破北京，崇祯帝在煤山（今景山）自缢，太监王承恩随行。明朝灭亡。"
    }
  ],
  "kangxi": [
    {
      "name": "九子夺嫡",
      "year": 1708,
      "description": "康熙晚年诸皇子争夺储位，四阿哥胤禛（雍正）最终胜出即位。"
    }
  ],
  "yongzheng": [
    {
      "name": "九子夺嫡",
      "year": 1708,
      "description": "康熙晚年诸皇子争夺储位，四阿哥胤禛（雍正）最终胜出即位。"
    },
    {
      "name": "军机处设立",
      "year": 1729,
      "description": "雍正七年设立军机处，成为清代中后期最高权力机关，取代议政王大臣会议。"
    }
  ],
  "qianlong": [
    {
      "name": "编纂四库全书",
      "year": 1773,
      "description": "乾隆帝命纪昀等总纂《四库全书》，收录图书3503种，是中国古代最大的丛书。"
    },
    {
      "name": "和珅被抄家",
      "year": 1799,
      "description": "乾隆驾崩后十五天，嘉庆帝宣布和珅二十大罪状，赐自尽。抄家所得相当于清政府十余年财政收入。"
    }
  ],
  "daoguang": [
    {
      "name": "虎门销烟与鸦片战争",
      "year": 1839,
      "description": "林则徐虎门销烟后，英国发动鸦片战争。清军战败，签订南京条约，中国开始沦为半殖民地。"
    }
  ],
  "guangxu": [
    {
      "name": "戊戌变法",
      "year": 1898,
      "description": "光绪帝支持康有为、梁启超发起维新变法，推行新政。慈禧太后发动戊戌政变，变法失败。"
    },
    {
      "name": "清帝退位",
      "year": 1912,
      "description": "隆裕太后在养心殿签署《清帝退位诏书》，溥仪退位。清朝灭亡，中国两千多年帝制终结。"
    }
  ],
  "xuantong": [
    {
      "name": "清帝退位",
      "year": 1912,
      "description": "隆裕太后在养心殿签署《清帝退位诏书》，溥仪退位。清朝灭亡，中国两千多年帝制终结。"
    },
    {
      "name": "溥仪被逐出宫",
      "year": 1924,
      "description": "冯玉祥发动北京政变，派鹿钟麟率军进入故宫，限令溥仪三小时内离宫。溥仪从此告别紫禁城。"
    }
  ],
  "zhangju-zheng": [],
  "yansong": [],
  "hai-rui": [],
  "wei-zhongxian": [],
  "zheng-he": [],
  "yu-qian": [],
  "zhangtingyu": [
    {
      "name": "军机处设立",
      "year": 1729,
      "description": "雍正七年设立军机处，成为清代中后期最高权力机关，取代议政王大臣会议。"
    }
  ],
  "he-shen": [
    {
      "name": "和珅被抄家",
      "year": 1799,
      "description": "乾隆驾崩后十五天，嘉庆帝宣布和珅二十大罪状，赐自尽。抄家所得相当于清政府十余年财政收入。"
    }
  ],
  "jixiaolan": [],
  "lin-zexu": [
    {
      "name": "虎门销烟与鸦片战争",
      "year": 1839,
      "description": "林则徐虎门销烟后，英国发动鸦片战争。清军战败，签订南京条约，中国开始沦为半殖民地。"
    }
  ],
  "zuo-zongtang": [],
  "li-hongzhang": [],
  "cixi": [
    {
      "name": "戊戌变法",
      "year": 1898,
      "description": "光绪帝支持康有为、梁启超发起维新变法，推行新政。慈禧太后发动戊戌政变，变法失败。"
    },
    {
      "name": "珍妃之死",
      "year": 1900,
      "description": "八国联军攻入北京，慈禧太后仓皇出逃前，命太监将珍妃投入井中溺死。"
    }
  ],
  "longyu": [
    {
      "name": "清帝退位",
      "year": 1912,
      "description": "隆裕太后在养心殿签署《清帝退位诏书》，溥仪退位。清朝灭亡，中国两千多年帝制终结。"
    }
  ],
  "wanrong": [],
  "zhen-fei": [
    {
      "name": "珍妃之死",
      "year": 1900,
      "description": "八国联军攻入北京，慈禧太后仓皇出逃前，命太监将珍妃投入井中溺死。"
    }
  ],
  "ci-an": [],
  "eunuch-li-lianying": [],
  "wu-sangui": [
    {
      "name": "清军入关定鼎北京",
      "year": 1644,
      "description": "吴三桂引清兵入关，多尔衮率军击败李自成，清军进入北京并定都于此，故宫成为清朝皇宫。"
    }
  ],
  "nalan-xingde": [],
  "caoxueqin": [],
  "zeng-guofan": [],
  "kangyouwei": [
    {
      "name": "戊戌变法",
      "year": 1898,
      "description": "光绪帝支持康有为、梁启超发起维新变法，推行新政。慈禧太后发动戊戌政变，变法失败。"
    }
  ],
  "liangqichao": [
    {
      "name": "戊戌变法",
      "year": 1898,
      "description": "光绪帝支持康有为、梁启超发起维新变法，推行新政。慈禧太后发动戊戌政变，变法失败。"
    }
  ],
  "yuan-shikai": [
    {
      "name": "清帝退位",
      "year": 1912,
      "description": "隆裕太后在养心殿签署《清帝退位诏书》，溥仪退位。清朝灭亡，中国两千多年帝制终结。"
    },
    {
      "name": "溥仪被逐出宫",
      "year": 1924,
      "description": "冯玉祥发动北京政变，派鹿钟麟率军进入故宫，限令溥仪三小时内离宫。溥仪从此告别紫禁城。"
    }
  ],
  "sun-yatsen": [
    {
      "name": "清帝退位",
      "year": 1912,
      "description": "隆裕太后在养心殿签署《清帝退位诏书》，溥仪退位。清朝灭亡，中国两千多年帝制终结。"
    }
  ],
  "dorgon": [
    {
      "name": "清军入关定鼎北京",
      "year": 1644,
      "description": "吴三桂引清兵入关，多尔衮率军击败李自成，清军进入北京并定都于此，故宫成为清朝皇宫。"
    }
  ],
  "eunuch-wang-cheng-en": [
    {
      "name": "崇祯帝自缢",
      "year": 1644,
      "description": "李自成攻破北京，崇祯帝在煤山（今景山）自缢，太监王承恩随行。明朝灭亡。"
    }
  ],
  "zhangju-zheng-rival": [],
  "eunuch-wei-zhongxian-rival": []
};