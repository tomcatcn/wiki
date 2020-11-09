from django.test import TestCase

# Create your tests here.
# s = [
#     {'id':1,'p_id':0},
#     {'id':5,'p_id':2},
#     {'id':9,'p_id':1},
#     {'id':2,'p_id':0},
#     {'id':10,'p_id':1},
#     {'id':15,'p_id':2},
#      ]

def fun2(s,d):

    del s[d['id']]
    return s

def fun1(s,l):

    d = {}
    key = -1
    for i in s:
        key += 1
        if i['p_id'] == 0:
            d['id'] = i['id']

            break
    d['childen'] = []
    if not d['id']:
        return
    for i in s:
        if i['p_id'] == d['id']:
            dd = {}
            dd['id'] = i['id']
            d['childen'].append(dd)

    l.append(d)
    s.pop(key)
    fun1(s,l)



if __name__ == '__main__':
    s = [
        {'id': 1, 'p_id': 0},
        {'id': 5, 'p_id': 2},
        {'id': 9, 'p_id': 1},
        {'id': 2, 'p_id': 0},
        {'id': 10, 'p_id': 1},
        {'id': 15, 'p_id': 2},
        {'id': 17, 'p_id': 0},
        {'id': 13, 'p_id': 17},
        {'id': 58, 'p_id': 17},

    ]
    l = []
    try:
       fun1(s,l)
    except:
        print(l)


