# Escher Warp

An interactive demo of the conformal **Droste map** behind M.&nbsp;C.&nbsp;Escher's
*Print Gallery*, as analysed by Bart de&nbsp;Smit and Hendrik Lenstra.

A *straight* picture that is **self-similar under scaling by `q`** about its centre
(it contains a copy of itself shrunk by `q`) is turned into the famous twist by the
complex map

```
output(z) = input(z^alpha),   alpha = 1 - i * ln(q) / (2*pi)
```

This exponent is the only family for which crossing the complex-log branch cut
(`theta -> theta + 2*pi`) rescales the source by exactly `q^k` — a real
self-similarity the source actually has — so the result is **seamless**. It also
makes the *output* self-similar under a scale of ~22.6x and a rotation of ~157.6°
per loop (the signature numbers from the de&nbsp;Smit–Lenstra paper) and keeps the
centre sharp (`Re(alpha) = 1`).

## The self-similarity rectangle

Drag the rectangle on the source to mark the **shrunk copy of the whole picture
inside itself** (aspect-locked, no rotation — a pure scaling). From it the app
derives the two parameters the map needs:

- `q = imageWidth / rectWidth` — the self-similarity factor.
- `F = C_rect / (1 - 1/q)` — the recursion **fixed point** (the spiral's eye),
  the one point left unmoved by "scale the full image down into the rectangle".

The renderer folds sample points by scaling about `F` (an off-center version of
the square `max(|x|,|y|)` norm). The result is seamless **iff** the rectangle
matches the image's actual self-similarity — which is exactly how you tell the
app where the self-similarity is when you upload your own Droste image.

## Running

It's a single static page. Serve the folder and open `index.html`:

```
python3 -m http.server
```

(A server is needed so the canvas can read the source image without tainting.)

## The source image

`make_selfsimilar.py` procedurally generates a **rectangular self-similar** source —
a one-point-perspective gallery corridor that contains a scaled copy of itself in a
centred square. Self-similarity is exact because every pixel is a function only of
`frac(log_q(rho))` (depth) and position across the current face, with
`rho = max(|x|, |y|)` (the same L∞ norm the renderer folds by). Change `q` or the
drawing layers and re-run:

```
python3 make_selfsimilar.py assets/selfsimilar.png.ppm   # then convert to PNG
```

You can also upload your own image in the page — but it only looks right if it is
genuinely self-similar by the chosen `q`.
