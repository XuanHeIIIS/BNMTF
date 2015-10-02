"""
Plot the performances of the many different NMF algorithms in a single graph.

We plot the average performance across all 10 attempts for different fractions:
[0.1, 0.2, ..., 0.9].

We use a dataset of I=100, J=80, K=10, with unit mean priors and zero mean unit
variance noise.

We have the following methods:
- VB NMF
- Gibbs NMF
- ICM NMF
- Non-probabilistic NMF
"""

import matplotlib.pyplot as plt
metrics = ['MSE','R^2','Rp']

MSE_max = 10

fractions_unknown = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] 

# VB NMF
vb_all_performances = {'R^2': [[0.9683884038267335, 0.9646169881339781, 0.9664777405474239, 0.9670287785874833, 0.9624240881702343, 0.9680355038256945, 0.9719307299997457, 0.9629826925022824, 0.9602855205649463, 0.9686705195002323], [0.9653987822562707, 0.9636273772329373, 0.9640673367298059, 0.966066739890249, 0.9633793377232198, 0.9679830987986853, 0.9620785803612693, 0.96082553183301, 0.9661693135001368, 0.9663244944657601], [0.9617930248094203, 0.9642355392384485, 0.9627655889098621, 0.9634443979607432, 0.9596607722421969, 0.9578754064932169, 0.9624082866584496, 0.9538263576952851, 0.9618078543645939, 0.963271891900556], [0.9599720724228168, 0.9589949486255698, 0.9624692958301866, 0.9600292193732625, 0.9586718181830132, 0.9644936230314554, 0.9601011113115265, 0.9582402555176157, 0.9610914150598637, 0.9568099713514397], [0.9510575870994907, 0.953133159466471, 0.9572018168117287, 0.9555886955604032, 0.9562238953027933, 0.9535614336904481, 0.9573252257504995, 0.9524315798133682, 0.9529882110179831, 0.9542089981937436], [0.9415774776278928, 0.9422029887451251, 0.9442776105339002, 0.9389233420029472, 0.9391074784542185, 0.9398795777026226, 0.9422419596592234, 0.9456691395310083, 0.9468243139570814, 0.9398076162947815], [0.9195686981189897, 0.9079605465864389, 0.9078082797884448, 0.9220014020277639, 0.9108287430753849, 0.9037028915591239, 0.912591476608551, 0.918270531533928, 0.9188651953510093, 0.9179806928033701], [0.6920410395599819, 0.6008746365040979, 0.5866015587287425, 0.6186019054564796, 0.5668339370408491, 0.6094993454431883, 0.6132762475293851, 0.49265601928467573, 0.6022068381761583, 0.5266814373578397], [0.498127855582871, 0.46276570487837276, 0.4688479204125017, 0.4643276992518711, 0.485925226956077, 0.47531296302186266, 0.47253208953783354, 0.4575697706092281, 0.32915747811593643, 0.3982904426552035]], 'MSE': [[1.3307806443295218, 1.3860030221750916, 1.3491865404494512, 1.2629440098447298, 1.3525845995372878, 1.3265179972285617, 1.3099149226729085, 1.3020277237977143, 1.4601402263219909, 1.2513376147112634], [1.435952160790894, 1.4303848268759256, 1.3641094842905677, 1.3897974028163187, 1.4508505446515516, 1.3585230505898929, 1.4387783797472564, 1.4369681270833714, 1.3365463498588703, 1.3972466786242712], [1.4560875651344829, 1.4162829303391684, 1.4619786232698355, 1.4634447984464445, 1.419116277117898, 1.5617928762366986, 1.4340335524769894, 1.5602103918913377, 1.4913875309554596, 1.434913867582116], [1.6041488253096432, 1.5757054761400267, 1.51638250689182, 1.6144003105634825, 1.5879065992141508, 1.5553875416864309, 1.5117231920229905, 1.6480661011771951, 1.6104213492947808, 1.5746276392092045], [1.8249532954410042, 1.8684675176149066, 1.6884323641027121, 1.7357984294610043, 1.7600831122286691, 1.7602824360794105, 1.7541479574284402, 1.8496812642592837, 1.8017840734869119, 1.8028886582045112], [2.2830756844552869, 2.3381965848102286, 2.216514115860623, 2.3093143677485344, 2.3415264238240638, 2.2899284412993794, 2.2271667169283544, 2.1963148167304456, 2.0830955631671704, 2.4138472512538964], [3.1232560756434995, 3.5500566611187123, 3.5434235337850692, 3.1256896633925706, 3.5094838277923319, 3.7894116899659496, 3.3721896132320386, 3.1328631528840871, 3.1814614927189346, 3.2612035339698324], [12.285753990084888, 15.358471185031494, 16.052806094752338, 14.905585025277116, 16.848948739652801, 15.506789499794692, 14.846760598929515, 20.165428714525419, 15.641343624014961, 18.888603197701336], [19.91181911887352, 21.089792265365787, 20.820169006409735, 21.111090007086695, 20.383431673137796, 20.692187943371938, 20.931366119129279, 21.338393635409702, 26.574615383488879, 23.191480741378562]], 'Rp': [[0.98417814296283501, 0.98223400580549158, 0.98310326759249378, 0.98340722606591879, 0.98109337471923375, 0.98404390169079525, 0.98592775532569599, 0.98131947992398216, 0.97998468118843007, 0.98422609008714801], [0.9826101986875232, 0.98164905167945748, 0.98193816637754328, 0.98290389426688474, 0.98154124970139101, 0.98390533314231476, 0.98101064425676598, 0.98026353532428501, 0.98297973175637066, 0.98305830615657197], [0.98078317148555072, 0.98198414505700715, 0.98122073773732377, 0.98155713977161774, 0.97963966020841486, 0.97874970585541088, 0.98104144030097185, 0.97667120348535452, 0.98076429936402731, 0.98151649299554744], [0.97994720265290991, 0.97937813547381558, 0.98107978700989862, 0.97983062508002172, 0.97919011307640369, 0.98208889140778566, 0.97990775152411236, 0.97892552090575269, 0.98035357770873099, 0.97823011129973625], [0.97527494390058556, 0.97661348931923153, 0.97847670949617727, 0.97768219832746694, 0.9778798337102893, 0.97658532879410387, 0.97851222466341137, 0.97598467728753147, 0.97623619637760939, 0.97694115727467978], [0.97039259977702308, 0.97073350305394834, 0.97179438232063309, 0.96901986600092904, 0.96919448091426885, 0.96948570832841707, 0.9707251134658279, 0.97246199162764579, 0.97310098700035219, 0.9694711588036119], [0.95912297665582935, 0.95332670849063539, 0.95288766098517352, 0.9602238588797064, 0.95446281935606847, 0.95093148902935831, 0.95553021872522659, 0.95856275340635955, 0.95885273967483775, 0.95837112445540062], [0.83309959117472532, 0.78392590768509252, 0.78228908789976048, 0.79230555909437228, 0.77539309469738738, 0.79410490646410281, 0.7990139950108649, 0.73383952871177027, 0.78463353986423079, 0.74223137952499108], [0.73535887538412503, 0.72700259454644678, 0.72810312108849651, 0.73051322809824903, 0.73276297324422102, 0.73165859759103224, 0.73380231876238378, 0.71376455057499144, 0.67766815789763035, 0.70196034943723151]]} 
vb_average_performances = {'R^2': [0.96608409656587535, 0.96459205927913449, 0.96110891202727733, 0.96008737307067504, 0.95437206027069299, 0.94205115045088017, 0.91395784574530037, 0.5909272965081398, 0.4512857151021758], 'MSE': [1.3331437301068518, 1.4039157005328922, 1.4699248413450432, 1.5798769541509725, 1.7846519108306853, 2.2698979966077983, 3.3589039244503018, 16.050049066976456, 21.604434589365191], 'Rp': [0.98295179253620246, 0.98218601113491089, 0.98039279962612258, 0.97989317161391676, 0.97701867591510871, 0.97063797912926564, 0.9562272349658596, 0.78208365901272991, 0.72125947666248069]}

