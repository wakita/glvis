# compute shader
# version 430

layout(std430, binding=0) buffer particles {
    vec3 pos[];
};

uniform float time;

layout (local_size_x = 128, local_size_y = 1, local_size_z = 1) in;

#define PI atan(1) * 4
#define PI2 (PI * 2)

vec2 rotate(in vec2 p, in float t) {
    return p * cos(-t) + vec2(p.y, -p.x) * sin(-t);
}

float hash(float n) {
    return fract(sin(n) * 753.5453123);
}

void main() {
    uint id = gl_GlobalInvocationID.x;
    float theta = hash(float(id) * 0.3123887) * PI2 + time;
    pos[id] = vec3(cos(theta) + 1.5, sin(theta) * 0.2, 0.0);
    pos[id].xz = rotate(pos[id].xz, hash(float(id) * 0.5123) * PI2);
}
