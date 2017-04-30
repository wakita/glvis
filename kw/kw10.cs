# compute shader
# version 430

layout(std430, binding=0) buffer particles {
    vec2 pos[];
};

uniform float time;

layout (local_size_x = 1024, local_size_y = 1, local_size_z = 1) in;

#define PI atan(1) * 4
#define PI2 (PI * 2)

/*
vec2 rotate(in vec2 p, in float t) {
    return p * cos(-t) + vec2(p.y, -p.x) * sin(-t);
}
*/

float hash(float n) {
    return fract(sin(n) * 753.5453123);
}

void main() {
    float id = float(gl_GlobalInvocationID.x);
    float v = hash(id * 0.323887);
    float r = abs(sin(id));
    float theta = v * PI2 + time / (0.2 + r) / 3;
    pos[int(id)] = vec2(r * cos(theta), r * sin(theta));
    //pos[id].xz = rotate(pos[id].xz, hash(float(id) * 0.5123) * PI2);
}
