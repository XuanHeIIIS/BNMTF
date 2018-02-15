"""
Test the performance of non-probabilistic NMF for recovering a toy dataset, where 
we vary the fraction of entries that are missing.

We use the correct number of latent factors and same priors as used to generate the data.

I, J, K, L = 100, 50, 10, 5
"""

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../"
sys.path.append(project_location)

from BNMTF.code.models.nmtf_np import NMTF
from BNMTF.data_toy.bnmtf.generate_bnmtf import try_generate_M
from BNMTF.code.cross_validation.mask import calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

fractions_unknown = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95] #[ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]

input_folder = project_location+"BNMTF/data_toy/bnmtf/"

repeats = 10 # number of times we try each fraction
iterations = 1000
I,J,K,L = 100, 80, 5, 5

init_FG = 'kmeans'
init_S = 'exponential'
expo_prior = 1/10.

metrics = ['MSE', 'R^2', 'Rp']

# Load in data
R = numpy.loadtxt(input_folder+"R.txt")

# Seed all of the methods the same
numpy.random.seed(3)

# Generate matrices M - one list of M's for each fraction
M_attempts = 100
all_Ms = [ 
    [try_generate_M(I,J,fraction,M_attempts) for r in range(0,repeats)]
    for fraction in fractions_unknown
]
all_Ms_test = [ [calc_inverse_M(M) for M in Ms] for Ms in all_Ms ]

# Make sure each M has no empty rows or columns
def check_empty_rows_columns(M,fraction):
    sums_columns = M.sum(axis=0)
    sums_rows = M.sum(axis=1)
    for i,c in enumerate(sums_rows):
        assert c != 0, "Fully unobserved row in M, row %s. Fraction %s." % (i,fraction)
    for j,c in enumerate(sums_columns):
        assert c != 0, "Fully unobserved column in M, column %s. Fraction %s." % (j,fraction)
        
for Ms,fraction in zip(all_Ms,fractions_unknown):
    for M in Ms:
        check_empty_rows_columns(M,fraction)


# We now run the VB algorithm on each of the M's for each fraction.
all_performances = {metric:[] for metric in metrics} 
average_performances = {metric:[] for metric in metrics} # averaged over repeats
for (fraction,Ms,Ms_test) in zip(fractions_unknown,all_Ms,all_Ms_test):
    print "Trying fraction %s." % fraction
    
    # Run the algorithm <repeats> times and store all the performances
    for metric in metrics:
        all_performances[metric].append([])
    for (repeat,M,M_test) in zip(range(0,repeats),Ms,Ms_test):
        print "Repeat %s of fraction %s." % (repeat+1, fraction)
    
        # Run the VB algorithm
        nmtf = NMTF(R,M,K,L)
        nmtf.initialise(init_S,init_FG)
        nmtf.run(iterations)
    
        # Measure the performances
        performances = nmtf.predict(M_test)
        for metric in metrics:
            # Add this metric's performance to the list of <repeat> performances for this fraction
            all_performances[metric][-1].append(performances[metric])
    
    # Compute the average across attempts
    for metric in metrics:
        average_performances[metric].append(sum(all_performances[metric][-1])/repeats)
        

print "repeats=%s \nfractions_unknown = %s \nall_performances = %s \naverage_performances = %s" % \
    (repeats,fractions_unknown,all_performances,average_performances)