# Gibbs NMF
gibbs_all_performances = {'R^2': [[0.9625030326397841, 0.9706451677249774, 0.963217707895298, 0.9654064278239094, 0.9643691045132832, 0.9672850759760732, 0.9678050734114245, 0.9700054162557077, 0.9705148382516579, 0.9639043626891819], [0.9652178740692119, 0.9635050992610616, 0.9657536717024912, 0.964522008466088, 0.9667065431225558, 0.9632625900673261, 0.9647633303828732, 0.9616172252261357, 0.9679151936920822, 0.964703774483381], [0.9629037141883738, 0.9608822891589637, 0.9656496888280449, 0.9633602441053563, 0.9580945073694958, 0.9669982233351793, 0.9653941908930447, 0.9632441314624717, 0.9632777036861077, 0.962266323182308], [0.9579299402036267, 0.9598158920752131, 0.9600909536153182, 0.9603853977612107, 0.9586308199546364, 0.960102646967832, 0.9598887021643804, 0.9576088800122263, 0.957762572220755, 0.9602726667571723], [0.9533424107044418, 0.954540844669128, 0.9527718533303425, 0.9522647284709008, 0.9515463243684358, 0.9534377017421702, 0.9546347761473944, 0.9527172602202294, 0.9533165949889422, 0.9553071857604678], [0.9431804130943913, 0.9436343468492804, 0.9446919305820516, 0.9434464097304541, 0.9422055576268311, 0.9421622537817048, 0.9409263728884416, 0.9398447610968322, 0.9429289265571029, 0.9374073592359273], [0.916524382023979, 0.9043779074524534, 0.9183809333829188, 0.900249099866099, 0.9042200028924992, 0.9083023628121983, 0.90897818251417, 0.9045388804986353, 0.9191668777556593, 0.8818574754459069], [0.6671567942933867, 0.6151737193408983, 0.6219931021607186, 0.39224588120077664, 0.6195966459142095, 0.7219978088246659, 0.6874080966837983, 0.6850285173577916, 0.6722454012900922, 0.636281137745908], [0.3675212826444849, 0.23977033459351604, 0.3131819547995017, 0.3195825910173784, 0.4211396095429468, 0.060084743933808804, 0.39875730727715586, 0.3154303760209578, 0.20980645235433315, 0.2535522654865773]], 'MSE': [[1.4080635301945019, 1.3834441410282272, 1.43846832498792, 1.3252201775103192, 1.289768927310458, 1.3907245622336175, 1.4628305532080657, 1.304976056368647, 1.3194413200996815, 1.3479391381887493], [1.3481063483908744, 1.442155660963143, 1.3523061894096968, 1.5024222091668862, 1.3857698541563856, 1.4682058869615482, 1.4249816213159914, 1.4567483413995783, 1.3323855931001123, 1.4217683300724258], [1.3827222803883148, 1.5751554279148783, 1.4061987209744606, 1.509455688815255, 1.507625578272743, 1.3824379048291175, 1.4234381842926758, 1.4963368471226333, 1.4396804186110883, 1.477881704853435], [1.5801209153324454, 1.5973218269774465, 1.6351795675932914, 1.6562019256517353, 1.6087627620105758, 1.5854058215600058, 1.5514288060190793, 1.7075562805566704, 1.6438600388615745, 1.5828742414373866], [1.7576436997384206, 1.8051022217662807, 1.8412551180472241, 1.8383194618348511, 1.8225252368084555, 1.7994736800937963, 1.7936386434290248, 1.8750743464116044, 1.8394212504554981, 1.7891029799471618], [2.2223513017617433, 2.2627072329745261, 2.2574489146867021, 2.2473658939138743, 2.321469558832471, 2.3134088317317745, 2.3801439793355135, 2.3410716909025076, 2.2015953734873492, 2.376271466983384], [3.3831137298395082, 3.7684340128891258, 3.1093920809466207, 3.8128585112652775, 3.8571548660298505, 3.612694885489443, 3.5642514383519068, 3.7040733323563302, 3.1787849159740511, 4.6733030187818558], [13.279569274385175, 15.203207789979999, 14.769243083707813, 23.774445419182403, 15.020806911986938, 11.009636346242466, 12.537176264539049, 12.528002453462435, 12.80758362532964, 14.115115429959346], [24.777056197673051, 30.043140977870845, 26.97455437847875, 26.977072284106811, 23.030147899288796, 36.435247069949099, 23.845359136623536, 27.105507744658343, 30.575962892150574, 29.506229606962588]], 'Rp': [[0.98112907943488292, 0.98525417987384933, 0.98147935507119177, 0.98275775056054115, 0.98203948996015467, 0.98352304605683794, 0.98379250854491329, 0.984964701042218, 0.98516016083518776, 0.9819138352749941], [0.98250662588756255, 0.98172420267800842, 0.98279751393473935, 0.98217124196125649, 0.98349853736107673, 0.98150198314314674, 0.9822598925141427, 0.98067597895876679, 0.98389870591089801, 0.98223219168438902], [0.98140167903506048, 0.98030883029687921, 0.982709405522598, 0.98159461273400095, 0.97895560271084825, 0.98345588910478432, 0.98287061242843787, 0.98149631542050431, 0.98150248690828956, 0.98096674913419646], [0.97876283666103892, 0.97974855069099387, 0.97994153136465889, 0.98005826843124322, 0.97917150451239099, 0.98000849015850999, 0.97984798411581941, 0.97867791253219261, 0.9786565803073719, 0.9800136677189899], [0.97654729362476933, 0.97722039322632015, 0.9763397785691339, 0.97593222594460827, 0.97558903597236113, 0.97661128767616934, 0.97720816479140737, 0.97662587249773991, 0.97651198444980425, 0.97745215330403623], [0.97177140810030704, 0.97165361246740878, 0.97222485268945658, 0.97179840668585771, 0.97077494046407375, 0.97084121265223111, 0.97016293403649922, 0.96996475459882969, 0.97109772640221903, 0.96856794941700564], [0.95767311191108817, 0.95107568848913859, 0.95961178954209159, 0.94961968749910031, 0.95235107854603918, 0.95400452406913894, 0.95405643445250732, 0.95116417152877031, 0.95933894276955078, 0.94063567824205208], [0.82495235207159523, 0.81003828716231907, 0.80807134161041672, 0.74265169909681406, 0.81048620429537788, 0.85837090993758092, 0.84449553510914677, 0.83915780946639851, 0.83280220624881118, 0.82379152767400254], [0.73184437699249605, 0.70574964090467174, 0.72927832469092224, 0.68654459784768007, 0.73612620404475915, 0.65664491003305059, 0.74881349033900768, 0.72468877844848423, 0.68276566639679837, 0.73287909775681781]]} 
gibbs_average_performances = {'R^2': [0.96656562071812968, 0.96479673104732055, 0.96320710162093448, 0.95924884717323722, 0.95338796804024528, 0.94204283314430182, 0.90665961046445198, 0.63191271048122455, 0.28988269176706605], 'MSE': [1.3670876731130188, 1.4134850034936641, 1.4600932756074601, 1.6148712186000211, 1.8161556638532321, 2.2923834244609842, 3.6664060791923974, 14.504478659877526, 27.927027818776242], 'Rp': [0.98320141066547717, 0.98232668740339868, 0.98152621832956011, 0.97948873264932101, 0.97660381900563498, 0.97088577975138879, 0.95295311070494759, 0.8194817872672463, 0.71353350874546884]}

