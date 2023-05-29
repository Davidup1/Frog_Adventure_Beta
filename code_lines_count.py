from os import listdir


def count_lines(path,layer=0):
    result = {}
    counts = 0
    for filename in listdir(path):
        temp = filename.split('.')
        count = 0
        if len(temp) == 1:
            if temp[0] not in ["data","font","image"]:
                res = count_lines(path+'/'+temp[0],layer+1)
                result[temp[0]] = res
                count = res[1]
        elif temp[1] == 'py':
            count = len(open(path + '/' + filename,'r',encoding='utf-8').readlines())
            result[temp[0]] = count
        counts += count
    return result,counts


res,count = count_lines('./')
print(res)
print(count)
