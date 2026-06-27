#!/usr/bin/env python3
"""Generate a RECTANGULAR self-similar (Droste) source image.

A one-point-perspective corridor/gallery that contains a scaled copy of
itself in a centered square: nested archways receding to a vanishing point,
side walls hung with framed pictures, a tiled floor and ceiling.

Self-similarity is exact because every pixel value is a function only of
  u = frac(log_q(rho)),  rho = max(|x|,|y|)   (depth within one segment)
  s = position across the current face   (in [-1,1])
  face = floor / ceiling / left wall / right wall
Scaling the plane by q maps the image onto itself -> perfect Droste input.
The page reduces coordinates by the SAME L-inf norm, so this lines up exactly.
"""
import numpy as np, sys, math

OUT = 800        # final image size
SS = 4           # supersampling factor: baked-in anti-aliasing (one-time)
W = OUT * SS     # work resolution
q = 8.0          # self-similarity factor (use the same q in the page)

xs = np.linspace(-1, 1, W)
X, Y = np.meshgrid(xs, xs)
ax, ay = np.abs(X), np.abs(Y)
rho = np.maximum(np.maximum(ax, ay), 1e-6)
lnq = math.log(q)
u = (np.log(rho) / lnq) % 1.0            # 0 = far/inner edge, 1 = near/outer edge

vertical = ax >= ay                      # left/right walls
horizontal = ~vertical                   # floor/ceiling
right = vertical & (X > 0)
left  = vertical & (X <= 0)
ceil  = horizontal & (Y > 0)
floor = horizontal & (Y <= 0)

# position across the current face, in [-1,1]
s = np.where(vertical, Y / rho, X / rho)

img = np.zeros((W, W), float)

# ---- base shading per face, with a depth gradient (far=dark, near=light) ----
depth = 0.45 + 0.55 * u                  # darker toward the vanishing point
img[left]  = 0.50 * depth[left]
img[right] = 0.58 * depth[right]
img[floor] = 0.80 * depth[floor]
img[ceil]  = 0.30 * depth[ceil]

def m(mask):                              # convenience
    return mask

# ---- floor tiles: lines across (constant s) and depth seams (constant u) ----
tile_s = (np.abs(((s * 4) % 1.0) - 0.5) < 0.03)
seam_u = (((u) % (1/3)) < 0.02)
img[floor & (tile_s | seam_u)] = 0.95
img[ceil  & (tile_s | seam_u)] = 0.15

# ---- framed pictures on the side walls, each with a big "L" / "R" letter ----
def letter_mask(L, X, Y):                 # X right, Y up; strokes ~0.4 thick
    vbar = (X > -0.55) & (X < -0.15) & (Y > -0.9) & (Y < 0.9)
    if L == 'L':
        hbar = (Y > -0.9) & (Y < -0.5) & (X > -0.55) & (X < 0.55)
        return vbar | hbar
    top = (Y > 0.5) & (Y < 0.9) & (X > -0.55) & (X < 0.4)         # R: bowl top
    rsd = (X > 0.1) & (X < 0.5) & (Y > 0.05) & (Y < 0.9)          #    bowl side
    mid = (Y > 0.05) & (Y < 0.45) & (X > -0.55) & (X < 0.5)       #    bowl bottom
    leg = (np.abs((Y - 0.05) + 1.4 * (X + 0.15)) < 0.32) \
          & (X > -0.2) & (X < 0.6) & (Y > -0.9) & (Y < 0.1)       #    diagonal leg
    return vbar | top | rsd | mid | leg

def wall_pictures(mask, L, xdir):
    inb = mask & (np.abs(s) < 0.62) & (u > 0.22) & (u < 0.82)
    frame = inb & ((np.abs(s) > 0.55) | (u < 0.30) | (u > 0.74))
    mat   = inb & ~frame
    img[mat] = 0.93
    img[frame] = 0.08
    # letter coords: depth (u) is the picture's horizontal, screen (s) its vertical
    LX = xdir * (u - 0.52) / 0.22
    LY = -s / 0.5
    img[mat & letter_mask(L, LX, LY)] = 0.12
wall_pictures(left,  'L', -1)
wall_pictures(right, 'R', +1)

# ---- nested archway: a thick dark frame at each segment boundary ----
arch = (u < 0.06) | (u > 0.965)
img[arch] = 0.05
# a lighter inner lip just inside the arch for a 3-D molding feel
lip = ((u >= 0.06) & (u < 0.10)) | ((u <= 0.965) & (u > 0.93))
img[lip] = 0.70

# ---- the recursion center is left BLANK on purpose ----
# Everything inside the self-similarity rectangle (rho < 1/q) is never sampled by
# the renderer: it folds the outer ring inward to synthesize the recursion. So we
# just paint it black here to show the source does NOT need to be pre-drosted.
img[rho < 1.0 / q] = 0.04

g = np.clip(img, 0, 1)
# box-downsample SSxSS -> bake the anti-aliasing into the final image
g = g.reshape(OUT, SS, OUT, SS).mean(axis=(1, 3))
rgb = (np.dstack([g, g, g]) * 255).astype(np.uint8)
with open(sys.argv[1], 'wb') as f:
    f.write(b'P6\n%d %d\n255\n' % (OUT, OUT))
    f.write(rgb.tobytes())
print("wrote", sys.argv[1], OUT, "x", OUT, "(SS=%d)" % SS, "q=", q)
