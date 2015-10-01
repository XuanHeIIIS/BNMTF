"""
Run BNMTF with the Exp priors on the Sanger dataset.
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmtf_vb_optimised import bnmtf_vb_optimised
from load_data import load_Sanger

import numpy, matplotlib.pyplot as plt, random

##########

standardised = False #standardised Sanger or unstandardised

iterations = 1000
I, J, K, L = 622,139,30,20

init_S = 'random' #'exp' #
init_FG = 'kmeans' #'exp' #
tauFSG = {
    'tauF' : numpy.ones((I,K))*1.,
    'tauS' : numpy.ones((K,L))*1.,
    'tauG' : numpy.ones((J,L))*1.  
}

alpha, beta = 1., 1.
lambdaF = numpy.ones((I,K))/10.
lambdaS = numpy.ones((K,L))/10.
lambdaG = numpy.ones((J,L))/10.
priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }

# Load in data
(_,X_min,M,_,_,_,_) = load_Sanger(standardised=standardised)

# Run the Gibbs sampler
BNMTF = bnmtf_vb_optimised(X_min,M,K,L,priors)
BNMTF.initialise(init_S=init_S,init_FG=init_FG,tauFSG=tauFSG)
BNMTF.run(iterations)

# Plot the tau expectation values to check convergence
plt.plot(BNMTF.all_exp_tau)

# Print the performances across iterations (MSE)
print "vb_all_performances = %s" % BNMTF.all_performances['MSE']

'''
vb_all_performances = [3.6560497805224408, 3.0813292661709162, 3.0645411707818879, 3.0525658578677146, 3.0432294800433217, 3.0353147079925389, 3.0281758341302782, 3.0226092485114404, 3.0180924608167805, 3.0139127030767114, 3.0099122667795863, 3.0059787264911373, 3.0020059059602895, 2.9979235848542376, 2.9939857310808189, 2.9898185953423795, 2.9854832227763319, 2.9809603527304036, 2.97624979475611, 2.9711907503274269, 2.9658176056612779, 2.9601355444227435, 2.9541278594520368, 2.9477835971072976, 2.9412314889174089, 2.9352617225772626, 2.9292177423085928, 2.9227155371535689, 2.9155856674515941, 2.9076653346542143, 2.8987801998468714, 2.8887613557725276, 2.877929867013683, 2.8664188240201112, 2.853946443672462, 2.8404561369103098, 2.8264738197741579, 2.8126534805321883, 2.7994240587681447, 2.7867394981258542, 2.7738704133811085, 2.7607088513751723, 2.7472492349120992, 2.7335579408151376, 2.7199102127498063, 2.7068352201855417, 2.6940848737391012, 2.6817269337924143, 2.669756858405901, 2.6578316000013333, 2.6457385873537937, 2.6352039707814567, 2.6263373139507173, 2.6184511925159919, 2.611199879564492, 2.6044738437438752, 2.598200830592627, 2.5923243952235322, 2.5867990838311168, 2.5815867196158364, 2.5766545339890716, 2.5719729771397386, 2.5675132996735486, 2.563247301129044, 2.5591499223735945, 2.5552190232426533, 2.5514961756469443, 2.5479492727489572, 2.5445153560246223, 2.5411652671113889, 2.5378835587917732, 2.5346580967152756, 2.5314784647321011, 2.5283355753788883, 2.5252212175519877, 2.5221279788671471, 2.5190493573826367, 2.5159796537672854, 2.5129135330412247, 2.5098453426257246, 2.5067809227272497, 2.5037614603826319, 2.5007199273377827, 2.4976126544675603, 2.4944331098992083, 2.4911782709979646, 2.4878440708469833, 2.4844260739733337, 2.4809257035614043, 2.4773577135594618, 2.4737540989267566, 2.4701792139920662, 2.4666095633314615, 2.4630112926416063, 2.4593711122874291, 2.4556838142082782, 2.4519491165965084, 2.4481697200140573, 2.4443486552141542, 2.440487093172842, 2.4365839756035839, 2.4326371149794848, 2.4286446046552457, 2.4246059042360666, 2.4205223328853833, 2.4163969111727042, 2.4122338970306205, 2.4080382794948063, 2.403815130964206, 2.3995689988120903, 2.3953037201324006, 2.3910227364882082, 2.3867298159103272, 2.3824301769542031, 2.3781314718043607, 2.3738432998122976, 2.3695719276547158, 2.3653150625629031, 2.3610921489770931, 2.3569375784395401, 2.3528612189229094, 2.3488605113009573, 2.3449337782904451, 2.3410816686800642, 2.3373051211829856, 2.3336042769123884, 2.3299819419611127, 2.3264475393113844, 2.3230099146884546, 2.3196605347440284, 2.3163699005757441, 2.3131041171384816, 2.3098388634347544, 2.3065539242858808, 2.3033182263003829, 2.3000289882953253, 2.2965245371922194, 2.2930851183528502, 2.2898203348285544, 2.2867324823351622, 2.2837843562781512, 2.2809502521712557, 2.2782062737714202, 2.2755378060435718, 2.2729396825035399, 2.2704080121247978, 2.2679387349034092, 2.2655280687098336, 2.2631727111787008, 2.2608697941416125, 2.2586167584042793, 2.2564112368206284, 2.254250984534973, 2.2521338765877226, 2.250057965504205, 2.2480215350797716, 2.2460230719295247, 2.2440611613506314, 2.2421343925244104, 2.2402413320282495, 2.2383805592443196, 2.2365507290126176, 2.2347506305141955, 2.232979222000008, 2.2312356325229965, 2.2295191334064701, 2.2278290893503025, 2.2261649009982198, 2.2245259495991418, 2.222911550479524, 2.2213209195038264, 2.219753165351348, 2.2182073376733249, 2.2166825473541953, 2.215178094736681, 2.2136934856905413, 2.2122283166960508, 2.2107821486213015, 2.209354463389662, 2.2079446889741581, 2.2065522409149985, 2.2051765521555708, 2.2038170869594369, 2.2024733459888894, 2.2011448733806449, 2.1998312747526425, 2.1985322449522573, 2.1972475797369087, 2.1959771319675045, 2.194720719235236, 2.1934780512787668, 2.1922487251394505, 2.1910322832835596, 2.1898283248750485, 2.1886366514269846, 2.1874573625907296, 2.1862907927433848, 2.1851372956078143, 2.183997017604661, 2.1828697926704992, 2.1817551789542744, 2.1806525675723059, 2.1795612867988021, 2.1784806694500398, 2.1774100934866407, 2.1763490189402912, 2.1752970207839977, 2.1742537894982745, 2.1732190943775671, 2.1721927482306129, 2.17117460349484, 2.1701645748079788, 2.1691626704416147, 2.1681690060993568, 2.1671837699916541, 2.1662071553377249, 2.165239317699867, 2.1642803747659212, 2.1633304223621033, 2.1623895478325323, 2.1614578394239365, 2.160535366187109, 2.1596218197695309, 2.1587145439898645, 2.1578056502100114, 2.1568879340850122, 2.1559726215284307, 2.1551056253483334, 2.1542746101358072, 2.1534404402323051, 2.1525993041660749, 2.1517561584321103, 2.1509150437345674, 2.1500787162545856, 2.1492492151721208, 2.1484283145915981, 2.1476178021736683, 2.1468194857244884, 2.1460349218231851, 2.1452650897659691, 2.1445101226509506, 2.1437690938284462, 2.1430405522961848, 2.1423242449256037, 2.1416221856203941, 2.1409374721553371, 2.1402713044080666, 2.1396198614575352, 2.1389760884528934, 2.1383354233837659, 2.1376932399624575, 2.1370418213462887, 2.1363793365679227, 2.1357133715635195, 2.1350496403275354, 2.1343915499008133, 2.1337243753358086, 2.1329527133461808, 2.1320179346951926, 2.130885502597692, 2.1297321288744033, 2.1286240275667652, 2.1275867942879882, 2.1266190943573107, 2.1257067168890456, 2.1248347248152322, 2.1239927818589335, 2.1231748637492012, 2.122377466885379, 2.1215983129292937, 2.1208357263777908, 2.1200883843801508, 2.1193552099589841, 2.1186353104891724, 2.1179279331651579, 2.1172324316629489, 2.1165482419951904, 2.1158748655662318, 2.1152118576238927, 2.1145588196153025, 2.1139153940176132, 2.1132812603385824, 2.112656131649004, 2.1120397517949656, 2.1114318931760558, 2.1108323539466678, 2.1102409542026872, 2.1096575336277557, 2.109081953808432, 2.1085141039804625, 2.1079539038972306, 2.107401298505835, 2.1068562454962438, 2.1063187016213183, 2.1057886130265806, 2.1052659111426655, 2.1047505128643307, 2.1042423229771159, 2.1037412372475819, 2.1032471452983805, 2.1027599330047582, 2.102279484773951, 2.1018056868763209, 2.1013384336598295, 2.1008776374101426, 2.1004232377285974, 2.0999752000245073, 2.0995334945992252, 2.0990980606620084, 2.0986687662763095, 2.0982453638946161, 2.0978274373718824, 2.0974143751939884, 2.0970054516638381, 2.0966000377298912, 2.0961978102650844, 2.0957988080934156, 2.0954033306649356, 2.095011782094351, 2.0946245496203377, 2.0942419451514835, 2.0938642011479094, 2.0934915113974411, 2.0931241123753681, 2.0927623462470444, 2.0924065667449052, 2.0920569203865305, 2.091713290608086, 2.0913754400625306, 2.0910431212397969, 2.0907160958372661, 2.0903941341961971, 2.0900770250138629, 2.0897645859366505, 2.0894566660728118, 2.0891531411339734, 2.0888539059167908, 2.0885588677257365, 2.0882679419023589, 2.0879810490711423, 2.0876981133598838, 2.0874190611290881, 2.0871438200878565, 2.086872318843338, 2.0866044869635965, 2.0863402556298412, 2.0860795589658592, 2.0858223361346075, 2.0855685342274177, 2.0853181116823238, 2.0850710412179989, 2.0848273101380892, 2.0845869155834515, 2.0843498544236128, 2.084116111017738, 2.0838856476919108, 2.083658401021395, 2.0834342839186508, 2.0832131915283498, 2.0829950085467108, 2.0827796160601753, 2.0825668966314632, 2.0823567369751563, 2.0821490282578026, 2.0819436648234011, 2.0817405427549764, 2.0815395597913797, 2.0813406175242282, 2.0811436256266069, 2.0809485066573781, 2.0807551994804321, 2.0805636599249904, 2.0803738586042693, 2.0801857769348993, 2.0799994027350022, 2.0798147263964335, 2.0796317380019635, 2.0794504253130799, 2.0792707724066464, 2.0790927587917225, 2.0789163589490114, 2.078741542295238, 2.0785682735604438, 2.0783965135092894, 2.0782262198834967, 2.0780573484302849, 2.0778898541515525, 2.0777237011479879, 2.0775589998541033, 2.0773968266300558, 2.0772404629819881, 2.0770932775391824, 2.0769550149963893, 2.0768231931267667, 2.0766957689622636, 2.0765716405100347, 2.0764502624105954, 2.076331329659828, 2.0762146335230631, 2.0761000096693243, 2.0759873216804845, 2.075876455569901, 2.0757673168148179, 2.075659827370111, 2.0755539221875616, 2.0754495455009012, 2.0753466473580615, 2.0752451808177521, 2.0751451000164542, 2.0750463590862416, 2.0749489117545896, 2.0748527114066966, 2.0747577114276736, 2.0746638657382901, 2.0745711295938465, 2.0744794609222685, 2.0743888224315512, 2.0742991827545247, 2.0742105067068137, 2.0741227123435859, 2.0740356018170583, 2.0739489091299075, 2.0738626000385296, 2.0737770477188184, 2.0736927137452406, 2.0736098000816212, 2.0735282385911726, 2.07344783239449, 2.0733683615870451, 2.0732896287207816, 2.0732114714542571, 2.0731337628029181, 2.0730564076780684, 2.0729793385353785, 2.072902510810203, 2.0728258982264172, 2.0727494880763691, 2.0726732767537279, 2.0725972659087315, 2.0725214595107144, 2.0724458619110511, 2.0723704768159057, 2.0722953069713772, 2.0722203543282816, 2.07214562046406, 2.0720711070618338, 2.0719968162749813, 2.0719227508485654, 2.0718489139407343, 2.0717753086877875, 2.0717019376708601, 2.071628802514776, 2.071555903836364, 2.071483241628576, 2.0714108159615692, 2.0713386276997374, 2.0712666788939873, 2.0711949726580414, 2.0711235125958782, 2.0710523020563563, 2.0709813435342315, 2.070910638416144, 2.0708401870873314, 2.0707699892765752, 2.0707000444758408, 2.070630352306043, 2.0705609127737583, 2.070491726419061, 2.0704227943838553, 2.0703541184217764, 2.0702857008530953, 2.0702175444533606, 2.0701496522745511, 2.0700820274248684, 2.0700146728665043, 2.0699475913020136, 2.0698807851949823, 2.0698142569238938, 2.0697480090142628, 2.0696820443603761, 2.0696163663458216, 2.0695509787972326, 2.0694858857515142, 2.0694210910677895, 2.0693565979577087, 2.0692924085300222, 2.0692285234406551, 2.0691649417089666, 2.0691016607197223, 2.0690386763886481, 2.0689759834435022, 2.0689135757629473, 2.0688514467206822, 2.0687895894899824, 2.0687279972803325, 2.0686666634933526, 2.0686055818046896, 2.0685447461939073, 2.0684841509499736, 2.0684237906739407, 2.0683636602889237, 2.0683037550537944, 2.0682440705734031, 2.0681846027974435, 2.0681253480061152, 2.0680663027854198, 2.0680074639990855, 2.067948828762872, 2.067890394410417, 2.0678321581569117, 2.0677741129218714, 2.0677162146178087, 2.0676582392889973, 2.0675995479108633, 2.0675394969895744, 2.0674788248940827, 2.0674190913725981, 2.0673604309873239, 2.067301790526455, 2.067242287380092, 2.0671816122504221, 2.0671198346581807, 2.0670571758298291, 2.0669938846386757, 2.0669301888129099, 2.0668662820841157, 2.066802324917167, 2.0667384491077927, 2.0666747627427311, 2.0666113545330727, 2.0665482973954425, 2.0664856513807814, 2.0664234660687302, 2.06636178251025, 2.0663006347755819, 2.0662400511581613, 2.0661800550904572, 2.06612066583501, 2.0660618990169541, 2.0660037670537541, 2.0659462795232937, 2.0658894434912152, 2.0658332637965682, 2.0657777432698334, 2.0657228828266732, 2.0656686813396048, 2.0656151351611927, 2.0655622372051998, 2.0655099757238191, 2.0654583334917462, 2.0654072889279798, 2.0653568208866813, 2.065306917014087, 2.0652575821857639, 2.0652088426579183, 2.0651607448523182, 2.0651133494988567, 2.0650667204525837, 2.0650209095602192, 2.0649759438327937, 2.0649318209692784, 2.0648885137565438, 2.0648459793280773, 2.0648041687123215, 2.06476303400874, 2.0647225325764933, 2.0646826287787508, 2.0646432941501485, 2.0646045067332821, 2.0645662500867594, 2.0645285122504284, 2.0644912848111363, 2.0644545621278927, 2.0644183407359824, 2.0643826189323238, 2.0643473965410055, 2.0643126748589755, 2.0642784567835566, 2.0642447471181065, 2.0642115530375094, 2.0641788846571734, 2.0641467555922604, 2.0641151833136511, 2.064084189043712, 2.0640537969366228, 2.0640240324131347, 2.0639949197648226, 2.0639664794081183, 2.0639387252995087, 2.0639116629590526, 2.063885288353994, 2.0638595877181856, 2.0638345382759553, 2.0638101097692561, 2.0637862665958533, 2.0637629702774736, 2.0637401819356662, 2.0637178645001679, 2.0636959844654639, 2.0636745131229208, 2.0636534272798803, 2.0636327095302884, 2.0636123481686437, 2.0635923368430236, 2.0635726740368963, 2.0635533624551523, 2.063534408374379, 2.0635158210002347, 2.0634976118619419, 2.063479794261684, 2.0634623827889356, 2.0634453929022092, 2.0634288405779375, 2.0634127420222774, 2.0633971134406823, 2.0633819708590631, 2.0633673299897293, 2.0633532061355218, 2.0633396141256113, 2.063326568276985, 2.063314082374188, 2.0633021696601004, 2.0632908428274308, 2.0632801139944212, 2.0632699946370723, 2.0632604954343363, 2.0632516259610254, 2.0632433941503474, 2.0632358054671696, 2.0632288618402135, 2.0632225606542569, 2.0632168945053624, 2.0632118527650172, 2.0632074257749293, 2.0632036112738152, 2.0632004209636374, 2.0631978844066539, 2.0631960482769589, 2.0631949703669212, 2.0631947092764849, 2.0631953127752016, 2.0631968090711581, 2.0631992039104032, 2.0632024834252287, 2.0632066203780286, 2.0632115810554228, 2.0632173309742363, 2.0632238387201078, 2.0632310780338843, 2.0632390286014042, 2.0632476760351022, 2.0632570114339082, 2.0632670307795342, 2.063277734321431, 2.063289126030821, 2.0633012131576693, 2.063314005898067, 2.0633275171634478, 2.06334176242909, 2.0633567596304783, 2.0633725290605898, 2.0633890932111134, 2.0634064764921933, 2.0634247047700511, 2.0634438046857717, 2.0634638027637329, 2.0634847243782555, 2.0635065926965219, 2.0635294277439926, 2.0635532457198766, 2.0635780586428631, 2.0636038743424532, 2.0636306967568601, 2.0636585264601774, 2.0636873613294537, 2.0637171972668149, 2.0637480289057208, 2.0637798502545133, 2.0638126552497886, 2.0638464382152821, 2.0638811942346535, 2.0639169194584599, 2.0639536113671961, 2.0639912690130431, 2.064029893256929, 2.0640694870118819, 2.0641100554953833, 2.0641516064871555, 2.0641941505841852, 2.0642377014400228, 2.0642822759763173, 2.0643278945530059, 2.0643745810877712, 2.0644223631141632, 2.0644712717723563, 2.064521341726945, 2.064572611009595, 2.0646251207958679, 2.0646789151449982, 2.0647340407699852, 2.0647905469680419, 2.0648484859270844, 2.0649079137263984, 2.0649688924360432, 2.0650314937196574, 2.0650958041357383, 2.0651619317203176, 2.0652300122721736, 2.0653002121527249, 2.0653727231575818, 2.0654477457386111, 2.0655254610861906, 2.0656059994833162, 2.0656894173983376, 2.0657756938593672, 2.0658647478406649, 2.0659564690155796, 2.0660507505908825, 2.0661475156389395, 2.0662467335815617, 2.0663484276236397, 2.0664526757798551, 2.0665596082252584, 2.0666694029943025, 2.0667822812217271, 2.0668985024666835, 2.0670183602630012, 2.0671421778869599, 2.0672703043920726, 2.0674031111874203, 2.0675409897400878, 2.0676843512163385, 2.0678336288351002, 2.0679892832346507, 2.0681518102683891, 2.068321749669126, 2.068499692493118, 2.0686862856883876, 2.0688822336515806, 2.069088298858266, 2.0693053057345669, 2.0695341528474631, 2.0697758372800008, 2.0700314909772866, 2.0703024210047243, 2.0705901319705329, 2.0708962880297204, 2.0712225610778816, 2.0715703742981648, 2.0719407358724413, 2.0723344758902065, 2.0727529082820308, 2.0731986119835262, 2.0736763061462367, 2.0741937037453351, 2.0747604977286525, 2.0753820134959251, 2.0760485766306491, 2.0767345554746415, 2.0774105711056419, 2.0780361907805998, 2.0785618992779131, 2.0789086601400286, 2.0789276789944418, 2.0785823142897906, 2.078129050498132, 2.0776806429030668, 2.0772634723581205, 2.0768689065163515, 2.0764931561861286, 2.0761350953919679, 2.0757935215954908, 2.0754671182855686, 2.0751546279734945, 2.0748549033890304, 2.0745669119811172, 2.0742897303715635, 2.0740225362943354, 2.0737645993778826, 2.0735152715672025, 2.073273977813864, 2.0730402073996923, 2.0728135060448336, 2.0725934688270451, 2.0723797338808638, 2.0721719768182991, 2.0719699058099921, 2.0717732572651264, 2.0715817920558499, 2.0713952922345005, 2.071213558196618, 2.0710364062429201, 2.0708636664959923, 2.0706951811279644, 2.0705308028583347, 2.0703703936836999, 2.0702138238046195, 2.0700609707177118, 2.0699117184468023, 2.0697659568880145, 2.069623581249485, 2.0694844915688031, 2.0693485922944186, 2.0692157919213048, 2.06908600267603, 2.0689591402563585, 2.068835123655973, 2.0687138751629011, 2.0685953207529706, 2.0684793913466688, 2.0683660257997425, 2.0682551769624782, 2.0681468223010633, 2.0680409795639276, 2.0679377244752022, 2.067837200846216, 2.067739607229814, 2.0676451485780705, 2.0675539642204472, 2.0674660691601074, 2.0673813421627618, 2.0672995604516657, 2.0672204535336189, 2.0671437493760529, 2.0670692020599373, 2.0669966027645517, 2.0669257803012884, 2.0668565966882797, 2.0667889411853824, 2.0667227244956736, 2.0666578738052821, 2.0665943288093285, 2.0665320386467494, 2.0664709595909532, 2.0664110533341185, 2.0663522857247574, 2.0662946258406762, 2.0662380453079501, 2.0661825177974662, 2.0661280186471642, 2.0660745245743359, 2.0660220134507572, 2.0659704641225312, 2.0659198562619241, 2.0658701702430542, 2.0658213870360949, 2.0657734881162413, 2.0657264553857511, 2.0656802711076461, 2.0656349178501046, 2.0655903784404739, 2.0655466359287962, 2.0655036735599346, 2.0654614747528526, 2.065420023087007, 2.0653793022945823, 2.0653392962577488, 2.0652999890099597, 2.0652613647407372, 2.0652234078032614, 2.0651861027238825, 2.0651494342134122, 2.0651133871793879, 2.0650779467393616, 2.0650430982345553, 2.0650088272437648, 2.0649751195968293, 2.0649419613883917, 2.0649093389901045, 2.0648772390621692, 2.0648456485629825, 2.0648145547573113, 2.0647839452219094, 2.0647538078487897, 2.0647241308459026, 2.0646949027351678, 2.0646661123479935, 2.064637748818853, 2.0646098015767103, 2.0645822603351376, 2.0645551150816517, 2.0645283560664227, 2.0645019737912063, 2.0644759589982531, 2.0644503026603527, 2.0644249959710841, 2.0644000303367642, 2.0643753973687557, 2.0643510888768875, 2.0643270968639622, 2.0643034135208893, 2.0642800312225478, 2.0642569425239086, 2.064234140157184, 2.0642116170286977, 2.0641893662162922, 2.0641673809666861, 2.064145654693081, 2.064124180972684, 2.0641029535442228, 2.0640819663052685, 2.0640612133098393, 2.0640406887654827, 2.0640203870306579, 2.0640003026119396, 2.0639804301608775, 2.0639607644713394, 2.0639413004762699, 2.0639220332447663, 2.0639029579789785, 2.0638840700111167, 2.063865364800348, 2.0638468379295998, 2.0638284851027602, 2.063810302141476, 2.0637922849823296, 2.0637744296738081, 2.0637567323734647, 2.0637391893450054, 2.0637217969557007, 2.0637045516734358, 2.0636874500641227, 2.0636704887891191, 2.0636536646026435, 2.0636369743494054, 2.0636204149618651, 2.0636039834582971, 2.0635876769400618, 2.0635714925896531, 2.0635554276683785, 2.0635394795141315, 2.0635236455395578, 2.0635079232298534, 2.0634923101407097, 2.0634768038966458, 2.0634614021888349, 2.0634461027735993, 2.0634309034703899, 2.063415802160165, 2.0634007967836601, 2.0633858853398639, 2.0633710658842541, 2.0633563365274092, 2.0633416954333872, 2.0633271408183127, 2.0633126709489185, 2.06329828414118, 2.0632839787589816, 2.0632697532126452, 2.0632556059579281, 2.063241535494547, 2.0632275403650278, 2.0632136191536676, 2.0631997704851193, 2.0631859930237861, 2.0631722854723051, 2.0631586465709493, 2.0631450750965512, 2.0631315698617732, 2.0631181297145313, 2.0631047535373077, 2.0630914402470868, 2.0630781887950036, 2.0630649981669564, 2.063051867383872, 2.0630387955035605, 2.063025781622037, 2.0630128248764934, 2.0629999244491191, 2.0629870795720264, 2.0629742895336221, 2.062961553686506, 2.0629488714573831, 2.0629362423582061, 2.0629236659997883, 2.0629111421060697, 2.0628986705296599, 2.0628862512668289, 2.0628738844717494, 2.0628615704666089, 2.0628493097471154, 2.0628371029802772, 2.0628249509929959, 2.0628128547495805, 2.0628008153183295, 2.0627888338278382, 2.0627769114151255, 2.0627650491703253, 2.062753248080901, 2.0627415089809578, 2.062729832509667, 2.0627182190807036, 2.0627066688649784, 2.0626951817861765, 2.0626837575284358, 2.0626723955545798, 2.0626610951335165, 2.0626498553771673, 2.0626386752883952, 2.0626275538222316]
'''