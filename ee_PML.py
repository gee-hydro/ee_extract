def cal_ETsum(img):
    r = img.expression("b('Ec') + b('Es') + b('Ei')").rename("ET")
    return r.copyProperties(img, img.propertyNames())