'''
repeats=10 
fractions_unknown = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] 
all_performances = {'R^2': [[0.9980343429144349, 0.995609618431885, 0.9949348087065104, 0.9982636881051925, 0.9980652353035467, 0.9975858464757429, 0.9982870148398022, 0.9979401506447826, 0.9984285716597046, 0.9981641744293244], [0.9978711565756241, 0.9951287961499744, 0.9955681745487412, 0.9977816392170151, 0.9976521250865921, 0.9980295403896086, 0.997967923476359, 0.998133275350781, 0.9977997887661408, 0.9976685147823149], [0.9974878783068148, 0.9977227798620565, 0.9964085132001691, 0.9979066461073346, 0.9976156756353801, 0.9977450435816912, 0.9979100744486454, 0.9978245838548117, 0.9978511881366197, 0.9978482327011712], [0.9977014482955708, 0.9977308797494522, 0.9979366179315533, 0.9974637696425553, 0.997567461760042, 0.997232480770134, 0.9978046385772357, 0.9958527869467003, 0.9976979457890558, 0.9976039928091303], [0.9972873791567107, 0.9974788313451, 0.9974874870493455, 0.9976407323409554, 0.9976075690681417, 0.9968273846950513, 0.9975191092280739, 0.9957221939684213, 0.9940014813239068, 0.9975382659486167], [0.9972760828563136, 0.9973243972377697, 0.9971832708219596, 0.9971215746756694, 0.9959736934524578, 0.9974774945714368, 0.996821475613117, 0.9969160552417984, 0.9974096115578959, 0.997158452666769], [0.9952929262598474, 0.9964297512630778, 0.9460503817431494, 0.9964772516678725, 0.9962207997347254, 0.9963726980531884, 0.9966501497043366, 0.9963737293018352, 0.9966902187552384, 0.9962939159188997], [0.9830150098355507, 0.9874911795421858, 0.8936347493707586, 0.9877260361953338, 0.9909088566617611, 0.9539134425722242, 0.9929213967933344, 0.9899306534387379, 0.9915779962418456, 0.9886991669119036], [0.5248515363916246, -7.024220602118414e+52, 0.7794147157383904, 0.5655423577728611, 0.7067000089738362, 0.36084588195959366, 0.6642642108143817, 0.7581320210169895, 0.7448099035778358, 0.7934430488340981]], 'MSE': [[1.1117273217378305, 2.3256773636075838, 2.9998561716900229, 1.1098033050993086, 1.0948085435040582, 1.2827467330013105, 1.1913980300490594, 1.3028129274095495, 1.1661385896617491, 1.2842719862649354], [1.2245273456719461, 2.3136521304393223, 2.4610859524398383, 1.2236548175424988, 1.2180003141282578, 1.1731739638750209, 1.2046935743663822, 1.2806399258355881, 1.2680535334083713, 1.389284693705213], [1.2588366636023249, 1.2841200803571773, 2.266613268725413, 1.1768216450733573, 1.2377841468514552, 1.2734553909153328, 1.249335830894494, 1.2854355430335669, 1.2189422766194737, 1.2666054721024202], [1.2908570246570437, 1.3556280072018361, 1.2710824575159441, 1.3213661147982978, 1.3277951257577973, 1.4858258783528859, 1.320584587958312, 2.496345993882279, 1.3198053691046701, 1.2930205186768902], [1.4757018569434037, 1.3833886749310353, 1.44261511794411, 1.4716594488218024, 1.374673050139454, 1.7637131189789428, 1.3490298959990301, 2.4682230761075292, 3.1875323257963935, 1.4526496250295395], [1.5802395951361314, 1.5169576690580031, 1.579972485028267, 1.6345701428905648, 2.1646134699942974, 1.5139838888367847, 1.6693633434318642, 1.627937462063324, 1.4939395117947363, 1.6318822480375663], [2.6462347938031714, 1.9774539650171108, 30.404288995593351, 2.0678630459146747, 2.2019393825194209, 2.0155135038322074, 1.8379413250731671, 2.1417047615223836, 1.8689874228503611, 2.1469989037293975], [10.00351199232586, 7.0374960093009928, 61.312164632958066, 7.2479063248142719, 5.1383066740763077, 25.786585434786456, 4.0860549464388924, 5.9186700417560267, 4.8378237060334861, 6.4192980730779574], [277.54525146528437, 4.0054170095568005e+55, 125.49911986794422, 248.68429881964471, 168.28248872197133, 366.69536847829045, 193.99197205474707, 138.75847806416536, 141.69537167011299, 118.56358302693702]], 'Rp': [[0.99901831033550148, 0.99780267323418492, 0.99746532993847858, 0.99913184513114062, 0.99903476674991853, 0.99880402516521027, 0.99914522989985854, 0.99897248918732606, 0.99921789276757178, 0.99908661815973598], [0.99893681373087895, 0.99758801048588652, 0.99778177276524527, 0.99889553637877282, 0.99882707580567365, 0.99901455166763853, 0.99898429732255611, 0.99906725758542458, 0.99890242410479768, 0.99883689243690521], [0.99874389090697591, 0.99886115746120463, 0.99820283070307547, 0.99895416759157307, 0.99881468578807919, 0.99887202005848885, 0.99895486890826601, 0.99891177416512533, 0.99892518952847609, 0.99892397729039517], [0.9988504461615394, 0.99886535314254665, 0.99896950233159876, 0.99873324352209936, 0.99878342543591769, 0.99861580778971792, 0.99890278482331929, 0.99792672022315521, 0.99885055131867329, 0.99880184616905998], [0.9986455214633525, 0.99874135118538232, 0.99874445271605405, 0.99882057829495607, 0.99880509920628302, 0.99841739036749755, 0.99876029963181223, 0.99787641705417718, 0.99700267143790289, 0.99877110190618346], [0.9986420737099263, 0.99866166298444703, 0.99859088348326819, 0.99856286714576636, 0.99798913092482722, 0.99873865443757215, 0.99841445921822869, 0.99845946526067653, 0.99870415634755061, 0.99857935368159356], [0.99765801147108923, 0.99821463763173846, 0.97369867754965167, 0.99823846555228446, 0.99810891026453552, 0.99818580924244882, 0.99832436981576389, 0.99820000427266786, 0.99835221365309634, 0.99814790541981058], [0.99163850472123882, 0.99374088005539329, 0.95099812872284506, 0.99386323564774937, 0.99544851212496843, 0.97746944649188028, 0.99646362300198033, 0.99498800160241041, 0.99578162502496104, 0.99442329673681795], [0.82217943237744207, 0.0086490164132459486, 0.89763285493411682, 0.79763928882156299, 0.87052056847973192, 0.81024677391454336, 0.84867623154677641, 0.89351663603146692, 0.88580704312138958, 0.90926055138610729]]} 
average_performances = {'R^2': [0.9975313451510924, 0.9973600934343152, 0.9976320615834695, 0.997459202227143, 0.9969110434124323, 0.9970662108695187, 0.9912851822402171, 0.9759818487563635, -7.024220602118413e+51], 'MSE': [1.4869240972025408, 1.4756766251412441, 1.3517950318175014, 1.4482311077905954, 1.7369186190691241, 1.6413459816271536, 4.9308926099855253, 13.778781783556832, 4.0054170095568004e+54], 'Rp': [0.99876791805689291, 0.99868346322837787, 0.99881645624016591, 0.99872996809176284, 0.99845848832636008, 0.99853427071938561, 0.99571290048730854, 0.98848152541302436, 0.7744128397026383]}

repeats=10 
fractions_unknown = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95] 
all_performances = {'R^2': [[0.9962063945066817, 0.9952117860440499, 0.9954751339964156, 0.9960098290923545, 0.9963955556694212, 0.9978892486245532, 0.9928980680212569, 0.9970063645728976, 0.9960648669613977, 0.9946485164619207], [0.9981371973903026, 0.9967864075747161, 0.9961049591417127, 0.9979163030563502, 0.9972685687369583, 0.9958623365262758, 0.995462664836765, 0.9957846983440475, 0.9969554513882282, 0.9959799650009298], [0.9958338895174539, 0.9972157313221351, 0.9978899753236734, 0.9974220954889335, 0.9952318509517915, 0.9961471219924026, 0.9975367173888783, 0.9953352798433481, 0.9978626483303038, 0.9940083607657426], [0.995882980890237, 0.9950422974054679, 0.9976331866124758, 0.9953716523625389, 0.9970176559478298, 0.9971472250769187, 0.9972282381990349, 0.9954657122093548, 0.9940886324475817, 0.9949353089634675], [0.9956461754981152, 0.9960253762659874, 0.9956196891949282, 0.9953023471085498, 0.9948675813628644, 0.9957778952907087, 0.9978155274130537, 0.9962673381561962, 0.9960550011548281, 0.9955981822642457], [0.99592259909498, 0.997663756806484, 0.9962296790863876, 0.9956478565392816, 0.9958678701351467, 0.9964957219221171, 0.9967792305176417, 0.995089723428762, 0.9971694417396728, 0.9979325866167374], [0.9949737140760235, 0.9956983603137102, 0.9956630495680359, 0.9955841280156259, 0.9963849288081821, 0.9976620900297413, 0.9955765636811043, 0.9966893569405892, 0.9955927097128661, 0.9952997550121442], [0.9972382928845018, 0.9952714483490777, 0.9948628680038072, 0.996200078178459, 0.995852448919139, 0.9948276943608685, 0.994824490068884, 0.995413158441782, 0.9957727671223241, 0.9957730639190467], [0.9952465804489504, 0.9977358908950131, 0.9953391639661217, 0.9955246271653274, 0.9970071651516105, 0.9956761478121187, 0.9971833440944355, 0.9951203921701669, 0.995233601664906, 0.9972323956726123], [0.9968668098499075, 0.9969358362327682, 0.9965388696837818, 0.9946481850681989, 0.99750446152684, 0.9950606809652205, 0.9970341186597591, 0.9962884149201763, 0.9952550037240914, 0.9953887884888017], [0.9971495971377476, 0.9945765082628745, 0.9954586232484604, 0.995013165659572, 0.9971895051660294, 0.9974840063941564, 0.9946708916134598, 0.9954140813542034, 0.9945691478999277, 0.9969308767820141], [0.9951156883843166, 0.9945869140557536, 0.9972781531372162, 0.9969896440022914, 0.9970302907262817, 0.995166340740021, 0.9939736473020614, 0.9946055054251018, 0.9950262790978491, 0.9951896130621724], [0.9945074945811259, 0.9963313309835414, 0.9959624695553247, 0.9943848688128225, 0.9958373466550637, 0.9944367070366555, 0.9962567476646124, 0.9945805102815026, 0.9949503638665529, 0.9945522436748129], [0.9801500158464631, 0.99449884522877, 0.9942781096393166, 0.9956882904922659, 0.9955931180038949, 0.996004134688716, 0.9945382877181, 0.9938658068918859, 0.994293853841724, 0.9936604101959295], [0.9935678014517111, 0.9932574344125626, 0.9901623220963821, 0.9863843702589428, 0.9685747520243158, 0.9938368847987423, 0.9930368515140815, 0.9935793493135131, 0.9919734871251957, 0.9929998561715981], [0.9895491882192277, 0.9756234686817539, 0.9793998127934948, 0.9886046175655753, 0.9575717263436173, 0.9747675131695464, 0.9673757504696554, 0.982078324247234, 0.9744142272621655, 0.8954502610566232], [0.886570952388983, 0.9386961308748675, 0.8984517594794402, 0.9007111871319804, 0.9351693222009404, 0.9803574318940305, 0.9843660429618423, 0.8173488261470822, 0.9174641971253716, 0.8832784089401231], [0.770204017331025, 0.7210630452231155, 0.730403080569797, 0.7529502664361041, 0.7552947969076185, 0.8793520157680721, 0.8465459736316541, 0.8709576248612239, 0.8670556148322343, 0.8086582503614737], [0.6487950095334953, 0.6422692009132736, 0.5305531520437426, 0.6313225023671221, 0.6413529985994542, 0.6892896376461888, 0.6678619623174173, 0.7405230008470852, 0.4276942243413684, 0.7267407003838806]], 'MSE': [[2.1173723883692883, 3.193814808329372, 2.448282520157727, 2.6297125009937918, 2.0343284006701992, 1.2839455004694693, 3.3857797651730577, 1.3567688251004626, 1.8058277114902992, 2.3107589704934242], [1.2471859506206149, 2.185129612688681, 2.2197917557964435, 1.1811226752431248, 1.3273199593780669, 2.2522668267756756, 2.2391094929178736, 2.4904964222302555, 2.0367423951705446, 2.5251065275546365], [2.3850391038429102, 1.608332738838089, 1.2520832694995618, 1.3387311924283627, 2.5654617046736647, 2.3131660722593876, 1.4476853702316796, 2.3857413873584585, 1.2447511224206065, 3.0504806768194559], [2.5388842720556628, 2.6151972964295673, 1.2983850353050377, 2.5660309914137116, 1.7284602538015852, 1.5090468672231554, 1.6818074137622878, 2.3957198038034946, 2.5931619670684687, 2.5162165242806749], [2.3997913705706355, 2.4809781404937561, 2.5857856708207629, 2.6130439878538478, 2.7532964957562052, 2.3720336611567112, 1.3140707640987459, 2.2253948543183584, 2.74301363358849, 2.4864950356673057], [2.3507308183110811, 1.3079876448153482, 2.3970136318573272, 2.4099087273593827, 2.6605669003160752, 2.2613178693944915, 1.9816754604697322, 2.6490641111807887, 1.773839402304122, 1.2737033841024499], [2.7107740964264737, 2.4501682404434741, 2.5470310536566494, 2.419008010802504, 1.8942930041729593, 1.4665636007336595, 2.3151873475611109, 2.1782297674089461, 2.6011468108850013, 2.5476762660654395], [1.6550739848990221, 2.7297757863493963, 2.9326112742471899, 2.0909890543822507, 2.4395229115458323, 2.732220315058727, 2.853637078555487, 2.5140372233774153, 2.5550289073743011, 2.4870594529835439], [2.8059433667540588, 1.3131431959947197, 2.5621409549239096, 2.7510578749645314, 1.6451080711087924, 2.4121645906988225, 1.5856122030730515, 2.856784927931701, 2.8337275432278455, 1.6351790541430744], [1.8123275809937061, 1.8395419053965441, 2.0259623887907252, 2.8421768477089198, 1.391777409137934, 2.6636824106775259, 1.702260791985541, 2.174976479386221, 2.6340700250732305, 2.803232641330005], [1.5974054482430669, 2.9387027155927612, 2.6363823912314461, 2.8955332936589651, 1.5962231394966184, 1.4385160409888782, 2.8787698160216788, 2.6948051878902657, 3.0660212588955007, 1.7831162868805479], [2.9093961795176537, 3.1935115794981859, 1.5987895971831865, 1.6857837224109846, 1.7417441925024142, 2.8407720482578376, 3.5052132841924024, 3.0963737363643227, 2.9757877739113252, 2.9960071399840653], [3.0030813516560309, 2.1509894694192275, 2.2973446377874573, 3.3086711764771595, 2.3272315725825026, 3.2532357860075032, 2.0949265504753494, 3.0286290793794031, 2.9770981067374085, 3.1867936539589841], [11.40773455763537, 3.1031120008458442, 3.307037229497944, 2.3613328967169167, 2.5812072134147193, 2.3287235803959816, 3.101119042330565, 3.5729623502077428, 3.3143176922223323, 3.6740349513423665], [3.4767164594592637, 3.8756657265561527, 5.5688979763577482, 7.7971486167742281, 17.927830546091666, 3.5448240210926456, 4.0878861946887639, 3.6891269976335019, 4.7424405570560326, 3.9401806015099656], [6.0597086045913491, 13.61876296355222, 11.87828085352249, 6.6282237092920733, 24.953688218084938, 14.070022712752946, 18.646126889151681, 10.170059954171357, 14.830196003216651, 59.918776757578996], [64.251683006658965, 34.913144668199678, 57.786110138866363, 59.057010748959179, 35.563009167256993, 11.184688439410566, 8.9777121542854896, 101.36626749010232, 48.4078025309555, 66.450052701527056], [132.88190760313276, 163.18243788501226, 154.87754728195193, 142.21735914663051, 142.35972760057879, 69.096737303534951, 88.695195567448664, 74.007593443805547, 77.720121574047482, 110.94483947540073], [201.92213201634607, 207.45752965693751, 265.38342741342132, 209.31553963738176, 206.59915390578306, 173.57730442169114, 189.19916724529895, 145.98124085063219, 323.88844304737904, 157.64892698216559]], 'Rp': [[0.99810200238272762, 0.99761135611540253, 0.99774973391230803, 0.99800436487068755, 0.99821192856449481, 0.99894668830273503, 0.99654889357590482, 0.99850617085046722, 0.99804556534795097, 0.99732724641425941], [0.99906936292934112, 0.99840343524805619, 0.99805125242587711, 0.99895802435856007, 0.99863713178110358, 0.99795116968481534, 0.99773550169110681, 0.99789786006485015, 0.99848528872859166, 0.99799513993361533], [0.99791680344818179, 0.99861539185212767, 0.99894511272306308, 0.99871155064996286, 0.997630232654664, 0.99807763758578727, 0.99876865831200468, 0.99768182936748862, 0.99893089357934972, 0.99700256647963026], [0.99794900083218208, 0.99753064720788054, 0.99881637030886461, 0.9976836377119187, 0.99851042654273137, 0.99857550573124543, 0.99862994727409282, 0.99773931973575969, 0.99705536489399538, 0.99746633103505888], [0.99782313432175773, 0.99801575519353924, 0.99781164458134386, 0.99764936717332131, 0.99743098372607919, 0.99788982180496499, 0.99890790440123489, 0.99814024855201278, 0.99802937957561699, 0.99779777479935061], [0.99795996491450101, 0.99883185647221129, 0.99811548838022035, 0.99783549849715181, 0.99794241538180706, 0.99825785160466873, 0.99839558697020458, 0.99754317568762096, 0.99858399954705901, 0.99896651342421772], [0.99748389187577013, 0.9978471754243009, 0.99783006596343415, 0.99779081214235454, 0.99819121498066066, 0.99883049268767798, 0.99778656843659053, 0.99834427702806472, 0.99780479917557818, 0.99764771429102739], [0.99862259556841249, 0.99763731381805387, 0.99743588492631508, 0.99810309229881766, 0.99792483645384222, 0.99741985920171494, 0.99741644981457966, 0.99770480619671276, 0.99788439553728947, 0.99788625455284852], [0.99762149235995301, 0.99886781621688325, 0.99767269393710256, 0.99776077060451984, 0.99850496213725026, 0.99783589873654333, 0.99859198420215778, 0.99756384414085075, 0.99761544611101627, 0.99861630036959159], [0.99843303783713266, 0.99846908176434723, 0.99827945039381993, 0.99732623989524949, 0.99875147131127617, 0.99752976153223583, 0.9985182005594585, 0.9981471332798898, 0.99762819014456938, 0.99769514913226987], [0.99857425959737423, 0.99729143290855327, 0.9977272662859954, 0.99751110916918484, 0.99859473194949644, 0.99874174234411894, 0.99733473103465753, 0.99770817749847096, 0.99728387456758028, 0.99846594514346998], [0.99755895086361712, 0.99730035278931572, 0.99863845588394984, 0.99849482509257936, 0.99851566600091146, 0.99758599730716779, 0.99698228009244216, 0.99731616363742415, 0.99751092420822851, 0.99759216285709729], [0.99725708457334961, 0.99816398610349721, 0.99798285840639389, 0.99721078801533769, 0.99791818004433641, 0.99722009196335515, 0.99814473498784495, 0.99729296110935717, 0.99747671421559958, 0.99728165294550797], [0.99040480405222098, 0.99724661593629804, 0.99714037780173126, 0.99784594540720284, 0.99779534286293425, 0.99800091155751802, 0.99726990031710783, 0.9969479276246932, 0.99714824728911777, 0.99682602471623494], [0.99679760046678378, 0.99662850799937253, 0.99507210121142142, 0.99321514666298438, 0.98455928172238172, 0.99691406892798473, 0.99652989521316537, 0.99678718399226851, 0.99598910970521959, 0.99649651344396228], [0.99476138936053482, 0.98774794368627761, 0.98968339965245433, 0.99430334028126266, 0.97875763111257086, 0.98740987131287228, 0.98428597571263488, 0.99100494540804385, 0.98714719726364686, 0.95333824168682368], [0.94746885819437066, 0.97097786231867866, 0.94931237407951219, 0.95009504660308919, 0.96887852561255872, 0.99016901754617392, 0.99217617822752524, 0.91325898512923276, 0.95938084219284392, 0.94333606745047394], [0.90564585331309333, 0.86573146866485717, 0.8764413435787004, 0.88156927432077459, 0.87631502677332174, 0.94118904106620216, 0.92172601149193567, 0.93523410552270825, 0.9313050516274215, 0.91719490294270012], [0.83767825528794693, 0.84337794445225445, 0.79655012678040593, 0.82949191287563073, 0.81737894325544258, 0.86416766859217042, 0.84186252423579955, 0.89250011397106288, 0.80279940095954361, 0.86554645853794498]]} 
average_performances = {'R^2': [0.9957805763950949, 0.9966258551996285, 0.9964483670924664, 0.9959812890114907, 0.9958975113709478, 0.9964798465887211, 0.9959124656158023, 0.9956036310247889, 0.9961299309041263, 0.9961521169119545, 0.9958456403518445, 0.9954962075933065, 0.9951800083112013, 0.9932570872547066, 0.9897373109167045, 0.9684834889808892, 0.9142414259144662, 0.8002484685922319, 0.6346402388993029], 'MSE': [2.2566591391247091, 1.9704271618375919, 1.9591472638372174, 2.1442910425143649, 2.3973903614324819, 2.1065807950110802, 2.3130078198156219, 2.4989955988773165, 2.2400861782820503, 2.1890008480480354, 2.3525475578899728, 2.6543379253822379, 2.7628001384481022, 3.8751581514609783, 5.8650717697219967, 18.07738466659147, 48.795748104622213, 115.59834668815438, 208.09728651770371], 'Rp': [0.9979053950336938, 0.99831841668459165, 0.99822806766522587, 0.99799565512737287, 0.9979496014129221, 0.9982432350879662, 0.997955701200546, 0.99780354883685884, 0.99806512088158672, 0.99807777158502486, 0.99792332704989017, 0.99774957787327345, 0.997594905236458, 0.996662609756506, 0.99489894093455433, 0.98484399354771224, 0.95850537573544603, 0.90523520793017165, 0.83913533489482028]}
'''


# Plot the MSE, R^2 and Rp
for metric in metrics:
    plt.figure()
    x = fractions_unknown
    y = average_performances[metric]
    plt.plot(x,y)
    plt.xlabel("Fraction missing")
    plt.ylabel(metric)