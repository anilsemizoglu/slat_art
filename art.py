import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

slat_width = 0.7
slat_sep = 0.5
increment = slat_width+slat_sep

# bottom left coordinate

n_slats = 8
height = 36
width = 24
angle = 28
# transition point on the left panel
p1 = (0, 2 * height/3)
p4 = (n_slats*(increment)+p1[0]-increment, height/3)
p3 = (n_slats*(increment)+p1[0]-increment, 2*height/3)

def triang(arr, angle):
    return np.tan(np.deg2rad(angle))*arr
def get_section_1():
    # section 1
    slat_x_a = np.arange(p1[0], n_slats*(increment)+p1[0], increment)
    slat_x_b = slat_x_a

    slat_y_a = np.zeros(n_slats)
    slat_y_b = np.zeros(n_slats) + p1[1] + triang(slat_x_a, angle)

    # section 2
    dummy_n_slats = n_slats *40
    dummy_slat_x_a = np.arange(p1[0], dummy_n_slats*(increment), increment)
    dummy_slat_x_b = dummy_slat_x_a

    dummy_slat_y_a = np.zeros(dummy_n_slats)
    dummy_slat_y_b = np.zeros(dummy_n_slats) + p1[1] + triang(dummy_slat_x_a, angle)

    slope = np.tan(np.deg2rad(angle))

    # dummy_slat_x_c = np.clip(dummy_slat_x_b, 0, slat_x_a[-1])

    # delta_x is known based on the clipping we performed
    # calculate delta_y
    dummy_slat_x_c = dummy_slat_x_b
    dummy_slat_x_c = np.clip(dummy_slat_x_b, p1[0], slat_x_a[-1]-slat_width/2)
    delta_x = dummy_slat_x_b - dummy_slat_x_c
    delta_y = delta_x * slope + p1[0] # this zero is the canvas' leftmost coordinate
    dummy_slat_y_c = dummy_slat_y_b + delta_y
    
    # given point c, calculate point d using the slope
    # first calculate for x = 0, then calculate for y = max_height
    dummy_slat_x_d = np.zeros(len(dummy_slat_x_a))
    dummy_slat_y_d_ = dummy_slat_y_c + slope * dummy_slat_x_c

    # delta_y is known based on the clipping we performed
    dummy_slat_y_d = np.clip(dummy_slat_y_d_, 0, height)

    delta_y = dummy_slat_y_d_ - dummy_slat_y_d
    delta_x = delta_y / slope
    dummy_slat_x_d += delta_x

    idx_to_keep = np.where((dummy_slat_y_d<height+1) & (dummy_slat_y_c<height+1))[0]
    dummy_slat_x_c = dummy_slat_x_c[idx_to_keep]
    dummy_slat_x_d = dummy_slat_x_d[idx_to_keep]
    dummy_slat_y_c = dummy_slat_y_c[idx_to_keep]
    dummy_slat_y_d = dummy_slat_y_d[idx_to_keep]
    # extend the last vertical to the height

    slat_y_b[-1]=height


    return slat_x_a, slat_x_b, dummy_slat_x_c, dummy_slat_x_d, slat_y_a, slat_y_b, dummy_slat_y_c, dummy_slat_y_d

def get_section_2():
    # section 1 (bottom)

    slat_x_a = np.arange(n_slats*(increment)+p1[0], 2*n_slats*(increment)+p1[0], increment)
    # this one to calculate the y_b in the first section a->b
    dummy_slat_x_a_from_zero = np.arange(p1[0], n_slats*(increment)+p1[0], increment)
    # starting at zero

    slat_x_b = slat_x_a

    slat_y_a = np.zeros(n_slats)
    slat_y_b = np.zeros(n_slats) + p4[1] + triang(dummy_slat_x_a_from_zero, angle)

    # section 2
    dummy_n_slats = n_slats *40
    dummy_slat_x_a = np.arange(n_slats*(increment)+p1[0], dummy_n_slats*(increment)+p1[0]+n_slats*(increment)+p1[0], increment)
    dummy_slat_x_a_from_zero = np.arange(p1[0], dummy_n_slats*(increment)+p1[0], increment)
    dummy_slat_x_b = dummy_slat_x_a

    dummy_slat_y_a = np.zeros(dummy_n_slats)
    dummy_slat_y_b = np.zeros(dummy_n_slats) + p4[1] + triang(dummy_slat_x_a_from_zero, angle)

    slope = np.tan(np.deg2rad(angle))

    # dummy_slat_x_c = np.clip(dummy_slat_x_b, 0, slat_x_a[-1])


    dummy_slat_y_c = dummy_slat_y_b
    dummy_slat_x_c = dummy_slat_x_b

    dummy_slat_x_d = np.ones(len(dummy_slat_x_a))*p3[0]#np.clip(dummy_slat_x_c, p3[0], width)
    mx = slope*(p3[0]-dummy_slat_x_c)
    dummy_slat_y_d = dummy_slat_y_c-mx

    dummy_slat_x_c_ = np.clip(dummy_slat_x_c, 0,slat_x_a[-1])
    
    delta_x = dummy_slat_x_c - dummy_slat_x_c_
    dummy_slat_x_c = dummy_slat_x_c_
    delta_y = delta_x * slope
    dummy_slat_y_c += delta_y

    idx_to_keep = np.where( (dummy_slat_y_d < p3[1]+triang(dummy_slat_x_a, angle)+1) & 
                            (dummy_slat_y_c < p3[1]+triang(dummy_slat_x_a, angle)+1))[0]
    # idx_to_keep = np.where(dummy_slat_y_d>0)[0]
    dummy_slat_x_c = dummy_slat_x_c[idx_to_keep]
    dummy_slat_x_d = dummy_slat_x_d[idx_to_keep]
    dummy_slat_y_c = dummy_slat_y_c[idx_to_keep]
    dummy_slat_y_d = dummy_slat_y_d[idx_to_keep]
    # extend the last vertical to the height

    return slat_x_a, slat_x_b, dummy_slat_x_c, dummy_slat_x_d, slat_y_a, slat_y_b, dummy_slat_y_c, dummy_slat_y_d

def main():
    plt.figure(figsize=(10,20))

    # calculate lefthand side
    slat_x_a, slat_x_b,slat_x_c, slat_x_d, slat_y_a, slat_y_b, slat_y_c, slat_y_d = get_section_1()
    # plot lefthand side
    for i in range(len(slat_x_a)):
        plt.plot([slat_x_a[i], slat_x_b[i]], [slat_y_a[i], slat_y_b[i]],c='k')
    for i in range(len(slat_x_c)):
        plt.plot([slat_x_c[i], slat_x_d[i]], [slat_y_c[i], slat_y_d[i]],c='r')

    slat_x_a, slat_x_b,slat_x_c, slat_x_d, slat_y_a, slat_y_b, slat_y_c, slat_y_d = get_section_2()
    for i in range(len(slat_x_a)):
        plt.plot([slat_x_a[i], slat_x_b[i]], [slat_y_a[i], slat_y_b[i]],c='orange')
    for i in range(len(slat_x_c)):
        plt.plot([slat_x_c[i], slat_x_d[i]], [slat_y_c[i], slat_y_d[i]],c='g')
    plt.ylim([0, height])
    plt.xlim([0, width])
    ax = plt.gca()
    ax.set_aspect("equal")
    # ax.axis('off')
    # plt.gca().add_patch(rect)
    plt.savefig("test.png")
if __name__=="__main__":
    main()
