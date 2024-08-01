import display as dp
import projbar as pb

#========================================================
# Computes the projected barcode in the example
# undistinguishable by the fibered barcode
# see https://arxiv.org/abs/2206.08818
#========================================================

bd = [
[0, (0,1), []],
[0, (1,0), []],
[0, (1,1), []],
[-1, (1,1), [0,1]]
]

bd2 = [
[0, (0,1), []],
[0, (1,0), []]
]


bar0, bar1 = pb.pb_pp(bd, [0.5, 0.5], infinite_bar= True)
print("H0")
for x in bar0 : print(x)
print("H1")
for x in bar1 : print(x)

print("=====")


bar0, bar1 = pb.pb_pp(bd2, [0.5, 0.5], infinite_bar= True)
print("H0")
for x in bar0 : print(x)
print("H1")
for x in bar1 : print(x)

dp.display(bd2, infinite_bar = True)