# ICM NMF
icm_all_performances = {'R^2': [[0.9641562292087671, 0.9645010597069835, 0.9646901647940758, 0.9655401108016127, 0.9674530879915644, 0.9569122349718484, 0.9659676744219805, 0.961823331494361, 0.9588167717859395, 0.9677799213393541], [0.9653848809650548, 0.9620621930993009, 0.9640008426923107, 0.9650573608415195, 0.9626176887374777, 0.9678938358100784, 0.9656336306429064, 0.9658874195378, 0.9652151210503097, 0.9644450928693796], [0.9606542287614818, 0.9630774013973531, 0.9614947488092904, 0.9638428551389013, 0.9639431225149693, 0.9613333243745601, 0.962589151034413, 0.9622937077169137, 0.9648323744216998, 0.9627840868558615], [0.9573713059999577, 0.9603047794875761, 0.9604105518457282, 0.9599222108792298, 0.9583717438039353, 0.9609764263877065, 0.9584665615810277, 0.9594916076854826, 0.9618604428969201, 0.9584578815288594], [0.951945859286866, 0.9533250945881767, 0.9535805461601896, 0.951957301424992, 0.9530018526223901, 0.9507743945297216, 0.9505581120807776, 0.9515567288962331, 0.9512478253095026, 0.9519146032448463], [0.9404094188854749, 0.9336945507298016, 0.9350026335791896, 0.9400610379503956, 0.9383058550262751, 0.9405440166884551, 0.9421276539958618, 0.8453273983404234, 0.9409229351771975, 0.9412159509927134], [0.8373647489515432, 0.6593600787392411, 0.3857013908734044, 0.4285987221054517, -0.09804272884520082, 0.704092916823509, -0.3849876169183244, -0.6305356663474557, 0.5457178293698122, 0.24269210696018828], [-1.5236351313248049, -1.1687330885459528, -9.27866000769371, -2.5434674027132806, -3.108572831381043, -6.084027307204444, -0.8383840755797667, -2.2961562260049657, -3.763559201216636, -6.4064604561489675], [-48.087115511858926, -4.988536637651729, -13.588410241499483]], 'MSE': [[1.4157376128967303, 1.4172152810382146, 1.2982624221924366, 1.3660878392107088, 1.29413011643181, 1.3937119136567291, 1.24122050660739, 1.3714583484799947, 1.374719102657656, 1.225411413289351], [1.4143535690923141, 1.4024816442870915, 1.420143308333216, 1.3572228408037963, 1.4589553808393663, 1.4043078663157107, 1.3696816220228198, 1.4528537591434383, 1.3958140405975161, 1.4628392963149992], [1.4682991369101885, 1.4434980448246368, 1.5286511631346114, 1.4292470328290885, 1.4619574485924256, 1.4308418958806917, 1.4546923586872642, 1.4837337933507222, 1.4480701623668859, 1.4243120664506492], [1.6460829038655944, 1.5837355038774057, 1.5927933797650677, 1.5862983946889129, 1.6652205168830831, 1.5664651939031229, 1.61242928487742, 1.5801685343517209, 1.5349852001341278, 1.5911111352916367], [1.8004373299006959, 1.8506793815389737, 1.8387518473935809, 1.846188806961079, 1.8446840474272586, 1.9303648656261241, 1.8972671682840647, 1.9406695749130896, 1.8265258261696342, 1.8802983701989302], [2.4441134369396527, 2.5932139926844742, 2.5537570058304828, 2.3717359543163106, 2.3452921965481108, 2.4353039143070059, 2.2666633352411889, 5.9790532416995124, 2.3370397315869256, 2.3110464318179762], [6.2394953479314488, 13.784593279253274, 24.413549114187326, 22.074435636666941, 43.006418241923775, 11.78336042825334, 54.463352382775149, 63.852968595139409, 18.25734771363199, 28.910225414586353], [100.60746321557373, 87.117268686590904, 404.89917231840286, 139.77827007624774, 158.47479196109543, 283.0133371912288, 71.376220623944931, 131.6916560675991, 191.18767262917342, 297.25740371548216], [1962.6021086913352, 236.41109535417542, 583.85373463404892]], 'Rp': [[0.98211399540885458, 0.9821227854040846, 0.98224536989589228, 0.98266020829173428, 0.9836975174573801, 0.97833175537651063, 0.98284115656909854, 0.98073659923236323, 0.97928574344306818, 0.98376995424850522], [0.98255006826066837, 0.9809685309744689, 0.98191100095727535, 0.98240571325463921, 0.98117553577447336, 0.98383571689906058, 0.98268736743627849, 0.98295919555072864, 0.98253006918037389, 0.98211474189875991], [0.98012996319114154, 0.98142018962040667, 0.9807022680799482, 0.9818483602300967, 0.98189431679521122, 0.98047878687940315, 0.98123053528262116, 0.98104903560110901, 0.98230494368673038, 0.98122471738100714], [0.9786508632789751, 0.98002263850602911, 0.98003114162395899, 0.97978978703341157, 0.97903523697636363, 0.98041445367683056, 0.97926601139432823, 0.97962643078523393, 0.98084491811568064, 0.97911020775076651], [0.97595978557637297, 0.97647133340668057, 0.97662253254122089, 0.97575834842200704, 0.97635694617897473, 0.9754266207324167, 0.97514719743087108, 0.97562755309844695, 0.97549323954607658, 0.9759300551796849], [0.97017433106623752, 0.96712258530749773, 0.96757989375787468, 0.97009080698995864, 0.96896519339012244, 0.96994755012493528, 0.9710280832358994, 0.92312611736458228, 0.9703429260514721, 0.97039291603957767], [0.92262161908527718, 0.84441489551609283, 0.76553020553213313, 0.76721541794359593, 0.67650970147110256, 0.86231090261438936, 0.6142044177361794, 0.59485843617261747, 0.80863991123813217, 0.74642143976216602], [0.42402180869745382, 0.48701152422577909, 0.33006379185886042, 0.49131708735976293, 0.43358285957091047, 0.36538850849807497, 0.54465204022425162, 0.43791219015955979, 0.42742608847350999, 0.33937256120533654], [0.25033726482988228, 0.47484548419016576, 0.37271089170747973]]}
icm_average_performances = {'R^2': [0.9637640586516486, 0.96481980662461386, 0.96268450010254436, 0.95956335120964231, 0.95198623181436959, 0.92976114513657893, 0.2689961781712169, -3.7011655727813575, -22.22135413033671], 'MSE': [1.3397954556461018, 1.413865332775027, 1.4573303103027164, 1.5959290047638093, 1.8655867218413433, 2.763721924097164, 28.678574615434901, 186.54032564853392, 927.62231289318652], 'Rp': [0.98178050853274923, 0.98231379401867258, 0.98122831167476754, 0.97967916891415785, 0.97587936121127528, 0.96487704033281574, 0.76027269470716852, 0.42807484602735002, 0.3659645469091759]}

