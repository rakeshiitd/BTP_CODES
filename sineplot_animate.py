#!/usr/bin/env python

# Jonathan Senning <jonathan.senning@gordon.edu>
# Gordon College
# January 1999
# Converted to Python May 2008
# Animation added January 2015
#
# This python program does essentially the same thing as the sequence
# of MatLab commands given on page 25 of "Numerical Mathematics and
# Computing", 4th edition, by Cheney and Kincaid, Brooks/Cole, 1999.

from pylab import *
from math import factorial
import time

ion()

x = pi * arange( -400, 401 ) / 100.0
y = []
y.append( zeros( len( x ) ) )
plot( x, sin( x ), 'b-' )
axis( [x[0], x[-1], -3, 3] )
xlabel( '$x$' )
ylabel( '$y$' )
title( 'Partial sums of the Taylor series for $\sin(x)$' )
legend_list = [ '$y = \sin(x)$' ]
legend( tuple( legend_list ), loc='upper center' )
draw()

for k in range( 0, 12 ):
    time.sleep( 1 )
    y.append( y[-1] + ((-1)**k) * (x**(2*k+1)) / factorial( 2*k+1 ) )
    ioff()
    cla()
    plot( x, sin( x ), 'b-', x, y[k+1], 'r-' )
    axis( [x[0], x[-1], -3, 3] )
    xlabel( '$x$' )
    ylabel( '$y$' )
    title( 'Partial sums of the Taylor series for $\sin(x)$' )
    legend_list = [ '$y = \sin(x)$', '$y = T_{%d}(x)$' % k ]
    legend( tuple( legend_list ), loc='upper center' )
    draw()
    ion()

raw_input( "Press Enter to quit... " )

# End of File
