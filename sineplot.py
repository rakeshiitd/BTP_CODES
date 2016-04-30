#!/usr/bin/env python

# Jonathan Senning <jonathan.senning@gordon.edu>
# Gordon College
# January 1999
# Revised August 2000
# Revised April 27, 2006 to update graphing commands
# Converted to Python May 2008
#
# This python program does essentially the same thing as the sequence
# of MatLab commands given on page 25 of "Numerical Mathematics and
# Computing", 4th edition, by Cheney and Kincaid, Brooks/Cole, 1999.

from pylab import *
from math import factorial

x = pi * arange( -400, 401 ) / 100.0
plot( x, sin( x ) )
axis( [x[0], x[-1], -3, 3] )
legend_list = [ '$y = \sin(x)$' ]

y = []
y.append( zeros( len( x ) ) )
for k in range( 0, 5 ):
    y.append( y[-1] + ((-1)**k) * (x**(2*k+1)) / factorial( 2*k+1 ) )
    plot( x, y[k+1] )
    legend_list.append( '$y = T_{%d}(x)$' % k )

xlabel( '$x$' )
ylabel( '$y$' )
title( 'Partial sums of the Taylor series for $\sin(x)$' )
legend( tuple( legend_list ), loc='upper left' )
show()

# End of File
