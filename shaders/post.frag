#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform float u_time;

in vec2 texcoord;


const float gamma = 2.2;
const float inv_gamma = 1.0 / gamma;
const float exposure = 1.5;

vec3 exponential_tonemap(vec3 col) {
    return vec3(1.0) - exp(-col * exposure);
}

vec3 aces_tonemap(vec3 col) {
    float a = 2.51f;
    float b = 0.03f;
    float c = 2.43f;
    float d = 0.59f;
    float e = 0.14f;
    return clamp((col * (a * col + b)) / (col * (c * col + d) + e), 0.0, 1.0);
}

vec3 uncharted2_tonemap(vec3 col) {
    float A = 0.15;
    float B = 0.50;
    float C = 0.10;
    float D = 0.20;
    float E = 0.02;
    float F = 0.30;
    return ((col*(A*col+C*B)+D*E)/(col*(A*col+B)+D*F))-E/F;
}

void main() {
    float _ = u_time;

    vec3 col = texture(u_screen_texture, texcoord).rgb;

    // sRGB to linear
    col = pow(col, vec3(gamma));

    // Exposure
    col *= exposure;

    // Tone mapping
    col = uncharted2_tonemap(col);
    
    // Linear to sRGB
    col = pow(col, vec3(inv_gamma));
    
    fragColor = vec4(col, 1.0);
}