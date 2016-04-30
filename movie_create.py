import CreateMovie as movie
import matplotlib.pyplot as plt
import numpy as np

 
x = np.linspace(-.5,4,500)
 
# Plots a given frame
def plotFunction( frame ):
	plt.plot(x, np.exp( -10*(x - frame/10.0)**2) )

	plt.axis((-.5,4,0,1.1))
 
movie.CreateMovie(plotFunction, 50)

def CreateMovie(plotter, numberOfFrames, fps=10):
	import os, sys

	import matplotlib.pyplot as plt
 
	for i in range(numberOfFrames):
		plotter(i)

		fname = '_tmp%05d.png'%i
 
		plt.savefig(fname)
		plt.clf()
 
	os.system("rm movie.mp4")

	os.system("ffmpeg -r "+str(fps)+" -b 1800 -i _tmp%05d.png movie.mp4")
	os.system("rm _tmp*.png")