import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

slat_width = 0.7
slat_sep = 0.5
n_slats = 8
height = 36
width = 24
angle = 28

def triang(arr, angle):
    return np.tan(np.deg2rad(angle))*arr
def get_section_1():
    p1 = (0, 2 * height/3)
    # section 1

    slat_x_a = np.arange(0, n_slats*(slat_width+slat_sep), slat_width+slat_sep)
    slat_x_b = slat_x_a

    slat_y_a = np.zeros(n_slats)
    slat_y_b = np.zeros(n_slats) + p1[1] + triang(slat_x_a, angle)

    # section 2
    dummy_n_slats = n_slats *40
    dummy_slat_x_a = np.arange(0, dummy_n_slats*(slat_width+slat_sep), slat_width+slat_sep)
    dummy_slat_x_b = dummy_slat_x_a

    dummy_slat_y_a = np.zeros(dummy_n_slats)
    dummy_slat_y_b = np.zeros(dummy_n_slats) + p1[1] + triang(dummy_slat_x_a, angle)

    slope = np.tan(np.deg2rad(angle))

    # dummy_slat_x_c = np.clip(dummy_slat_x_b, 0, slat_x_a[-1])

    # delta_x is known based on the clipping we performed
    # calculate delta_y
    dummy_slat_x_c = dummy_slat_x_b
    dummy_slat_x_c = np.clip(dummy_slat_x_b, 0, slat_x_a[-1])
    delta_x = dummy_slat_x_b - dummy_slat_x_c
    delta_y = delta_x * slope + 0 # this zero is the canvas' leftmost coordinate
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

    # plt.figure()
    # for i in range(len(dummy_slat_x_c)):
    #     plt.plot([dummy_slat_x_c[i], dummy_slat_x_d[i]], [dummy_slat_y_c[i], dummy_slat_y_d[i]],c='k')
    # plt.gca().set_aspect("equal")
    # plt.savefig('test1.png')


    return slat_x_a, slat_x_b, dummy_slat_x_c, dummy_slat_x_d, slat_y_a, slat_y_b, dummy_slat_y_c, dummy_slat_y_d

def get_section_2():
    p3 = (0, height/2)
    # section 1
    incr = slat_width+slat_sep # increment
    x_start =n_slats * (slat_width+slat_sep) +incr# x start
    
    print(x_start,(width+x_start))

    slat_x_a = np.arange(x_start, x_start+incr*n_slats_section, incr)
    slat_x_b = slat_x_a
    slat_y_a = np.ones(n_slats_section)*height
    print(triang(slat_x_a, angle))
    slat_y_b = np.zeros(n_slats_section) + p3[1] + triang(slat_x_a, angle)

    # section 2
    slope = np.tan(np.deg2rad(angle))
    slat_x_b_1 = slat_x_b 
    slat_y_c = slope * slat_x_b_1 + slat_y_b

    return slat_x_a, slat_x_b, slat_y_a, slat_y_b, slat_y_c
def main():
    plt.figure(figsize=(10,20))

    # calculate lefthand side
    slat_x_a, slat_x_b,slat_x_c, slat_x_d, slat_y_a, slat_y_b, slat_y_c, slat_y_d = get_section_1()
    # plot lefthand side
    for i in range(len(slat_x_a)):
        plt.plot([slat_x_a[i], slat_x_b[i]], [slat_y_a[i], slat_y_b[i]],c='k')
    for i in range(len(slat_x_c)):
        plt.plot([slat_x_c[i], slat_x_d[i]], [slat_y_c[i], slat_y_d[i]],c='r')
    # rect = patches.Rectangle((n_slats*(slat_width+slat_sep)+.1, 0), width-n_slats*(slat_width+slat_sep)+.51, height, linewidth=1,
    #                       color = "white",zorder=2)
    # calculate middle
    # slat_x_a, slat_x_b, slat_y_a, slat_y_b, slat_y_c = get_section_2()
    # for i in range(n_slats_section):
    #     plt.plot([slat_x_a[i], slat_x_b[i]], [slat_y_a[i], slat_y_b[i]],c='orange',zorder =5)
        # plt.plot([slat_x_b[i], 0], [slat_y_b[i], slat_y_c[i]],c='o')
    # plot middle
    plt.ylim([0, height])
    plt.xlim([0, width])
    plt.gca().set_aspect("equal")
    # plt.gca().add_patch(rect)
    plt.savefig("test.png")
if __name__=="__main__":
    main()
