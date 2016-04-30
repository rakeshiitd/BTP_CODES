import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

#Data:
x = np.linspace(0,2*np.pi,100)
f = np.sin(x) + .02*(np.random.rand(100)-.5)

#Normalization:
dx = x[1] - x[0] # use np.diff(x) if x is not uniform
dxdx = dx**2

#First derivatives:
df = np.diff(f) / dx
cf = np.convolve(f, [1,-1]) / dx
gf = ndimage.gaussian_filter1d(f, sigma=1, order=1, mode='wrap') / dx

#Second derivatives:
ddf = np.diff(f, 2) / dxdx
ccf = np.convolve(f, [1, -2, 1]) / dxdx
ggf = ndimage.gaussian_filter1d(f, sigma=1, order=2, mode='wrap') / dxdx

#Plotting:
plt.figure()
plt.plot(x, f, 'k', lw=2, label='original')
plt.plot(x[:-1], df, 'r.', label='np.diff, 1')
plt.plot(x, cf[:-1], 'r--', label='np.convolve, [1,-1]')
plt.plot(x, gf, 'r', label='gaussian, 1')
plt.plot(x[:-2], ddf, 'g.', label='np.diff, 2')
plt.plot(x, ccf[:-2], 'g--', label='np.convolve, [1,-2,1]')
plt.plot(x, ggf, 'g', label='gaussian, 2')

x = np.linspace(0,2*np.pi,100)
sine = np.sin(x)

im = sine * sine[...,None]
d1 = ndimage.gaussian_filter(im, sigma=5, order=1, mode='wrap')
d2 = ndimage.gaussian_filter(im, sigma=5, order=2, mode='wrap')

plt.figure()

plt.subplot(131)
plt.imshow(im)
plt.title('original')

plt.subplot(132)
plt.imshow(d1)
plt.title('first derivative')

plt.subplot(133)
plt.imshow(d2)
plt.title('second derivative')