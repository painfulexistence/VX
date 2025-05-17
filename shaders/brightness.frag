#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_texture;

in vec2 texcoord;


const float threshold = 1.0;

void main() {
    vec3 color = texture(u_texture, texcoord).rgb;
    
    float brightness = dot(color, vec3(0.2126, 0.7152, 0.0722));
    float contribution = max(0.0, brightness - threshold);
    color *= contribution / (brightness + 0.00001);
    
    fragColor = vec4(color, 1.0);
} 