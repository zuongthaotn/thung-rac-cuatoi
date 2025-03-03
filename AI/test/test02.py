import numpy as np

def get_degree_three_points(p, p1, p2):
    v1 = np.array([p1.x - p.x, p1.y - p.y])
    v2 = np.array([p2.x - p.x, p2.y - p.y])
    unit_v1 = v1 / np.linalg.norm(v1)
    unit_v2 = v2 / np.linalg.norm(v2)
    dot_product = np.dot(unit_v1, unit_v2)
    angle = np.math.atan2(np.linalg.det([unit_v1, unit_v2]), dot_product)
    degree = np.round(np.degrees(angle), 2)
    return degree if degree > 0 else degree + 360


import math


def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


# print(getAngle((5, 0), (0, 0), (0, 5)))
# print(abs(180-getAngle((0, 5), (0, 0), (5, 0))))


# print(abs(getAngle((2, 13.48), (0, 13.83), (2, 13.89))))
# print(abs(180-getAngle((2, 13.48), (0, 13.83), (2, 13.89))))


# a = np.array([2, 13.48])
# b = np.array([0, 13.83])
# c = np.array([2, 13.89])
#
# ba = a - b
# bc = c - b
#
# cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
# angle = np.arccos(cosine_angle)
#
# print(np.degrees(angle))

import matplotlib.pyplot as plt
plt.plot(2, 13.89, 'go')
plt.plot(0, 13.83, 'ro')
plt.plot(2, 13.48, 'yo')
plt.plot([2, 0, 2],[13.89, 13.83, 13.48])
plt.plot([5, 0, 0],[0, 0, 5])
plt.show()

# a = np.array([1, 2, 3, 4, 5])
# # plt.plot(a, 'go')
# print(a)
# plt.show()