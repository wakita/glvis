import numpy as np

from transforms3d import affines as a
#from transforms3d import taitbryan as tb
#from transforms3d import quaternions as q
from transforms3d import _gohlketransforms as t

def vec(*args): return np.array(args, dtype=np.float32)
def vec2(x, y): return np.array([x, y], dtype=np.float32)
def vec3(x, y, z): return np.array([x, y, z], dtype=np.float32)
def vec4(x, y, z, w): return np.array([x, y, z, w], dtype=np.float32)

NoTranslation = [0, 0, 0]
NoRotation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
NoZoom = [1, 1, 1]

def comp(T=NoTranslation, R=NoRotation, Z=NoZoom): return a.compose(T, R, Z)

identity = t.identity_matrix

cat = t.concatenate_matrices

def scale(*xyz): return comp(Z=xyz)

def rotate(*args): return t.rotation_matrix(*args)

shear = t.shear_matrix

def translate(*xyz): return comp(T=xyz)

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: return v
    return v/norm

def mat4x4(m00, m01, m02, m03, m10, m11, m12, m13,
        m20, m21, m22, m23, m30, m31, m32, m33):
    return np.array([m00, m01, m02, m03, m10, m11, m12, m13,
        m20, m21, m22, m23, m30, m31, m32, m33], dtype=np.float32).reshape((4, 4))

def ortho(left, right, bottom, top, zNear=-1, zFar=1):
    rl, tb, fn = right - left, top - bottom, zFar - zNear
    return mat4x4(
            2/rl, 0, 0, 0,
            0, 2/tb, 0, 0,
            0, 0, 2/fn, 0,
            (right + left)/rl, (top + bottom)/tb, (zFar + zNear)/fn, 0)

''' GLM Implementation

template <typename T> GLM_FUNC_QUALIFIER tmat4x4<T, defaultp>
ortho (T right, T bottom, T top, T zNear, T zFar) {
    tmat4x4<T, defaultp> Result(1);
    Result[0][0] = static_cast<T>(2) / (right - left);
    Result[1][1] = static_cast<T>(2) / (top - bottom);
    Result[2][2] = - static_cast<T>(2) / (zFar - zNear);
    Result[3][0] = - (right + left) / (right - left);
    Result[3][1] = - (top + bottom) / (top - bottom);
    Result[3][2] = - (zFar + zNear) / (zFar - zNear);
    return Result;
}

template <typename T> GLM_FUNC_QUALIFIER tmat4x4<T, defaultp>
ortho (T left, T right, T bottom, T top) {
    tmat4x4<T, defaultp> Result(1);
    Result[0][0] = static_cast<T>(2) / (right - left);
    Result[1][1] = static_cast<T>(2) / (top - bottom);
    Result[2][2] = - static_cast<T>(1);
    Result[3][0] = - (right + left) / (right - left);
    Result[3][1] = - (top + bottom) / (top - bottom);
    return Result;
}'''

def frustum(left, right, bottom, top, near, far):
    rl, tb, fn = right - left, top - bottom, far - near
    return mat4x4(
            2 * near / rl, 0, 0, 0,
            0, 2 * near / tb, 0, 0,
            (right + left) / rl, (top + bottom) / tb, -1, 0,
            0, 0, -2 * far * near / fn, 0)

''' GLM implementation
template <typename T> GLM_FUNC_QUALIFIER tmat4x4<T, defaultp>
frustum (T left, T right, T bottom, T top, T nearVal, T farVal) {
    tmat4x4<T, defaultp> Result(0);
    Result[0][0] = (static_cast<T>(2) * nearVal) / (right - left);
    Result[1][1] = (static_cast<T>(2) * nearVal) / (top - bottom);
    Result[2][0] = (right + left) / (right - left);
    Result[2][1] = (top + bottom) / (top - bottom);
    Result[2][2] = -(farVal + nearVal) / (farVal - nearVal);
    Result[2][3] = static_cast<T>(-1);
    Result[3][2] = -(static_cast<T>(2) * farVal * nearVal) / (farVal - nearVal);
    return Result;
}
'''

def perspective(fovy, aspect, near, far):
    tanFovy2 = tan(fovy / 2)
    return mat4x4(
            1/(aspect * tanFovy2), 0, 0, 0,
            0, 1/tanFovy2, 0, 0,
            0, 0, -(far+near) / (far - near), 0,
            0, 0, -1, -2 * far * near / (far - near))

def perspective(fovy, aspect, near, far):
    s = 1 / tan(fovy / 2 * np.pi / 180)
    M = np.diag([s, s, - float(far + near) / float(far - near), 0])
    M[2][3] = -1; M[3][2] = - 2 * far * near / float(far - near)
    return M.astype(np.float32)

