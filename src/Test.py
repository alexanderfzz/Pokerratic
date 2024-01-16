class Test:
    def change(self):
        setattr(self, 'foo', 'changed')

test = Test()
setattr(test, 'foo', 12345)
setattr(test, 'goo', 'ahgahgah')

a = 1
for i in range(4):
    print (a)
    a+=1