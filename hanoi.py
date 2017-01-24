#汉若塔
def hanoi(layer,pi_x,pi_y,pi_z,count):

    if layer == 1:
        count +=1
        print("第%s次，%s柱-->%s柱"%((count),pi_x,pi_z))
    else:
        hanoi(layer-1,pi_x,pi_z,pi_y,count)
        count +=1
        print("第%s次，%s柱-->%s柱"%((1+count),pi_x,pi_z))
        hanoi(layer-1,pi_y,pi_x,pi_z,count)
        return count

hanoi(2,'A','B','C',count=0)