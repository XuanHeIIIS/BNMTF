"""
Run the grid search method for finding the best values for K and L for BNMTF.
We use the parameters for the true priors.

For BNMTF I find that the BIC is a better estimator - the log likelihood is 
high for higher values for K and L than the true ones, same for the AIC. With
the BIC we get a nice peak just below the true K and L (for true K=L=5, at K=L=4).
"""

project_location = "/Users/thomasbrouwer/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.data_toy.bnmtf.generate_bnmtf import generate_dataset, try_generate_M
from BNMTF.code.cross_validation.grid_search_bnmtf import GridSearch
from BNMTF.code.models.bnmtf_vb_optimised import bnmtf_vb_optimised

import numpy, matplotlib.pyplot as plt
import scipy.interpolate

##########

restarts = 5
iterations = 1000

I, J = 100,80
true_K, true_L = 5, 5
values_K, values_L = range(1,10+1), range(1,10+1)

#fraction_unknown = 0.1
attempts_M = 100

alpha, beta = 1., 1. #1., 1.
tau = alpha / beta
lambdaF = numpy.ones((I,true_K))
lambdaS = numpy.ones((true_K,true_L))
lambdaG = numpy.ones((J,true_L))

classifier = bnmtf_vb_optimised
initFG = 'kmeans'
initS = 'random'

# Generate data
(_,_,_,_,_,R) = generate_dataset(I,J,true_K,true_L,lambdaF,lambdaS,lambdaG,tau)
M = numpy.ones((I,J))
#M = try_generate_M(I,J,fraction_unknown,attempts_M)

# Run the line search. The priors lambdaF,S,G need to be a single value (recall K,L is unknown)
priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF[0,0]/10, 'lambdaS':lambdaS[0,0]/10, 'lambdaG':lambdaG[0,0]/10 }
grid_search = GridSearch(classifier,values_K,values_L,R,M,priors,initS,initFG,iterations,restarts)
grid_search.search()

# Plot the performances of all three metrics
metrics = ['loglikelihood', 'BIC', 'AIC','MSE']
for metric in metrics:
    # Make three lists of indices X,Y,Z (K,L,metric)
    values = numpy.array(grid_search.all_values(metric)).flatten()
    list_values_K = numpy.array([values_K for l in range(0,len(values_L))]).T.flatten()
    list_values_L = numpy.array([values_L for k in range(0,len(values_K))]).flatten()
    
    # Set up a regular grid of interpolation points
    Ki, Li = (numpy.linspace(min(list_values_K), max(list_values_K), 100), 
              numpy.linspace(min(list_values_L), max(list_values_L), 100))
    Ki, Li = numpy.meshgrid(Ki, Li)
    
    # Interpolate
    rbf = scipy.interpolate.Rbf(list_values_K, list_values_L, values, function='linear')
    values_i = rbf(Ki, Li)
    
    # Plot
    plt.figure()
    plt.imshow(values_i, cmap='jet_r',
               vmin=min(values), vmax=max(values), origin='lower',
               extent=[min(values_K), max(values_K), min(values_L), max(values_L)])
    plt.scatter(list_values_K, list_values_L, c=values, cmap='jet_r')
    plt.colorbar()
    plt.title("Metric: %s." % metric)   
    plt.xlabel("K")     
    plt.ylabel("L")  
    plt.show()
    
    # Print the best value
    best_K,best_L = grid_search.best_value(metric)
    print "Best K,L for metric %s: %s,%s." % (metric,best_K,best_L)
    
    
# Also print out all values in a dictionary
all_values = {}
for metric in metrics:
    all_values[metric] = list(grid_search.all_values(metric).flatten())
    
print "all_values = %s \nvalues_K=%s \nvalues_L=%s" % (all_values,values_K,values_L)