# Non-probabilistic NMF
np_all_performances = {'R^2': [[0.9661502982083258, 0.962935694405879, 0.9579918847016707, 0.9586855847444192, 0.9579413301853976, 0.9643752424278978, 0.9625018541706338, 0.9642155889543582, 0.9693308247182233, 0.9622156078161591], [0.7738031941739528, 0.9582488188784992, 0.9637610801855058, 0.9607422939171018, 0.9404025066359981, 0.9594583669040999, 0.9591830257467121, 0.9553099498878874, -2.4448183930816992e+17, 0.9610755403854095], [0.9550921840646763, 0.9599898031432155, 0.9556577196733663, 0.9581000885171519, 0.9492740309957454, 0.9598876053162747, 0.9507090899821207, 0.956382631652309, 0.9611693944104636, 0.9425040555152631], [0.9543206264599566, 0.9357396874372022, 0.9021616378326077, 0.9514680771189915, 0.9275762779294109, 0.953324220159332, 0.9550403684039722, 0.9558863218069189, 0.9374463953138343, 0.9472423819364637], [0.8975214047725241, 0.9381100537188582, 0.9309242402464417, 0.9397998009897294, 0.943055387739175, 0.9465670199112393, 0.9321294891175007, 0.94543022499159, 0.9436772193615721, 0.8810111283285733], [0.900633426748527, 0.9013446777363628, 0.9172841361893971, 0.9230259836336084, 0.8751296483680102, -1.348735323695198e+31, 0.8836529080552435, 0.8834468969624704, -2.105639709054465e+26, 0.9046920642038049], [0.010884183541726156, 0.5049777169744014, 0.5296323472122934, 0.5936943976062795, 0.5716720534000084, 0.6233092094213697, 0.5965611750679126, 0.5779136673568901, 0.42055629538918204, 0.6287568644436624], [-0.45642794157473143, -1.052633358086458, -0.4529742629337812, -1.1243674854489534, -3.908537592753116e+61, -4.98306776726117e+21, -0.6467249736651255, -1.2738651178092981, -0.30512221429863495, -0.05200502764261228], [-0.04309526390610796, -0.02014083310684356, -0.34542612514425763, -0.3477585712038145, -0.14517898827705533, -0.8193145272438367, -0.2279504356076938, -0.23181027839634227, -1.2175964528062164, -0.31144237736982583]], 'MSE': [[1.3695686217895828, 1.475720118788193, 1.5216162009390759, 1.4690436017122814, 1.6151908512877098, 1.4027485131097412, 1.514739676861188, 1.3897245750825027, 1.3891606148877207, 1.3389950648223417], [8.6852868129859857, 1.5375422078098413, 1.4530307437814056, 1.4805769532281412, 2.3237136578971449, 1.5873539482310122, 1.5019477036713205, 1.6487801883379343, 9.7666811832596111e+18, 1.4819662095171759], [1.8188632432736556, 1.6366831874773429, 1.6795250705324127, 1.6179417424938518, 2.0453406988109779, 1.5663308378797991, 1.9080645950773132, 1.7016937087671649, 1.5437459708857908, 2.3982064104972007], [1.7571084255952911, 2.6855252887984506, 3.8160089658610654, 1.8970323665474809, 2.8888169509394079, 1.8225906952658044, 1.7814349144649713, 1.7378457301070249, 2.3589722529861175, 2.01764908440577], [4.017845426767555, 2.3841519511545295, 2.7262206294237856, 2.3101858277707894, 2.1892511792243368, 2.0622537857657726, 2.7074802112092384, 2.1269716748773471, 2.1799390180663178, 4.5341836237437683], [3.7502306628708184, 4.0640664512526401, 3.2847420788901274, 3.0368310621083441, 4.9732944238799259, 5.3282235229279668e+32, 4.6312237653647648, 4.5046690115209191, 8.3773807319324908e+27, 3.7155048001008875], [40.095910868119844, 19.36582278758366, 18.488739845707268, 15.937851581220615, 16.468447877392624, 15.316301044706533, 15.920846166152756, 16.618627600928225, 23.600890264012477, 14.373470158311665], [57.222233431202966, 80.44232137085946, 57.124626413084862, 84.745185775547284, 1.5303091422216016e+63, 1.9717159904449872e+23, 64.571133901740438, 85.750332559312724, 52.665746201305325, 39.493631260428785], [40.849424198732912, 39.934197145504463, 52.487030821784849, 53.49887422652801, 45.896261560908144, 71.504820883916068, 48.141645727118984, 47.841832985258534, 86.266965432227664, 51.208290236424475]], 'Rp': [[0.98303370494402409, 0.98132979238664919, 0.97891205371012113, 0.97921246854617705, 0.97892066995417559, 0.98223769361949387, 0.9811947765558624, 0.98201103290914415, 0.98482390347244664, 0.98095040304505887], [0.89154932826012911, 0.9789409665837564, 0.98175639896461442, 0.98020342334469313, 0.96987511958161765, 0.97963102479020481, 0.97945186953392538, 0.9775525367400687, 0.021583198076839838, 0.98038584912331239], [0.97732765396093946, 0.97979995031795875, 0.97769985274599824, 0.97890656365927697, 0.97430872401340629, 0.97975550634114006, 0.97504544500232437, 0.97804511746463418, 0.98041505342158231, 0.97116110827122637], [0.97702066323586367, 0.96741279159188498, 0.95166574406088056, 0.97563123935745122, 0.96359365421918686, 0.97647879587444342, 0.97738567464388637, 0.9778381459264176, 0.96900570574306977, 0.97344895915611185], [0.9501543533595006, 0.96882839140687249, 0.96544954061435939, 0.96970982816912665, 0.97130099789985669, 0.97310954364170166, 0.96588216475382849, 0.97270453478590346, 0.97171141880713785, 0.94298972155482585], [0.95101556943385346, 0.95027401310186033, 0.95871189128867473, 0.96278393252484862, 0.93819070108323099, 0.0045923032382887818, 0.94209130511964156, 0.94283433250564219, 0.037932442615479227, 0.95353919145581856], [0.62747739503465205, 0.75919705790635872, 0.79461938581828295, 0.81912315886921971, 0.81503479520577748, 0.82778453608926539, 0.80896978574934975, 0.80745852658153683, 0.75668962639993753, 0.83078458067261762], [0.54217456399624087, 0.50578520529676785, 0.527315450601331, 0.46735722232504817, 0.00753951176349306, -0.0043707847973975342, 0.55950830721917455, 0.52562595089792885, 0.54872075607088666, 0.6249312428373156], [0.59672416261665451, 0.58784736293138717, 0.57630471698331109, 0.4877833058977542, 0.56269504499787926, 0.46837200206146462, 0.52103365407006086, 0.57663952599409773, 0.46857183958752213, 0.56737668246188722]]} 
np_average_performances = {'R^2': [0.96263439103329651, -24448183930816992.0, 0.95487666032705865, 0.94202059943986904, 0.92982259691772051, -1.3487563800922885e+30, 0.50579579104137262, -3.9085375927531155e+60, -0.37097138530619944], 'MSE': [1.4486507839280338, 9.7666811832596109e+17, 1.7916395465695509, 2.2762984674971385, 2.723848332800344, 5.3283072967352863e+31, 19.618690819413565, 1.5303091422216016e+62, 53.762934321840405], 'Rp': [0.98126264991431511, 0.87409297149991616, 0.97724649751984871, 0.97094813738091967, 0.96518404949931136, 0.76419656823673365, 0.78471388483269988, 0.4304587426210788, 0.54133482976020186]}



# Assemble the average performances and method names
methods = ['VB-NMF', 'G-NMF', 'ICM-NMF', 'NP-NMF']
avr_performances = [
    vb_average_performances,
    gibbs_average_performances,
    icm_average_performances,
    np_average_performances
]

for metric in metrics:
    plt.figure()
    #plt.title("Performances (%s) for different fractions of missing values" % metric)
    plt.xlabel("Fraction missing", fontsize=16)
    plt.ylabel(metric, fontsize=16)
    
    x = fractions_unknown
    for method, avr_performance in zip(methods,avr_performances):
        y = avr_performance[metric]
        #plt.plot(x,y,label=method)
        plt.plot(x,y,linestyle='-', marker='o', label=method)
    plt.legend(loc=0)  
    
    if metric == 'MSE':
        plt.ylim(0,MSE_max)
    else:
        plt.ylim(0,1)