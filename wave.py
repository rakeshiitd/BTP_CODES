#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Jonathan Senning <jonathan.senning@gordon.edu>
# Gordon College
# April 26, 1999
# Converted to Python November 2008
#
# $Id$
#
# Solve the one-dimensional wave equation
#
#       d  du       d  du
#       -- -- = c^2 -- --
#       dt dt       dx dx
#
# along with boundary conditions
#
#       u(xmin,t) = 0
#       u(xmax,t) = 0
#
# and initial conditions
#
#       u(x,tmin)  = f(x)
#       u'(x,tmin) = g(x)
#
#-----------------------------------------------------------------------------

import matplotlib
matplotlib.use( 'GTKAgg' )

from pylab import *
import time

individual_curves = 1           # Show curves during comutation

# Set the value of the wave velocity

c = 1

# Set size of the domain.  These values are combined with interval sizes to
# compute h (spatial stepsize) and k (temporal stepsize).

n = 256;                    # Number of spatial intervals
m = 1024+1;                 # Number of time steps

# We need three rows (timesteps) of data to be available at any given time.
# The finite difference stencil for this problem looks like a cross, where
# u[i,j+1] is computed using u[i-1,j], u[i,j], u[i+1,j] and u[i,j-1].  We
# compute the j+1 timestep information using the j and j-1 timestep
# information.  As we don't need to keep all previously computed data, only
# that for the most recent two timesteps, we can use a three-row matrix to
# hold the data being computed (j+1) and the data being used (j and j-1).  A
# separate index array, called z in this program, will be used to cycle
# through the rows of u so we don't actually need to copy them as the
# iteration progresses.  z[2] will always refer to the j+1 timestep
# information, z[1] refers to the j timestep and z[0] refers to the j-1
# timestep.

u = zeros( ( n+1, 3 ), float )
z = range( 3 )

# X position of left and right endpoints

xmin, xmax = ( 0, 1 )

# Interval of time: tmin should probably be left at zero

tmin, tmax = ( 0, 4 ) # ( 0, 4 )

# Compute step sizes

h = ( xmax - xmin ) / float( n )
k = ( tmax - tmin ) / float( m )
rho = ( c * c ) * ( k * k ) / ( h * h );

if rho >= 1:
    print 'Warning: may be unstable; rho = %f >= 1' % rho

# Generate x values.  These aren't really needed to solve the PDE but they
# are useful for computing boundary/initial conditions and graphing.

x = linspace( xmin, xmax, n+1 )

# Initial conditions

def f( x, n ):
    #y = zeros( n+1, float )
    #y[n/4:n/2] = 100 * ( 1.0 - cos( 8 * pi * x[n/4:n/2] ) )
    x0 = 0.6
    y = exp( -200 * ( x - x0 )**2 )
    return y

def g( x, n ):
    return 0.0 * x

u[:,0] = f( x, n )
u[:,1] = 0.5 * rho * ( f( x - h, n ) + f( x + h, n ) ) \
                + ( 1 - rho ) * f( x, n ) + k * g( x, n )

# Boundary conditions

u[0,:] = 0.0                   # Left
u[n,:] = 0.0                   # Right

#-----------------------------------------------------------------------------
#       Should not need to make changes below this point :)
#-----------------------------------------------------------------------------

# Find likely extremes for u

umax = u.max()
umin = -umax

# Plot initial condition curve.  The "sleep()" is used to allow time for the
# plot to appear on the screen before actually starting to solve the problem
# for t > 0.

ion()

if individual_curves != 0:
    plot( x, u[:,0], '-' )
    axis( [xmin, xmax, umin, umax] )
    xlabel( 'x' )
    ylabel( 'displacement' )
    title( 'step = %4d; t = %f;' % ( 0, 0.0 ) )
    draw()
    time.sleep( 3 )

# Main loop.

for j in xrange( 1, m ):

    if individual_curves != 0:
        ioff()
        cla()
        plot( x, u[:,z[1]], '-' )
        axis( [xmin, xmax, umin, umax] )
        xlabel( 'x' )
        ylabel( 'displacement' )
        title( 'step = %4d; t = %f' % ( j, j * k ) )
        draw()
        draw()   # second draw() is necessary to show most recent figure
        ion()

    u[1:-1,z[2]] = rho * ( u[0:-2,z[1]] + u[2:,z[1]] ) \
                        + 2.0 * ( 1 - rho ) * u[1:-1,z[1]] - u[1:-1,z[0]]

    # Rotate indices so z[1] is index of most recent date in u

    z[0], z[1], z[2] = ( z[1], z[2], z[0] )

# Draw last curve

if individual_curves != 0:
    ioff()
    cla()
    plot( x, u[:,z[1]], '-' )
    axis( [xmin, xmax, umin, umax] )
    xlabel( 'x' )
    ylabel( 'displacement' )
    title( 'step = %4d; t = %f' % ( m, m * k ) )
    draw()
    draw()   # second draw() is necessary to show most recent figure
    ion()
    raw_input( "Press Enter to quit... " )

# End of file
