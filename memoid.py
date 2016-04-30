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
    time1Hs_H120 = time.time()
    Hs_H120= getFields(120.,'head')
    time2Hs_H120 = time.time()
    print 'function took---------------------------------->>>> '+str(((time1Hs_H120-time2Hs_H120)*1000.0))

    if not plotIt:return
    import matplotlib.pyplot as plt
    plt.figure(figsize=(13,5))
    plt.subplot(121)
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