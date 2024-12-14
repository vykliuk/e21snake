#global variables
apple = (2, 5) #default value
head = (4,3)
tail = [(4, 1), (4,2)]

def eat_apple():
    tail_arr.append(head)
    head = apple
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    apple = (x,y)
    while apple in tail_arr or apple == head:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        apple = (x,y)
