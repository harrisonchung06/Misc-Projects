import random
import argparse
 
parser = argparse.ArgumentParser(description = "An addition program")
 
parser.add_argument("add", nargs = '*', metavar = "num", type = int, 
                     help = "All the numbers separated by spaces will be added.")
 
args = parser.parse_args()
c = 0
if len(args.add) != 0:
    for i in range(50):
        if(args.add[i] == 12):
            c+=1
print(c)

#for i in range(50):
#    print(random.randint(1,6))

