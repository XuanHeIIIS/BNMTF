"""
Recover the toy dataset using VB.

We can plot the MSE, R2 and Rp as it converges, on the entire dataset.

We have I=100, J=80, K=10, and no test data.
We give flatter priors (1/10) than what was used to generate the data (1).
"""

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../"
sys.path.append(project_location)

from BNMTF.code.models.bnmf_vb_optimised import bnmf_vb_optimised
from BNMTF.code.cross_validation.mask import calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

input_folder = project_location+"BNMTF/data_toy/bnmf/"

iterations = 200
init_UV = 'random'
I, J, K = 100,80,10

alpha, beta = 1., 1. #1., 1.
lambdaU = numpy.ones((I,K))/10.
lambdaV = numpy.ones((J,K))/10.
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

# Load in data
R = numpy.loadtxt(input_folder+"R.txt")
M = numpy.ones((I,J))

# Run the VB algorithm
BNMF = bnmf_vb_optimised(R,M,K,priors) 
BNMF.initialise(init_UV)
BNMF.run(iterations)

# Plot the tau expectation values to check convergence
plt.plot(BNMF.all_exp_tau)

# Extract the performances across all iterations
print "vb_all_performances = %s" % BNMF.all_performances

'''
vb_all_performances = {'R^2': [-568.0441214850692, -12.065852161733632, 0.6111142176390654, 0.6894727007761771, 0.6951151587124467, 0.7140397612742699, 0.741486061398124, 0.782495217302652, 0.8313128853081553, 0.8673627766103285, 0.897742949965608, 0.9180503048267509, 0.9283212088415719, 0.9359944056403732, 0.9417187787639725, 0.9457969724545253, 0.9491240552388082, 0.9521576020891553, 0.9549908845882131, 0.9574710738106214, 0.9594491066391847, 0.9610401416698016, 0.9624170042282227, 0.9637617489842852, 0.9651896707439098, 0.9667311961174231, 0.9682983494540904, 0.9697296489752586, 0.9709019074543284, 0.9718007051019989, 0.9724932868823896, 0.9730521945190864, 0.9735268346202028, 0.9739471883846382, 0.9743302321028442, 0.974685007173449, 0.9750153121522791, 0.9753227285189114, 0.975608529492046, 0.9758741447925515, 0.9761211356412153, 0.9763510346644863, 0.9765651770221175, 0.9767646493003674, 0.9769503317466575, 0.9771229598122498, 0.9772831769645078, 0.9774315727631061, 0.9775687101971214, 0.9776951592093992, 0.9778115382595417, 0.9779185400005043, 0.9780169193493262, 0.978107448860463, 0.9781908732982757, 0.9782678838544773, 0.9783391084045955, 0.9784051097945933, 0.9784663883928548, 0.9785233871923971, 0.9785764980721009, 0.978626068072364, 0.9786724049553961, 0.9787157817140666, 0.9787564400086535, 0.978794592823345, 0.9788304269371362, 0.9788641059198493, 0.9788957740686497, 0.978925561023805, 0.9789535861934707, 0.9789799620675763, 0.9790047960085886, 0.9790281907249236, 0.9790502439701448, 0.979071048008406, 0.9790906891991117, 0.9791092478452783, 0.9791267983036324, 0.9791434092833489, 0.979159144245169, 0.9791740618281334, 0.9791882162573484, 0.9792016577111419, 0.9792144326441383, 0.9792265840729626, 0.9792381518345805, 0.9792491728258934, 0.979259681229618, 0.9792697087277749, 0.9792792847016472, 0.9792884364162566, 0.9792971891879599, 0.9793055665350398, 0.979313590312493, 0.9793212808331668, 0.9793286569777933, 0.9793357362963564, 0.9793425351027568, 0.9793490685641063, 0.9793553507853534, 0.9793613948894441, 0.9793672130929062, 0.9793728167766124, 0.9793782165515034, 0.9793834223191643, 0.9793884433273122, 0.9793932882203925, 0.9793979650856104, 0.9794024814947888, 0.9794068445424802, 0.979411060880749, 0.979415136751018, 0.9794190780133274, 0.9794228901733059, 0.9794265784071138, 0.9794301475845706, 0.9794336022906496, 0.9794369468454968, 0.9794401853231138, 0.9794433215688333, 0.9794463592157026, 0.9794493016998961, 0.9794521522752522, 0.9794549140270244, 0.9794575898849128, 0.9794601826354147, 0.979462694933502, 0.9794651293136105, 0.9794674881999014, 0.979469773915751, 0.9794719886924238, 0.9794741346769037, 0.979476213938879, 0.9794782284769036, 0.9794801802237818, 0.9794820710512376, 0.9794839027739307, 0.9794856771528705, 0.9794873958982585, 0.9794890606717508, 0.9794906730881104, 0.9794922347161881, 0.9794937470791796, 0.9794952116541448, 0.9794966298708485, 0.9794980031101252, 0.9794993327021102, 0.9795006199248439, 0.9795018660038507, 0.9795030721132844, 0.9795042393790817, 0.9795053688842761, 0.9795064616762337, 0.9795075187751828, 0.9795085411831269, 0.9795095298921106, 0.9795104858909198, 0.9795114101695597, 0.9795123037212301, 0.9795131675418864, 0.9795140026277698, 0.9795148099714728, 0.9795155905571652, 0.979516345355559, 0.9795170753190948, 0.979517781377695, 0.9795184644352969, 0.9795191253672696, 0.9795197650187175, 0.9795203842036193, 0.9795209837046943, 0.9795215642738688, 0.979522126633201, 0.9795226714761189, 0.9795231994688377, 0.979523711251839, 0.9795242074413141, 0.9795246886304989, 0.9795251553908578, 0.9795256082730889, 0.9795260478079549, 0.9795264745069496, 0.9795268888628252, 0.9795272913500148, 0.9795276824249765, 0.9795280625264927, 0.9795284320759514, 0.9795287914776287, 0.979529141118988, 0.9795294813710105, 0.979529812588556, 0.9795301351107646, 0.97953044926149, 0.9795307553497672, 0.9795310536703082, 0.9795313445040208, 0.9795316281185417, 0.9795319047687855, 0.9795321746974959], 'MSE': [22376.091062522872, 513.77861002661143, 15.291861123737212, 12.210629830772911, 11.98875573027447, 11.24459791498893, 10.165347839796285, 8.5527758576411284, 6.6331556673817538, 5.2155930916252373, 4.020976541121426, 3.2224458043025868, 2.8185708236942584, 2.5168435167456336, 2.2917483273686887, 2.1313846052160659, 2.0005562484282358, 1.8812703828812023, 1.7698593607634165, 1.6723327581722844, 1.5945520711825247, 1.5319890055351069, 1.4778476818229724, 1.4249693021307679, 1.3688202161159047, 1.3082039812220225, 1.2465799973406133, 1.1902980901664924, 1.1442022577237878, 1.10885951846735, 1.0816256495964769, 1.0596481478491047, 1.0409842345891143, 1.0244549818363862, 1.0093928437773283, 0.99544229234056247, 0.98245395979190153, 0.97036565880757453, 0.95912732357281905, 0.94868273425661342, 0.93897050015623018, 0.92993035496244236, 0.9215097971993722, 0.91366609985843583, 0.90636464963686925, 0.89957652694163681, 0.89327642919289518, 0.88744117358201779, 0.88204862211588664, 0.87707636336359818, 0.87250007810655439, 0.86829252967713133, 0.86442403304427728, 0.86086420963417654, 0.85758377364185723, 0.85455554585902105, 0.85175483681176034, 0.84915951413451563, 0.84674990222022983, 0.84450858158997266, 0.84242014268726872, 0.84047093910537662, 0.83864886894396817, 0.83694319751119073, 0.83534442218293037, 0.83384416794323579, 0.83243509022314255, 0.83111075709038951, 0.82986549445681668, 0.82869420457635523, 0.82759219205253332, 0.82655503352904325, 0.82557850727290794, 0.82465857455885117, 0.82379139149753389, 0.82297333005550466, 0.82220099438729832, 0.82147122679820905, 0.82078110341499078, 0.82012792243878796, 0.81950918845092902, 0.81892259563283276, 0.8183660117317002, 0.81783746362314491, 0.81733512460714908, 0.81685730317354255, 0.81640243284349301, 0.81596906274809133, 0.81555584874624931, 0.81516154502986993, 0.81478499626099743, 0.81442513031783126, 0.81408095170445738, 0.81375153562924674, 0.81343602270471416, 0.81313361418414498, 0.81284356763481658, 0.81256519295199936, 0.8122978486365271, 0.8120409382835504, 0.81179390725485978, 0.81155623952678946, 0.811327454718069, 0.81110710530725727, 0.81089477404836752, 0.81069007158886774, 0.81049263428778429, 0.81030212222613662, 0.81011821739687762, 0.80994062205894879, 0.80976905723863879, 0.80960326136184757, 0.80944298900184086, 0.80928800972869375, 0.80913810704874001, 0.80899307742374271, 0.80885272936148112, 0.8087168825705231, 0.80858536717303708, 0.80845802297013858, 0.80833469875473529, 0.80821525166725083, 0.8080995465895966, 0.80798745557355511, 0.80787885730004061, 0.80777363656667189, 0.80767168380213028, 0.80757289460695891, 0.80747716932146318, 0.80738441262218796, 0.80729453314876776, 0.8072074431628713, 0.8071230582402803, 0.80704129699621452, 0.80696208084304499, 0.80688533377857452, 0.80681098220241698, 0.80673895475808854, 0.80666918219874284, 0.80660159727542446, 0.80653613464808971, 0.80647273082063153, 0.80641132410232819, 0.80635185459769754, 0.80629426422543571, 0.80623849676398773, 0.80618449791583324, 0.80613221537708823, 0.80608159889231989, 0.80603260027116641, 0.80598517334327102, 0.80593927383427122, 0.80589485915686776, 0.8058518881262704, 0.80581032062481417, 0.80577011725148129, 0.80573123899684551, 0.80569364697962942, 0.80565730227061594, 0.80562216581494783, 0.80558819844943363, 0.80555536099963954, 0.80552361443459164, 0.80549292005453266, 0.80546323968888944, 0.80543453588555636, 0.80540677207791034, 0.80537991272109399, 0.80535392339364276, 0.80532877086415233, 0.80530442312515671, 0.80528084939837874, 0.80525802011638214, 0.80523590688622615, 0.80521448244076677, 0.80519372058292504, 0.80517359612752659, 0.80515408484455431, 0.80513516340663371, 0.80511680934251106, 0.8050990009974982, 0.80508171750081103, 0.80506493873937679, 0.80504864533706266, 0.80503281863810228, 0.80501744069353853, 0.80500249424946035, 0.80498796273594619, 0.80497383025596159, 0.80496008157356458, 0.80494670210095476, 0.80493367788423564, 0.80492099558766794, 0.80490864247659322, 0.80489660639906524, 0.80488487576633871, 0.80487343953250534, 0.8048622871734753, 0.80485140866544047, 0.80484079446317214], 'Rp': [0.12198410261051881, 0.61223359333849892, 0.82071482587249067, 0.83139003862344685, 0.83401151710310295, 0.84537852506417299, 0.86163585518551367, 0.88543991966627045, 0.91283413553684001, 0.9323696303798048, 0.94841041724477582, 0.95873106092151461, 0.96385083319311604, 0.96774115313850007, 0.97062512114877531, 0.97268871182887495, 0.97438359365315441, 0.97593650679295774, 0.97738797909631869, 0.9786533666241789, 0.97965905713167623, 0.9804666621914998, 0.98116468455190631, 0.98184705298667463, 0.98257292658890616, 0.98335665862289057, 0.98415098260602807, 0.98487247549038792, 0.98545934694132775, 0.98590611986323395, 0.98624838801965731, 0.98652303499292826, 0.98675520004152162, 0.98696031894080127, 0.98714726485789583, 0.98732081421628026, 0.98748290034536623, 0.98763418461141517, 0.98777512489545294, 0.98790628584307238, 0.98802835053203941, 0.98814203209109552, 0.9882479731439604, 0.98834670538287794, 0.98843866101008437, 0.98852419874713604, 0.98860362841320393, 0.98867722988218654, 0.98874526825469333, 0.98880801494449777, 0.98886577383337304, 0.98891889367789232, 0.98896775495039346, 0.98901274182996646, 0.98905421965369644, 0.98909252504270107, 0.98912796350660881, 0.98916080969495146, 0.98919130888276818, 0.98921967934106581, 0.98924611514862959, 0.98927078896727705, 0.98929385445447537, 0.9893154481710027, 0.9893356909946629, 0.98935468920367464, 0.98937253554702431, 0.98938931068755964, 0.98940508525437576, 0.98941992236614262, 0.98943388012033706, 0.98944701348551967, 0.98945937531543782, 0.98947101657798542, 0.9894819861117784, 0.98949233023625816, 0.98950209243325271, 0.98951131319167995, 0.98952003001618138, 0.98952827755586314, 0.98953608779903646, 0.98954349028948585, 0.98955051233504687, 0.98955717919494379, 0.98956351424302635, 0.98956953911044432, 0.98957527381355559, 0.98958073687225889, 0.98958594542213207, 0.98959091532159893, 0.98959566125373588, 0.98960019682167433, 0.98960453463654885, 0.98960868639732313, 0.98961266296269612, 0.98961647441573009, 0.98962013012216687, 0.98962363878372039, 0.9896270084871811, 0.98963024675025058, 0.98963336056448614, 0.98963635643560954, 0.98963924042128515, 0.98964201816623965, 0.98964469493477092, 0.98964727564056976, 0.98964976487397038, 0.98965216692674907, 0.98965448581465187, 0.98965672529791626, 0.98965888889989362, 0.9896609799241467, 0.989663001470105, 0.98966495644747388, 0.98966684758957346, 0.9896686774656962, 0.98967044849256558, 0.98967216294502658, 0.98967382296600759, 0.98967543057578578, 0.98967698768071199, 0.98967849608130043, 0.98967995747991655, 0.98968137348797292, 0.98968274563272429, 0.98968407536377134, 0.98968536405920116, 0.98968661303134187, 0.98968782353232265, 0.98968899675916144, 0.98969013385856885, 0.9896912359313258, 0.98969230403630182, 0.98969333919400604, 0.98969434238983389, 0.98969531457692528, 0.98969625667861594, 0.98969716959072374, 0.98969805418342816, 0.98969891130288901, 0.98969974177261755, 0.98970054639439153, 0.98970132594885529, 0.98970208119551661, 0.98970281287238893, 0.98970352169496556, 0.98970420835485162, 0.98970487351815517, 0.9897055178239238, 0.98970614188299189, 0.98970674627762711, 0.98970733156233204, 0.98970789826590977, 0.98970844689475557, 0.98970897793718404, 0.9897094918681949, 0.98970998915428376, 0.98971047025762326, 0.98971093563932844, 0.98971138576152717, 0.98971182108815947, 0.98971224208468911, 0.98971264921698754, 0.98971304294955686, 0.98971342374348747, 0.98971379205436205, 0.98971414833027838, 0.989714493010037, 0.98971482652179854, 0.98971514928191162, 0.98971546169421154, 0.98971576414955953, 0.98971605702570009, 0.98971634068726377, 0.9897166154860666, 0.98971688176137329, 0.98971713984034948, 0.98971739003849712, 0.98971763266002488, 0.98971786799835137, 0.98971809633634655, 0.98971831794670373, 0.98971853309217217, 0.98971874202576038, 0.98971894499089375, 0.98971914222160118, 0.98971933394261802, 0.98971952036957189, 0.98971970170908785, 0.98971987815894413, 0.98972004990827556, 0.98972021713777814, 0.98972038001991702, 0.98972053871911314, 0.98972069339210345, 0.98972084418811213, 0.9897209912492001, 0.98972113471051704, 0.98972127470059723, 0.98972141134169178]}
'''

plt.figure()
plt.plot(BNMF.all_performances['MSE'])