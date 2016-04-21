import ctypes
from math import tan
import numpy as np

def vec2(x, y): return np.array([x, y], dtype=np.float32)
def vec3(x, y, z): return np.array([x, y, z], dtype=np.float32)
def vec4(x, y, z, w): return np.array([x, y, z, w], dtype=np.float32)

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: return v
    return v/norm

def lookat(eye, target, up):
    zv = normalize(eye - target)
    xv = normalize(np.cross(up, zv))
    yv = np.cross(zv, xv)

    return np.array([
        [ xv[0], yv[0], zv[0], 0 ],
        [ xv[1], yv[1], zv[1], 0 ],
        [ xv[2], yv[2], zv[2], 0 ],
        [ -np.dot(xv, eye), -np.dot(yv, eye), -np.dot(zv, eye), 1 ] ], dtype=np.float32)

# A C++ implementation 
# http://www.3dgep.com/understanding-the-view-matrix/#Look_At_Camera
'''mat4 LookAtRH( vec3 eye, vec3 target, vec3 up )
{
    vec3 zaxis = normal(eye - target);    // The "forward" vector.
    vec3 xaxis = normal(cross(up, zaxis));// The "right" vector.
    vec3 yaxis = cross(zaxis, xaxis);     // The "up" vector.
 
    // Create a 4x4 view matrix from the right, up, forward and eye position vectors
    mat4 viewMatrix = {
        vec4(      xaxis.x,            yaxis.x,            zaxis.x,       0 ),
        vec4(      xaxis.y,            yaxis.y,            zaxis.y,       0 ),
        vec4(      xaxis.z,            yaxis.z,            zaxis.z,       0 ),
        vec4(-dot( xaxis, eye ), -dot( yaxis, eye ), -dot( zaxis, eye ),  1 )
    };
     
    return viewMatrix;
}'''

def perspective(angle, near, far):
    s = 1 / tan(angle / 2 * np.pi / 180)
    M = np.diag([s, s, - float(far + near) / float(far - near), 0])
    M[2][3] = -1; M[3][2] = - 2 * far * near / float(far - near)
    return M.astype(np.float32)
