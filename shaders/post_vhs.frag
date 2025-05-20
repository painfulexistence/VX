/* License CC BY-NC-SA 4.0 Deed */
/* https://creativecommons.org/licenses/by-nc-sa/4.0/ */
/* Fork of Ryk's VCR distortion shader */
/* https://www.shadertoy.com/view/ldjGzV */

#version 330 core

layout(location = 0) out vec4 fragColor;

uniform sampler2D u_screen_texture;
uniform sampler2D u_noise_texture;
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

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233*cos(u_time)))) * 43758.5453123);
}

float noise(vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);
    
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

// TODO: Add noise texture
// float noise(vec2 p) {
// 	float s = texture(u_noise_texture,vec2(1.,2.*cos(u_time))*u_time*8. + p*1.).x;
// 	s *= s;
// 	return s;
// }

float onOff(float a, float b, float c) {
	return step(c, sin(u_time + a*cos(u_time*b)));
}

float ramp(float y, float start, float end) {
	float inside = step(start,y) - step(end,y);
	float fact = (y-start)/(end-start)*inside;
	return (1.-fact) * inside;
	
}

float stripes(vec2 uv) {
	float noi = noise(uv*vec2(0.5,1.) + vec2(1.,3.));
	return ramp(mod(uv.y*4. + u_time/2.+sin(u_time + sin(u_time*0.63)),1.),0.5,0.6)*noi;
}

vec2 screenDistort(vec2 uv) {
	uv -= vec2(.5,.5);
	uv = uv*1.2*(1./1.2+2.*uv.x*uv.x*uv.y*uv.y);
	uv += vec2(.5,.5);
	return uv;
}

void main() {
    vec2 uv = screenDistort(texcoord);

    vec2 look = uv;
	float window = 1./(1.+20.*(look.y-mod(u_time/4.,1.))*(look.y-mod(u_time/4.,1.)));
	look.x = look.x + sin(look.y*10. + u_time)/50.*onOff(4.,4.,.3)*(1.+cos(u_time*80.))*window;
	float vShift = 0.4*onOff(2.,3.,.9)*(sin(u_time)*sin(u_time*20.) + (0.5 + 0.1*sin(u_time*200.)*cos(u_time)));
	look.y = mod(look.y + vShift, 1.);

	float vigAmt = 3.+.3*sin(u_time + 5.*cos(u_time*5.));
	float vignette = (1.-vigAmt*(uv.y-.5)*(uv.y-.5))*(1.-vigAmt*(uv.x-.5)*(uv.x-.5));
	
    vec3 video = vec3(texture(u_screen_texture, look));
	video = pow(video, vec3(gamma)); // sRGB to linear
	video *= u_exposure; // Exposure
	video = uncharted2_tonemap(video); // Tone mapping
	// video += stripes(uv);
	// video += noise(uv*2.)/2.; // Noisy pattern
	video *= vignette;
	video *= (12.+mod(uv.y*30.+u_time,1.))/13.;
    video = pow(video, vec3(inv_gamma)); // Linear to sRGB
	
	fragColor = vec4(video, 1.0);
}