'''
all_values = {'MSE': [5.9209424286945858, 5.920942379903166, 5.9209411834704371, 5.9209411139826615, 5.9209411629678472, 5.920936431721425, 5.9209406456817835, 5.9209406124122825, 5.9209403682680888, 5.9209403811863206, 5.9209426390252382, 2.7592644156798807, 2.7639163479945608, 2.7596884289042078, 2.7660677000566096, 2.7624823779509935, 2.7647529742031867, 2.7616691175710422, 2.7618765660526856, 2.7609721666085179, 5.9209424494072893, 2.7593689912920394, 1.3116694173944394, 1.3074565235379938, 1.3072928585621093, 1.3075313128411006, 1.3077501754504874, 1.3067995157772245, 1.3068039898379658, 1.3064561172188953, 5.9209429830134992, 2.7591604511541563, 1.3072109388487911, 0.93708659837832065, 0.93541528098446836, 0.93493437966847115, 0.93527118785521401, 0.93593759380150565, 0.93605728808434152, 0.93497150893943193, 5.9209435135315509, 2.7591634523435378, 1.3077667363666412, 0.93590124989174617, 0.91721080365604657, 0.90488504520169954, 0.90043826204005284, 0.90856505358156336, 0.90481481124211371, 0.90459234185129722, 5.9209433244642335, 2.7591480207413301, 1.3062684132887339, 0.93698405454016909, 0.89438818430621703, 0.9040778953980364, 0.87722197465630469, 0.88418473859926017, 0.87964139335588332, 0.88167183330770282, 5.9209438864075441, 2.7595216657286636, 1.3068845525102835, 0.93541578473572229, 0.89657069244651477, 0.88753836656241281, 0.87354665296668277, 0.87542234823483001, 0.87550989230847054, 0.88548219500236824, 5.9209436406521814, 2.7592672054220548, 1.3075158185767668, 0.93635719627706537, 0.89939983473131713, 0.88024614946993385, 0.88054318753370542, 0.87190479800353071, 0.88370110467857765, 0.87091375683472227, 5.9209440556894322, 2.7594500089603082, 1.3080990739961993, 0.93581018361285584, 0.89899669599112342, 0.86617416958182003, 0.89038589379495248, 0.84477574949263556, 0.87581799880970401, 0.85391638425082628, 5.9209443699818181, 2.7605898925518884, 1.3064075548059457, 0.93571583299276728, 0.89788067540998939, 0.88289530279925965, 0.86895415621189953, 0.84667214442910854, 0.85541892382855245, 0.86791423629921238], 'loglikelihood': [-18467.010731820366, -18467.02237510297, -18467.03322526213, -18467.044930104152, -18467.056795331486, -18467.066334782852, -18467.080170095902, -18467.092141867684, -18467.103961368153, -18467.116099050912, -18467.02276059478, -15416.085473555231, -15422.824784872601, -15416.784364915979, -15427.217367747182, -15422.86769002529, -15426.1280186195, -15421.840126117851, -15424.876458166847, -15421.053292175638, -18467.034561502765, -15416.284354643383, -12446.697098404198, -12436.991006639822, -12436.787554816152, -12437.436126812365, -12438.373291989818, -12439.123406428142, -12436.003161761164, -12438.614866785054, -18467.046954332662, -15416.045384933273, -12433.472712315717, -11109.655935876204, -11106.964170083116, -11101.064604001116, -11111.256983460034, -11109.996220366414, -11111.694957090825, -11106.345142700242, -18467.060552078481, -15416.096509659883, -12438.475246715976, -11109.370636560001, -11031.080500231779, -10979.284321209358, -10964.754356181036, -10997.191231012162, -10981.402296493574, -10982.312043749364, -18467.071478842459, -15416.131521036532, -12433.851051735635, -11114.198219173761, -10940.394278066022, -10982.588038340331, -10868.616498863585, -10903.904800187493, -10881.016137228169, -10888.102444486645, -18467.084214758004, -15419.085774554602, -12440.646268889577, -11108.369000905494, -10949.767318394794, -10914.54229836207, -10857.778570583068, -10869.081849386186, -10864.215972402835, -10918.710644946417, -18467.096296354168, -15418.931668970929, -12437.926305010895, -11112.518973319282, -10969.083256100555, -10882.789684833713, -10885.133515162806, -10859.013105676046, -10899.151974132876, -10851.978374424154, -18467.109157801002, -15416.707349093771, -12441.898044746385, -11110.520307304603, -10955.41889020981, -10827.619332798024, -10934.147763664294, -10734.322106061769, -10872.605442741578, -10783.007076123376, -18467.123355762073, -15420.631416379338, -12435.651967599824, -11115.776934684583, -10957.439492400725, -10895.892020815148, -10839.528903854354, -10744.925289136805, -10791.310114087828, -10842.730919096775], 'AIC': [37296.021463640733, 37458.04475020594, 37620.06645052426, 37782.089860208303, 37944.113590662972, 38106.132669565704, 38268.160340191804, 38430.184283735369, 38592.207922736307, 38754.232198101825, 37498.045521189561, 31560.170947110462, 31737.649569745201, 31889.568729831957, 32074.434735494364, 32229.735380050581, 32400.256037239, 32555.680252235703, 32725.752916333695, 32882.106584351277, 37700.069123005531, 31764.568709286767, 25991.394196808396, 26137.982013279645, 26303.575109632304, 26470.87225362473, 26638.746583979635, 26806.246812856283, 26966.006323522328, 27137.229733570108, 37902.093908665323, 31968.090769866547, 26170.945424631434, 23691.311871752408, 23853.928340166232, 24010.129208002232, 24198.513966920069, 24363.992440732829, 24535.389914181651, 24692.690285400484, 38104.121104156962, 32172.193019319766, 26386.950493431952, 23898.741273120002, 23912.161000463559, 23978.568642418715, 24119.508712362072, 24354.382462024325, 24492.804592987148, 24664.624087498727, 38306.142957684919, 32376.263042073064, 26583.702103471271, 24116.396438347521, 23940.788556132044, 24197.176076680662, 24141.232997727169, 24383.809600374985, 24510.032274456338, 24696.204888973291, 38508.168429516008, 32586.171549109204, 26803.292537779154, 24312.738001810987, 24169.534636789587, 24273.08459672414, 24333.557141166137, 24530.163698772372, 24694.43194480567, 24977.421289892834, 38710.192592708336, 32789.863337941861, 27003.85261002179, 24529.037946638564, 24418.166512201111, 24421.579369667426, 24602.267030325613, 24726.026211352091, 24982.303948265751, 25063.956748848308, 38912.218315602004, 32989.414698187538, 27217.796089492771, 24733.040614609206, 24600.837780419621, 24523.238665596047, 24914.295527328588, 24692.644212123538, 25147.210885483157, 25146.014152246753, 39114.246711524145, 33201.262832758672, 27411.303935199649, 24951.553869369167, 24814.878984801449, 24871.784041630297, 24939.057807708708, 24929.85057827361, 25202.620228175656, 25485.461838193551], 'BIC': [38560.704088180551, 39288.690317219378, 40016.674960011318, 40744.661312168981, 41472.647985097268, 42200.630006473621, 42928.620619573339, 43656.607505590524, 44384.594087065081, 45112.581304904219, 39468.435024616236, 34103.510589831421, 34853.93935176044, 35578.80865114148, 36336.624796098171, 37064.875579948668, 37808.346376431364, 38536.720730722351, 39279.743534114627, 40009.047341426485, 40376.16550531907, 35020.602427715246, 29827.365251351821, 30553.890403938014, 31299.420836405614, 32046.655316512984, 32794.466982982834, 33541.904547974424, 34281.601394755417, 35032.762140918137, 41283.897169865719, 35936.818564002548, 30726.597751703041, 28833.88873175962, 29583.429733109049, 30326.555133880654, 31101.8644257341, 31854.267432482462, 32612.589438866889, 33356.814343021331, 42191.631244244214, 36853.614889163291, 31662.28409303174, 29767.986602476059, 30375.318059575882, 31035.637431287309, 31770.489230986932, 32599.274710405451, 33331.60857112454, 34097.339795392392, 43099.359976659034, 37770.378987624106, 32578.716975599244, 30712.310237052421, 31137.601281413874, 31994.887728539426, 32539.843576162861, 33383.319105387607, 34110.440706045891, 34897.51224713977, 44007.09232737698, 38692.981570367767, 33517.988682435309, 31635.320269864736, 32100.003028240928, 32811.439111573069, 33479.797779412664, 34284.290460416487, 35056.444829847373, 35947.320298332132, 44914.823369456164, 39609.367434907945, 34438.230027206126, 32578.288684041159, 33082.290569821955, 33700.576747506522, 34496.137728382964, 35234.770229627698, 36105.921286759614, 36802.447407560423, 45822.555971236696, 40521.61287086115, 35371.854779205292, 33508.959821360644, 33998.617504209979, 34542.878906425314, 35555.796285196775, 35956.005487030634, 37032.432677429169, 37653.096461231682, 46730.291246045694, 41446.155081139805, 36285.043897440351, 34454.141545469451, 34946.314374761307, 35632.067145449735, 36328.188625387724, 36947.829109812206, 37849.446473573829, 38761.135797451294]}
values_K=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
values_L=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
'''