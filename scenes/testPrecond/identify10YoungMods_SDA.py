import Sofa
import math
import os
import sys
import csv
import yaml
import pprint
import numpy as np

__file = __file__.replace('\\', '/') # windows



def createScene(rootNode):
    # rootNode.createObject('RequiredPlugin', name='SofaMiscFem')
    rootNode.createObject('RequiredPlugin', name='Visual', pluginName='SofaOpenglVisual')
    rootNode.createObject('RequiredPlugin', name='Python', pluginName='SofaPython')
    rootNode.createObject('RequiredPlugin', name='Optimus', pluginName='Optimus')

    try:
        sys.argv[0]
    except:
        commandLineArguments = []
    else:
        commandLineArguments = sys.argv

    if len(commandLineArguments) > 1:
        configFileName = commandLineArguments[1]
    else:
        print 'ERROR: Must supply a yaml config file as an argument!'
        return

    with open(configFileName, 'r') as stream:
        try:
            options = yaml.safe_load(stream)

        except yaml.YAMLError as exc:
            print(exc)
            return

    if options['model']['int']['lin_type'] == 'Pardiso':
        rootNode.createObject('RequiredPlugin', name='Pardiso', pluginName='SofaPardisoSolver')

    AppliedForces_SDA(rootNode, options)

    return 0;




