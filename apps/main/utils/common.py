# --*--*--*--*--*--*- Create by bh at 2023/10/3 10:47 -*--*--*--*--*--*--


def contains(s, eles):
    for ele in eles:
        if ele in s:
            return True
    return False