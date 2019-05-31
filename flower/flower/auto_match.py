from fractions import Fraction

flower_price = {"rose": 10, "carnation": 10}
# 玫瑰花:Rose         满天星、紫罗兰、百合
# 满天星：baby's breath
# 桂花：Sweet Osmanthus 
# 康乃馨：Carnation 
# 百合：lily 
# 水仙花：Chinese Narsissus 
# 荷花：Hindu Lotus 
# 莲花：Hindu Lotus 
# 郁金香：tulip  
# 凤仙花： balsam 
# 美人蕉：canna 
# 向日葵：sunflower 
# 大竺葵：geranium 
# 牵牛花：morning-glory 
# 大波斯菊：cosmos  
# 三色堇：pansy
# 蝴蝶花：iris 
# 风信花：hyacinth   
# 雏菊：marguerite, daisy 
# 剑兰：gladiolus 
# 龙舌兰：cantury plant
# 杜鹃花：rhododendron
# 鸳鸯茉莉：broadleaf raintree
# 蝴蝶兰：moth orchid
# 石斛：dendrobium
# 紫罗兰 wall flower
total = 6
flower = {1: 10, 2: 5, 3: 7, 4: 6, 5: 9, 6: 15}
match = [
    # 1  2  3  4     5  6
     [0, 1, 2, 0.25, 0, 1],  # 1
     [0, 0, 0, 1, 0, 1],  # 2
     [0, 1, 0, 1, 0, 1],  # 3
     [0, 1, 0, 0, 0, 1],  # 4
     [0, 1, 0, 1, 0, 1],  # 5
     [0, 1, 0, 1, 0, 0]  # 6
]
# 假定1和2，3和4，5和6搭配


def auto_match(like: list, dislike: list, tp: int):
    methods = []
    for f in like:
        for i in range(0, total):
            if match[f - 1][i] != 0 and i + 1 not in dislike:  # 可组成一个组合
                frac = str(Fraction(match[f - 1][i])).split('/')
                frac.append(1)
                money = flower.get(f) * int(frac[0]) + flower.get(i + 1) * int(frac[1])
                num = tp // money
                for j in range(-1, 2):
                    method = {}
                    if (num + j) % 2 == 1 and (num + j) > 0:
                        method.update({f: (num + j) * int(frac[0])})
                        method.update({i + 1: (num + j) * int(frac[1])})
                        methods.append(method)
                        print(method, money * (num + j))
    return methods


print(auto_match([1, 3], [4], 100))