class AppliedForces_SDA(Sofa.PythonScriptController):

    def __init__(self, rootNode, opt):
        self.opt = opt

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(opt)

        ### extract configuration data
        self.saveEst = opt['io']['saveEst']
        self.saveGeo = opt["io"]["saveGeo"]
        prefix = opt['io']['prefix']
        suffix = opt['io']['suffix']

        ### generate output folders
        self.mainFolder = prefix + opt['model']['fem']['method'] + '_' + opt['model']['int']['type'] + str(opt['model']['int']['maxit']) + suffix
        # self.mainFolder = prefix + opt['model']['int']['type'] + str(opt['model']['int']['maxit']) + suffix
        self.obsFile = self.mainFolder +'/'+ opt['io']['obsFileName']
        self.estFolder = self.mainFolder + '/' + opt['filter']['kind'] + opt['io']['sda_suffix']

        if self.saveEst:
            os.system('mv '+self.estFolder+' '+self.estFolder+'_arch')
            os.system('mkdir '+self.estFolder)

            self.stateExpFile=self.estFolder+'/state.txt'
            self.stateVarFile=self.estFolder+'/variance.txt'
            self.stateCovarFile=self.estFolder+'/covariance.txt'
            # os.system('rm '+self.stateExpFile)
            # os.system('rm '+self.stateVarFile)
            # os.system('rm '+self.stateCovarFile)

        if self.saveGeo:
            self.geoFolder = self.estFolder + '/VTK'
            os.system('mkdir -p '+self.geoFolder)

        self.createGraph(rootNode)

        return



    def createGraph(self, rootNode):
        ### scene global stuff
        self.rootNode = rootNode
        rootNode.findData('dt').value = self.opt['model']['dt']
        rootNode.findData('gravity').value = self.opt['model']['gravity']

        rootNode.createObject('ViewerSetting', cameraMode='Perspective', resolution='1000 700', objectPickingMethod='Ray casting')
        rootNode.createObject('VisualStyle', name='VisualStyle', displayFlags='showBehaviorModels showForceFields showCollisionModels hideVisualModels')

        rootNode.createObject('FilteringAnimationLoop', name="StochAnimLoop", verbose="1")

        ### filter data
        self.filterKind = self.opt['filter']['kind']
        if self.filterKind == 'ROUKF':
            self.filter = rootNode.createObject('ROUKFilter', name="ROUKF", verbose="1", useBlasToMultiply='0', printLog='1', sigmaTopology=self.opt['filter']['sigma_points_topology'])
            estimatePosition = 1
        elif self.filterKind == 'UKFSimCorr':
            self.filter = rootNode.createObject('UKFilterSimCorr', name="UKFSC", verbose="1")
            estimatePosition = 0

        ### object loader
        rootNode.createObject('MeshVTKLoader', name='loader', filename=self.opt['model']['vol_mesh'])
        rootNode.createObject('MeshSTLLoader', name='sloader', filename=self.opt['model']['surf_mesh'])

        ### general node
        modelNode=rootNode.createChild('ModelNode')
        modelNode.createObject('StochasticStateWrapper', name="StateWrapper", verbose='1', langrangeMultipliers=0, estimatePosition=estimatePosition)
        simuNode=modelNode.createChild('cylinder')

        ### solvers
        intType = self.opt['model']['int']['type']
        if intType == 'Euler':
            rmass = self.opt['model']['int']['rmass']
            rstiff = self.opt['model']['int']['rstiff']
            simuNode.createObject('EulerImplicitSolver', rayleighStiffness=rstiff, rayleighMass=rmass)
        elif intType == 'Newton':
            intMaxit = self.opt['model']['int']['maxit']
            simuNode.createObject('StaticSolver', name="NewtonStatic", correction_tolerance_threshold="1e-8", residual_tolerance_threshold="1e-8", should_diverge_when_residual_is_growing="1",  newton_iterations=intMaxit, printLog='0')
        else:
            print 'Unknown solver type!'

        if self.opt['model']['linsol']['usePCG']:
            simuNode.createObject('StepPCGLinearSolver', name='lsolverit',use_precond='1', tolerance='1e-10', iterations='500', verbose='1', listening='1', preconditioners='lsolver', precondOnTimeStep=self.opt['model']['linsol']['PCGOnTimeStep'], update_step=self.opt['model']['linsol']['PCGRegularUpdate'], numIterationsToRefactorize=self.opt['model']['linsol']['PCGNumIterToRefact'])

        linType = self.opt['model']['int']['lin_type']
        if linType == 'Pardiso':
            simuNode.createObject('SparsePARDISOSolver', name='lsolver', verbose='0', pardisoSchurComplement=0, symmetric=self.opt['model']['linsol']['pardisoSym'], exportDataToFolder=self.opt['model']['linsol']['pardisoFolder'])
        elif linType == 'CG':
            simuNode.createObject('CGLinearSolver', name='lsolverit', tolerance='1e-10', threshold='1e-10', iterations='500', verbose='0')
        else:
            print 'Unknown linear solver type!'

        ### mechanical object
        simuNode.createObject('MechanicalObject', src="@/loader", name="Volume")
        simuNode.createObject('TetrahedronSetTopologyContainer', name="Container", src="@/loader", tags=" ")
        simuNode.createObject('TetrahedronSetTopologyModifier', name="Modifier")
        simuNode.createObject('TetrahedronSetTopologyAlgorithms', name="TopoAlgo")
        simuNode.createObject('TetrahedronSetGeometryAlgorithms', name="GeomAlgo")

        if 'total_mass' in self.opt['model'].keys():
            simuNode.createObject('UniformMass', totalMass=self.opt['model']['total_mass'])

        if 'density' in self.opt['model'].keys():
            simuNode.createObject('MeshMatrixMass', printMass='0', lumping='1', massDensity=self.opt['model']['density'], name='mass')

        ### estimate material properties
        simuNode.createObject('OptimParams', name="paramE", optimize="1", template="Vector", numParams=self.opt['filter']['nparams'],
            transformParams=self.opt['filter']['param_transform'], initValue=self.opt['filter']['param_init_exval'], stdev=self.opt['filter']['param_init_stdev'])

        youngModuli=self.opt['model']['fem']['young_modulus']
        poissonRatio = self.opt['model']['fem']['poisson_ratio']
        indices = range(1, len(youngModuli)+1)
        method = self.opt['model']['fem']['method']
        if  method[0:3] == 'Cor':
            simuNode.createObject('Indices2ValuesMapper', indices=indices, values='@paramE.value', name='youngMapper', inputValues='@loader.dataset')
            simuNode.createObject('TetrahedronFEMForceField', name='FEM', method='large', listening='true', drawHeterogeneousTetra='1', poissonRatio=poissonRatio, youngModulus='@youngMapper.outputValues', updateStiffness='1')
        elif method == 'StVenant':
            poissonRatii = poissonRatio * np.ones([1,len(youngModuli)])
            simuNode.createObject('Indices2ValuesTransformer', name='paramMapper', indices=indices, values1='@paramE.value', values2=poissonRatii, inputValues='@loader.dataset', transformation='ENu2MuLambda')
            simuNode.createObject('TetrahedronHyperelasticityFEMForceField', name='FEM', materialName='StVenantKirchhoff', ParameterSet='@paramMapper.outputValues')

        ### boundary conditions
        simuNode.createObject('BoxROI', box=self.opt['model']['bc']['boxes'], name='fixedBox')
        simuNode.createObject('FixedConstraint', indices='@fixedBox.indices')

        ### external impact
        if 'applied_periodic_force' in self.opt['model'].keys():
            simuNode.createObject('BoxROI', name='forceBox', box=self.opt['model']['applied_periodic_force']['boxes'])
            self.appliedForce = simuNode.createObject('ConstantForceField', force=self.opt['model']['applied_periodic_force']['initial_force'], indices='@forceBox.indices')

        ### export data
        if self.saveGeo:
            simuNode.createObject('VTKExporterDA', filename=self.geoFolder+'/object.vtk', XMLformat='0', listening='1', edges="0", triangles="0", quads="0", tetras="1", exportAtBegin="1", exportAtEnd="0", exportEveryNumberOfSteps="1")

        ### node with groundtruth observations
        obsNode = simuNode.createChild('observations')
        obsNode.createObject('MeshVTKLoader', name='obsloader', filename=self.opt['filter']['obs_points'])
        obsNode.createObject('MechanicalObject', name='SourceMO', position='@obsloader.position')
        # obsNode.createObject('VTKExporter', name='temporaryExporter', filename='tempObs.vtk', XMLformat='0', listening='1', edges="0", triangles="0", quads="0", tetras="0", exportAtBegin="1", exportAtEnd="0", exportEveryNumberOfSteps="0", position='@SourceMO.position')
        obsNode.createObject('BarycentricMapping')
        obsNode.createObject('MappedStateObservationManager', name="MOBS", listening="1", stateWrapper="@../../StateWrapper", verbose="1", observationStdev=self.opt['filter']['observ_stdev'], noiseStdev=self.opt['filter']['observ_noise_stdev'])
        obsNode.createObject('SimulatedStateObservationSource', name="ObsSource", monitorPrefix=self.obsFile)
        obsNode.createObject('ShowSpheres', name="estimated", radius="0.002", color="1 0 0 1", position='@SourceMO.position')
        obsNode.createObject('ShowSpheres', name="groundTruth", radius="0.0015", color="1 1 0 1", position='@MOBS.mappedObservations')

        ### visual node
        oglNode = simuNode.createChild('visualization')
        self.oglNode = oglNode
        oglNode.createObject('OglModel', color='1 0 0 1')
        oglNode.createObject('BarycentricMapping')

        return 0



    def initGraph(self, node):
        print 'Init graph called (python side)'
        self.step = 0
        self.total_time = 0
        return 0



    def onBeginAnimationStep(self, deltaTime):
        ### apply external impact
        self.step += 1
        if 'applied_periodic_force' in self.opt['model'].keys():
            # maxTS = self.opt['model']['applied_force']['num_inc_steps']
            # delta = np.array(self.opt['model']['applied_force']['delta'])
            per=self.opt['model']['applied_periodic_force']['period']
            amp=self.opt['model']['applied_periodic_force']['amplitude']
            arg=2*math.pi * self.step / per
            actualForce = np.array(amp) * math.sin(arg)
            self.appliedForce.findData('force').value = actualForce.tolist()
        return 0;



    def onEndAnimationStep(self, deltaTime):
        ### save filtering data to files
        if self.saveEst:
            stateName = 'reducedState' if self.filterKind == 'ROUKF' else 'state'
            varName = 'reducedVariance' if self.filterKind == 'ROUKF' else 'variance'
            covarName = 'reducedCovariance' if self.filterKind == 'ROUKF' else 'covariance'

            rs=self.filter.findData(stateName).value
            state = [val for sublist in rs for val in sublist]
            print 'State:', state
            # print reducedState

            f1 = open(self.stateExpFile, "a")
            f1.write(" ".join(map(lambda x: str(x), state)))
            f1.write('\n')
            f1.close()

            rv=self.filter.findData(varName).value
            variance = [val for sublist in rv for val in sublist]
            print 'Stdev: ', np.sqrt(variance)
            # print 'Reduced variance:'
            # print reducedVariance

            f2 = open(self.stateVarFile, "a")
            f2.write(" ".join(map(lambda x: str(x), variance)))
            f2.write('\n')
            f2.close()

            rcv=self.filter.findData(covarName).value
            covariance = [val for sublist in rcv for val in sublist]
            # print 'Reduced Covariance:'
            # print reducedCovariance

            f3 = open(self.stateCovarFile, "a")
            f3.write(" ".join(map(lambda x: str(x), covariance)))
            f3.write('\n')
            f3.close()

        # print self.basePoints.findData('indices_position').value

        return 0

    def cleanup(self):
        if self.saveEst:
            print 'Estimations saved to '+self.estFolder
        if self.saveGeo:
            print 'Geometries saved to '+self.geoFolder
        return 0;

    def onScriptEvent(self, senderNode, eventName, data):
        return 0;

