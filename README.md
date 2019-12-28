# Mine_Sweeper_AI

一个简单的自动扫雷AI (game_AI.py)

- 第一步：从当前窗口截图，MAGIC_NUMBER是游戏区域的坐标
- 第二步：利用OCR识别数字(load_observed_map.py)
- 第三步：迭代计算每个位置雷数量的期望值，点击期望最低的位置(cal_expectation.py)

两张截图是两次测试的结果

高级扫雷(16*30, 99个雷)大约耗时2分钟 主要是读图和OCR比较慢
当然扫雷并不能保证100%成功率
