#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform float u_exposure;
uniform float u_time;

in vec2 texcoord;


const float gamma = 2.2;
const float inv_gamma = 1.0 / gamma;

vec3 exponential_tonemap(vec3 col) {
    return vec3(1.0) - exp(-col);
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
    vec2 uv = texcoord;
        
    // Curved screen
    uv = (uv - 0.5) * 2.0;
    vec2 offset = abs(uv.yx) * vec2(0.2, 0.25);
    uv += uv * offset * offset;
    uv = uv * 0.5 + 0.5;
    if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
        fragColor = vec4(0.0);
        return;
    }    
    
    vec3 col = texture(u_screen_texture, uv).rgb;

    // Scanlines
    float scanline = sin(uv.y * 800.0 + u_time * 10.0) * 0.04;
    col += scanline;
    
    // Chromatic aberration
    col.r = texture(u_screen_texture, uv + vec2(0.001, 0.0)).r;
    col.b = texture(u_screen_texture, uv - vec2(0.001, 0.0)).b;

    // sRGB to linear
    col = pow(col, vec3(gamma));

    // Exposure
    col *= u_exposure * 0.66;

    // Tone mapping
    // col = exponential_tonemap(col);
    
    // Linear to sRGB
    col = pow(col, vec3(inv_gamma));
    
    fragColor = vec4(col, 1.0);
}