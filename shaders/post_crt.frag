#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform float u_time;

in vec2 texcoord;

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
    
    vec4 color = texture(u_screen_texture, uv);

    // Scanlines
    float scanline = sin(uv.y * 800.0 + u_time * 10.0) * 0.04;
    color.rgb += scanline;
    
    // Chromatic aberration
    color.r = texture(u_screen_texture, uv + vec2(0.001, 0.0)).r;
    color.b = texture(u_screen_texture, uv - vec2(0.001, 0.0)).b;
    
    fragColor = color;
}