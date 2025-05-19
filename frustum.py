import glm

class Plane:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

class Frustum:
    def __init__(self, combo_matrix):
        self.near = None
        self.far = None
        self.bottom = None
        self.top = None
        self.left = None
        self.right = None
        self.update_planes(combo_matrix)

    def update_planes(self, combo_matrix):
        self.near = Plane(
            combo_matrix[0][2],
            combo_matrix[1][2],
            combo_matrix[2][2],
            combo_matrix[3][2]
        )
        self.far = Plane(
            combo_matrix[0][3] - combo_matrix[0][2],
            combo_matrix[1][3] - combo_matrix[1][2],
            combo_matrix[2][3] - combo_matrix[2][2],
            combo_matrix[3][3] - combo_matrix[3][2]
        )
        self.bottom = Plane(
            combo_matrix[0][3] + combo_matrix[0][1],
            combo_matrix[1][3] + combo_matrix[1][1],
            combo_matrix[2][3] + combo_matrix[2][1],
            combo_matrix[3][3] + combo_matrix[3][1]
        )
        self.top = Plane(
            combo_matrix[0][3] - combo_matrix[0][1],
            combo_matrix[1][3] - combo_matrix[1][1],
            combo_matrix[2][3] - combo_matrix[2][1],
            combo_matrix[3][3] - combo_matrix[3][1]
        )
        self.left = Plane(
            combo_matrix[0][3] + combo_matrix[0][0],
            combo_matrix[1][3] + combo_matrix[1][0],
            combo_matrix[2][3] + combo_matrix[2][0],
            combo_matrix[3][3] + combo_matrix[3][0]
        )
        self.right = Plane(
            combo_matrix[0][3] - combo_matrix[0][0],
            combo_matrix[1][3] - combo_matrix[1][0],
            combo_matrix[2][3] - combo_matrix[2][0],
            combo_matrix[3][3] - combo_matrix[3][0]
        )
        for plane in [self.near, self.far, self.bottom, self.top, self.left, self.right]:
            len = glm.length(glm.vec3(plane.a, plane.b, plane.c))
            plane.a /= len
            plane.b /= len
            plane.c /= len
            plane.d /= len

    def is_inside(self, bsphere):
        for plane in [self.near, self.far, self.bottom, self.top, self.left, self.right]:
            dist = glm.dot(glm.vec3(plane.a, plane.b, plane.c), bsphere.center) + plane.d
            if dist < -bsphere.radius:
                return False
        return True