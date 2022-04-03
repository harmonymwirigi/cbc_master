from random import randint

faces = 6
eventb_boolean = False
eventc_boolean = False
# variable to count the number of 1/6 in simulation
counteventA = 0
# variable to count the number of 6 sixes in simulation
counteventB = 0
# variable to count the number of 3 sixes in simulation
counteventC = 0

# fucntion to check wether 1/6 occurs
def eventa():
    eventa_boolean = False
    # the number of dices rolled are 10 this for loop represents the number of dices
    for l in range(10):
        # declare any of the six faces can occur
        face = randint(1,6)
        if face == 1:
            eventa_boolean = True
    if eventa_boolean:
        return True
    else:
        return False

# fucntion to check wether 6 sixes occurs
def eventb():
    # variable to count the number sixes when all the 12 dices are rooled
    count = 0
    #     the number of dices rolled
    for k in range(12):
    # faces
        face = randint(1,6)
        if face == 6:
            count = count + 1
    if count >= 6:
        return True
    else:
        return False

# fucntion to check wether 3 sixes occurs
def eventc():
    # variable to count the number of sixes
    count = 0
    for i in range(18):
        face = randint(1,6)
        if face == 6:
            count = count + 1
    if count >= 3:
        return True
    else:
        return False

# simulation
for i in range(1000):
    if eventa():
        counteventA = counteventA + 1
    prob1 = counteventA/1000
    if eventb():
        counteventB = counteventB + 1
    prob2 = counteventB/1000
    if eventc():
        counteventC = counteventC + 1
    prob3 = counteventC/1000
print("the probability of event a is ", prob1)
print("the probability of event b is: ", prob2)
print("the probability of event c is: ", prob3)

def more_likely(num1, num2, num3):
    if (num1 > num2) and (num1 > num3):
        largest_num = num1
    elif (num2 > num1) and (num2 > num3):
        largest_num = num2
    else:
        largest_num = num3
    return  largest_num

answer = more_likely(prob1,prob2,prob3)
if prob1 == answer:
    print("envent A is more likely")
if prob2 == answer:
    print("event B is more likely")
if prob3 == answer:
    print("event C is more likely")

