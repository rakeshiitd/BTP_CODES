from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

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