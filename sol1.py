from SimPEG import *
from SimPEG.FLOW import Richards
import time

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap
@timing
def run(plotIt=True):
    """
        FLOW: Richards: 1D: Celia1990
        =============================

        There are two different forms of Richards equation that differ
        on how they deal with the non-linearity in the time-stepping term.

        The most fundamental form, referred to as the
        'mixed'-form of Richards Equation Celia1990_

        .. math::

            \\frac{\partial \\theta(\psi)}{\partial t} - \\nabla \cdot k(\psi) \\nabla \psi - \\frac{\partial k(\psi)}{\partial z} = 0
            \quad \psi \in \Omega

        where \\\\(\\\\theta\\\\) is water content, and \\\\(\\\\psi\\\\) is pressure head.
        This formulation of Richards equation is called the
        'mixed'-form because the equation is parameterized in \\\\(\\\\psi\\\\)
        but the time-stepping is in terms of \\\\(\\\\theta\\\\).

        As noted in Celia1990_ the 'head'-based form of Richards
        equation can be written in the continuous form as:

        .. math::

            \\frac{\partial \\theta}{\partial \psi}\\frac{\partial \psi}{\partial t} - \\nabla \cdot k(\psi) \\nabla \psi - \\frac{\partial k(\psi)}{\partial z} = 0 \quad \psi \in \Omega

        However, it can be shown that this does not conserve mass in the discrete formulation.

        Here we reproduce the results from Celia1990_ demonstrating the head-based formulation and the mixed-formulation.

        .. _Celia1990: http://www.webpages.uidaho.edu/ch/papers/Celia.pdf
    """
    time1 = time.time()
    M = Mesh.TensorMesh([np.ones(40)])
    M.setCellGradBC('dirichlet')
    params = Richards.Empirical.HaverkampParams().celia1990
    params['Ks'] = np.log(params['Ks'])
    E = Richards.Empirical.Haverkamp(M, **params)

    bc = np.array([-61.5,-20.7])
    h = np.zeros(M.nC) + bc[0]


    def getFields(timeStep,method):
        timeSteps = np.ones(360/timeStep)*timeStep
        prob = Richards.RichardsProblem(M, mapping=E, timeSteps=timeSteps,
                                        boundaryConditions=bc, initialConditions=h,
                                        doNewton=False, method=method)
        return prob.fields(params['Ks'])

    time1Hs_M10 = time.time()
    Hs_M10 = getFields(10., 'mixed')
    time2Hs_M10 = time.time()
    print 'function took---------------------------------->>>> '+str(((time2Hs_M10-time1Hs_M10)*1000.0))
    Hs_M30 = getFields(30., 'mixed')
    Hs_M120= getFields(120.,'mixed')
    time1Hs_H120 = time.time()
    Hs_H10 = getFields(10., 'head')
    time2Hs_H120 = time.time()
    print 'function took---------------------------------->>>> '+str(((time1Hs_H120-time2Hs_H120)*1000.0))
    Hs_H30 = getFields(30., 'head')
    Hs_H120= getFields(120.,'head')

    if not plotIt:return
    import matplotlib.pyplot as plt
    plt.figure(figsize=(13,5))
    plt.subplot(121)
    plt.plot(40-M.gridCC, Hs_M10[-1],'b-')
    plt.plot(40-M.gridCC, Hs_M30[-1],'r-')
    plt.plot(40-M.gridCC, Hs_M120[-1],'k-')
    plt.ylim([-70,-10])
    plt.title('Mixed Method')
    plt.xlabel('Depth, cm')
    plt.ylabel('Pressure Head, cm')
    plt.legend(('$\Delta t$ = 10 sec','$\Delta t$ = 30 sec','$\Delta t$ = 120 sec'))
    plt.subplot(122)
    plt.plot(40-M.gridCC, Hs_H10[-1],'b-')
    plt.plot(40-M.gridCC, Hs_H30[-1],'r-')
    plt.plot(40-M.gridCC, Hs_H120[-1],'k-')
    plt.ylim([-70,-10])
    plt.title('Head-Based Method')
    plt.xlabel('Depth, cm')
    plt.ylabel('Pressure Head, cm')
    plt.legend(('$\Delta t$ = 10 sec','$\Delta t$ = 30 sec','$\Delta t$ = 120 sec'))
    time2 = time.time()
    print 'function took---------------------------------- '+str(((time2-time1)*1000.0))
    plt.show()

if __name__ == '__main__':
    run()