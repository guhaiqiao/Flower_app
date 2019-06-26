from fractions import Fraction

# 玫瑰花: Rose         满天星、紫罗兰、百合、蝴蝶兰
# 满天星：baby's breath 玫瑰花、康乃馨、郁金香、杜鹃花
# 康乃馨：Carnation    百合、向日葵、玫瑰花、满天星
# 百合：lily           玫瑰花、水仙花、康乃馨、郁金香
# 水仙花：Chinese Narsissus  百合
# 郁金香：tulip        满天星、紫罗兰、百合
# 蝴蝶花：iris
# 向日葵：sunflower
# 风信花：hyacinth
# 雏菊：marguerite, daisy
# 剑兰：gladiolus       百合、红玫瑰
# 杜鹃花：rhododendron 满天星
# 鸳鸯茉莉：broadleaf raintree
# 蝴蝶兰：moth orchid 玫瑰花
# 紫罗兰 wall flower

flower = {
    1: "玫瑰花",
    2: "满天星",
    3: "康乃馨",
    4: "百合",
    5: "水仙花",
    6: "郁金香",
    7: "蝴蝶花",
    8: "向日葵",
    9: "风信花",
    10: "雏菊",
    11: "剑兰",
    12: "杜鹃花",
    13: "鸳鸯茉莉",
    14: "蝴蝶兰",
    15: "紫罗兰"
}
total = 15
flower_price = {
    1: 10,
    2: 2,
    3: 7,
    4: 9,
    5: 9,
    6: 10,
    7: 10,
    8: 12,
    9: 7,
    10: 5,
    11: 7,
    12: 12,
    13: 9,
    14: 10,
    15: 9
}
match = [
    [1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
    [0, 1, 0.5, 0, 0, 0.5, 0, 0, 0, 0, 0, 0.5, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]


def auto_match(like: list, dislike: list, tp: int):
    methods = []
    for f in like:
        for i in range(0, total):
            if i == f - 1 and match[f - 1][i] != 0:
                money = flower_price.get(f)
                num = tp // money
                for j in range(-1, 2):
                    method = {}
                    method.update({flower.get(f): num + j})
                    method.update({'价格': money * (num + j)})
                    methods.append(method)

            elif match[f - 1][i] != 0 and i + 1 not in dislike:  # 可组成一个组合
                frac = str(Fraction(match[f - 1][i])).split('/')
                frac.append(1)
                money = flower_price.get(f) * int(
                    frac[0]) + flower_price.get(i + 1) * int(frac[1])
                num = tp // money
                for j in range(-1, 2):
                    method = {}
                    if (num + j) % 2 == 1 and (num + j) > 0:
                        method.update(
                            {flower.get(f): (num + j) * int(frac[0])})
                        method.update(
                            {flower.get(i + 1): (num + j) * int(frac[1])})
                        method.update({'价格': money * (num + j)})
                        methods.append(method)
                        # print(method, money * (num + j))
    return methods


if __name__ == '__main__':
    print(auto_match([1, 3], [4], 100))