''' GLM implementation
template <typename T> GLM_FUNC_QUALIFIER tmat4x4<T, defaultp>
perspective (T fovy, T aspect, T zNear, T zFar) {
    assert(abs(aspect - std::numeric_limits<T>::epsilon()) > static_cast<T>(0));

    T const tanHalfFovy = tan(fovy / static_cast<T>(2));

    tmat4x4<T, defaultp> Result(static_cast<T>(0));
    Result[0][0] = static_cast<T>(1) / (aspect * tanHalfFovy);
    Result[1][1] = static_cast<T>(1) / (tanHalfFovy);
    Result[2][2] = - (zFar + zNear) / (zFar - zNear);
    Result[2][3] = - static_cast<T>(1);
    Result[3][2] = - (static_cast<T>(2) * zFar * zNear) / (zFar - zNear);
    return Result;
}'''

def perspectiveFov(fov, width, height, near, far):
    h = cos(fov/2) / sin(fov/2)
    w = h * height / width
    return mat4x4(
            w, 0, 0, 0,
            0, h, 0, 0,
            0, 0, -(far + near) / (far - near), -1, 
            0, 0, -2 * far * near / (far - near))

'''GLM implementation
template <typename T> GLM_FUNC_QUALIFIER tmat4x4<T, defaultp>
perspectiveFov (T fov, T width, T height, T zNear, T zFar) {
    assert(width > static_cast<T>(0));
    assert(height > static_cast<T>(0));
    assert(fov > static_cast<T>(0));

    T const rad = fov;
    T const h = glm::cos(static_cast<T>(0.5) * rad) / glm::sin(static_cast<T>(0.5) * rad);
    T const w = h * height / width; ///todo max(width , Height) / min(width , Height)?

    tmat4x4<T, defaultp> Result(static_cast<T>(0));
    Result[0][0] = w;
    Result[1][1] = h;
    Result[2][2] = - (zFar + zNear) / (zFar - zNear);
    Result[2][3] = - static_cast<T>(1);
    Result[3][2] = - (static_cast<T>(2) * zFar * zNear) / (zFar - zNear);
    return Result;
}'''

def project(obj, Model, Proj, viewport):
    V = Proj.dot(Model.dot(obj))
    V = V / V[3] / 2 + 0.5
    V[0] = V[0] * viewport[2] + viewport[0]
    V[1] = V[1] * viewport[3] + viewport[1]
    return V

'''GLM implementation
template <typename T, typename U, precision P> GLM_FUNC_QUALIFIER tvec3<T, P>
project (tvec3<T, P> const & obj, tmat4x4<T, P> const & model, tmat4x4<T, P> const & proj, tvec4<U, P> const & viewport) {
    tvec4<T, P> tmp = tvec4<T, P>(obj, T(1));
    tmp = model * tmp;
    tmp = proj * tmp;

    tmp /= tmp.w;
    tmp = tmp * T(0.5) + T(0.5);
    tmp[0] = tmp[0] * T(viewport[2]) + T(viewport[0]);
    tmp[1] = tmp[1] * T(viewport[3]) + T(viewport[1]);

    return tvec3<T, P>(tmp);
}'''

def lookat(eye, center, up):
    # Forward, Side, and Head
    F = normalize(center - eye)
    S = normalize(np.cross(F, up))
    H = np.cross(S, F)

    LookAt = mat4x4(
        S[0], H[0], -F[0], 0,
        S[1], H[1], -F[1], 0,
        S[2], H[2], -F[2], 0,
        -np.dot(S, eye), -np.dot(H, eye), np.dot(F, eye), 0)

    if False: # If debug
        Translate = translate(-eye[0], -eye[1], -eye[2])
        Rotate = np.transpose(np.array([
            [ S[0], H[0], F[0], 0 ],
            [ S[1], H[1], F[1], 0 ],
            [ S[2], H[2], F[2], 0 ],
            [ 0,    0,    0,    1 ]]))

        print('t3d.Translate:\n{0}'.format(Translate))
        print('t3d.Rotate:\n{0}'.format(Rotate))
        print('t3d.Rotate x Translate:\n{0}'.format(Translate.dot(Rotate)))
        print('t3d.LookAt:\n{0}'.format(LookAt))
        
        LookAtShouldBe = Rotate.dot(Translate)
        assert(LookAt == LookAtShouldBe)

    return LookAt

'''# GLM implementation
template <typename T, precision P> GLM_FUNC_QUALIFIER tmat4x4<T, P>
lookAt (tvec3<T, P> const & eye, tvec3<T, P> const & center, tvec3<T, P> const & up) {
    tvec3<T, P> const f(normalize(center - eye));
    tvec3<T, P> const s(normalize(cross(f, up)));
    tvec3<T, P> const u(cross(s, f));

    tmat4x4<T, P> Result(1);
    Result[0][0] = s.x;
    Result[1][0] = s.y;
    Result[2][0] = s.z;
    Result[0][1] = u.x;
    Result[1][1] = u.y;
    Result[2][1] = u.z;
    Result[0][2] =-f.x;
    Result[1][2] =-f.y;
    Result[2][2] =-f.z;
    Result[3][0] =-dot(s, eye);
    Result[3][1] =-dot(u, eye);
    Result[3][2] = dot(f, eye);
    return Result;
}'''
