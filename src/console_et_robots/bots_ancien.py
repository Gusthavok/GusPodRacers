from math import sqrt, atan, pi
from console_et_robots.ancien_code import decision

global premier_t, dep, l_cp, old_x, old_y
premier_t = True
dep = True
l_cp = []
old_x = 0
old_y = 0

def normalized(ang):
    return (int(ang+180)%360 - 180) # RMQ peut renvoyer -180 au lieu de +180, pas grave. 

def angle(vectx,vecty):
    if vectx == 0:
        if vecty>0:
            return 90
        else: #comprend le cas du vecteur (0,0)
            return -90
    elif vectx >0:
        return atan(vecty/vectx)*180/pi
    else:
        return normalized(180+atan(vecty/vectx)*180/pi)

def reponse_ancien_bot(_a, pod_a, pod_b, _b, _c, _d, _e, carte, show=False):
    global premier_t, dep, l_cp, old_x, old_y
    # INPUTS premier_tour, x, y, old_x, old_y, depart, liste_checkpoint, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle
    # OUTPUTS x_dir, y_dir, int(v_calc), premier_tour, depart, liste_checkpoint
    nextcpxa, nextcpya = carte[pod_a[1]]
    x, y = pod_a[2], pod_a[3]
    dist = sqrt((nextcpxa-x)**2+(nextcpya-y)**2)
    next_cp_angle = pod_a[6] - angle(nextcpxa-x, nextcpya-y)
    x_dir, y_dir, v_calc, premier_t, dep, l_cp, old_x, old_y = decision(premier_t, pod_a[2], pod_b[3], old_x, old_y, dep, l_cp, nextcpxa, nextcpya, dist, next_cp_angle)
    #C:\Users\augus_zcrxu\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts
    return ((x_dir, y_dir, v_calc),(0, 0, 0))