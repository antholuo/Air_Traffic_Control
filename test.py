def test1():
    class myclass:
        def __init__(self, val):
            self.val = val

    mylist = []
    myclass1 = myclass(1)
    for i in range(0, 10):
        tempclass = myclass(i)
        mylist.append(tempclass)
        myclass1 = tempclass

    for objekt in mylist:
        print(objekt.val)
