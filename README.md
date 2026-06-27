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
