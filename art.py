import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

slat_width = 0.7
slat_sep = 0.5
increment = slat_width+slat_sep

# bottom left coordinate

n_slats = 8
height = 36
width = 28
ANGLE = 28
# transition point on the left panel
p1 = (0, 2 * height/3)
p4 = (n_slats*(increment)+p1[0]-increment, height/3)
p3 = (2*n_slats*(increment)+p1[0]-increment, 2*height/3)

def triang(arr, angle):
    return np.tan(np.deg2rad(angle))*arr

def get_section_1(angle):
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

def get_section_2(angle):
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

    dummy_slat_x_d = np.ones(len(dummy_slat_x_a))*p4[0]#np.clip(dummy_slat_x_c, p3[0], width)
    mx = slope*(p4[0]-dummy_slat_x_c)
    dummy_slat_y_d = dummy_slat_y_c-mx

    dummy_slat_x_c_ = np.clip(dummy_slat_x_c, 0,slat_x_a[-1]+increment/2)
    
    delta_x = dummy_slat_x_c - dummy_slat_x_c_
    dummy_slat_x_c = dummy_slat_x_c_
    delta_y = delta_x * slope
    dummy_slat_y_c += delta_y

    # idx_to_keep = np.where( (dummy_slat_y_d < p3[1]+triang(dummy_slat_x_a, angle)+1) & 
    #                         (dummy_slat_y_c < p3[1]+triang(dummy_slat_x_a, angle)+1))[0]
    
    # extend the last vertical to the height
    start = 8
    xs = [dummy_slat_x_d[start], dummy_slat_x_c[12]]
    ys = [dummy_slat_y_d[start], dummy_slat_y_d[12]]
    a1 = np.array([xs[0], ys[0]])
    a2 = np.array([xs[1], ys[1]])
    for i in range(start,len(dummy_slat_y_d)):
        b1 = np.array([dummy_slat_x_c[i], dummy_slat_y_c[i]])
        b2 = np.array([dummy_slat_x_d[i], dummy_slat_y_d[i]])
        intersect = seg_intersect(a1, a2, b1, b2)
        dummy_slat_x_d[i], dummy_slat_y_d[i] = intersect[0], intersect[1]
    idx_to_keep = np.where((dummy_slat_x_c < 2*n_slats*(increment)+p1[0]) & 
                            (dummy_slat_x_d < 2*n_slats*(increment)+p1[0]))[0]
    dummy_slat_x_c = dummy_slat_x_c[idx_to_keep]
    dummy_slat_x_d = dummy_slat_x_d[idx_to_keep]
    dummy_slat_y_c = dummy_slat_y_c[idx_to_keep]
    dummy_slat_y_d = dummy_slat_y_d[idx_to_keep]

    slat_x_e, slat_x_f = dummy_slat_x_d, dummy_slat_x_d
    slat_y_e = dummy_slat_y_d
    slat_y_f = np.ones(len(slat_y_e))*height
    
    return slat_x_a, slat_x_b, dummy_slat_x_c, dummy_slat_x_d, slat_x_e, slat_x_f, slat_y_a, slat_y_b, dummy_slat_y_c, dummy_slat_y_d, slat_y_e, slat_y_f, xs, ys

def mirror_coordinates(xs, ys, axis = "y", mirror_value = 0.0):
    if axis == "y":
        return -(xs - mirror_value)+mirror_value , ys 
        

def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    return (num / denom.astype(float))*db + b1
def main():
    plt.figure(figsize=(10,20))

    # calculate lefthand side
    slat_x_a, slat_x_b,slat_x_c, slat_x_d, slat_y_a, slat_y_b, slat_y_c, slat_y_d = get_section_1(ANGLE)
    # plot lefthand side
    for i in range(len(slat_x_a)):
        plt.plot([slat_x_a[i], slat_x_b[i]], [slat_y_a[i], slat_y_b[i]],c='k',zorder=5)
    for i in range(len(slat_x_c)):
        plt.plot([slat_x_c[i], slat_x_d[i]], [slat_y_c[i], slat_y_d[i]],c='r')

    slat_x_a, slat_x_b,slat_x_c, slat_x_d,slat_x_e,slat_x_f, slat_y_a, slat_y_b, slat_y_c, slat_y_d, slat_y_e, slat_y_f, xs, ys = get_section_2(ANGLE)
    for i in range(len(slat_x_a)):
        plt.plot([slat_x_a[i], slat_x_b[i]], [slat_y_a[i], slat_y_b[i]],c='orange')
    for i in range(len(slat_x_c)):
        plt.plot([slat_x_c[i], slat_x_d[i]], [slat_y_c[i], slat_y_d[i]],c='g')
    for i in range(len(slat_x_e)):
        plt.plot([slat_x_e[i], slat_x_f[i]], [slat_y_e[i], slat_y_f[i]],c='orange')

    slat_x_a,slat_y_a = mirror_coordinates(slat_x_a, slat_y_a, "y", p3[0]+increment/2)
    slat_x_b,slat_y_b = mirror_coordinates(slat_x_b, slat_y_b, "y", p3[0]+increment/2)
    slat_x_c,slat_y_c = mirror_coordinates(slat_x_c, slat_y_c, "y", p3[0]+increment/2)
    slat_x_d,slat_y_d = mirror_coordinates(slat_x_d, slat_y_d, "y", p3[0]+increment/2)
    slat_x_e,slat_y_e = mirror_coordinates(slat_x_e, slat_y_e, "y", p3[0]+increment/2)
    slat_x_f,slat_y_f = mirror_coordinates(slat_x_f, slat_y_f, "y", p3[0]+increment/2)
    print(p3[0])
    for i in range(len(slat_x_a)):
        plt.plot([slat_x_a[i], slat_x_b[i]], [slat_y_a[i], slat_y_b[i]],c='k')
    for i in range(len(slat_x_c)):
        plt.plot([slat_x_c[i], slat_x_d[i]], [slat_y_c[i], slat_y_d[i]],c='r')
    for i in range(len(slat_x_e)):
        plt.plot([slat_x_e[i], slat_x_f[i]], [slat_y_e[i], slat_y_f[i]],c='magenta')
    plt.ylim([0, height])
    plt.xlim([0, width])
    ax = plt.gca()
    ax.set_aspect("equal")
    ax.axis('off')
    plt.savefig("test.png")
if __name__=="__main__":
    main()
