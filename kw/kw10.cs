# compute shader
# version 430

/* For testing purpose, the following buffer is declared but (intentionally) not used in the application code. */

layout(std430) buffer position_buf {
    vec2 position[];
};

layout(std430) buffer color_buf {
    vec3 color[];
};

uniform float time;

layout (local_size_x = 1024, local_size_y = 1, local_size_z = 1) in;

#define PI atan(1) * 4
#define PI2 (PI * 2)

float hash(float n) {
    return fract(sin(n) * 753.5453123);
}

void main() {
    uint id = gl_GlobalInvocationID.x;
    float v = hash(id * 0.323887);
    float r = abs(sin(float(id)));
    float theta = v * PI2 + time / (0.2 + r) / 3;
    position[id] = vec2(r * cos(theta), r * sin(theta));
    //color[int(id)] = vec3(position[int(id)], 1);
    color[id] = vec3(0, 0, 1);
}
