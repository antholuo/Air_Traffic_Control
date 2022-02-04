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

def test2():
    # does not work
    while(
        if (a == True):
            i > 3
        else
            i >4
    ):
            print(i)
            i +=1