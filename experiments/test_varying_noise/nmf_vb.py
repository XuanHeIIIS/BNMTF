"""
Test the performance of Variational Bayes for recovering a toy dataset, where 
we vary the level of noise, and use 10% test data.
We repeat this 10 times per noise level and average that.

We use the correct number of latent factors and flatter priors than used to generate the data.

I, J, K = 100, 80, 10

The noise levels indicate the percentage of noise, compared to the amount of 
variance in the dataset - i.e. the inverse of the Signal to Noise ratio:
    SNR = std_signal^2 / std_noise^2
    noise = 1 / SNR
We test it for 1%, 10%, 20%, 50%, and 100% noise.
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmf_vb_optimised import bnmf_vb_optimised
from BNMTF.experiments.generate_toy.bnmf.generate_bnmf import add_noise, try_generate_M
from ml_helpers.code.mask import calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

fraction_unknown = 0.1
noise_ratios = [ 0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5 ] # 1/SNR

input_folder = project_location+"BNMTF/experiments/generate_toy/bnmf/"

repeats = 10
iterations = 1000
I,J,K = 100, 80, 10

alpha, beta = 1., 1.
lambdaU = numpy.ones((I,K))/10.
lambdaV = numpy.ones((J,K))/10.
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

init_UV = 'random'

metrics = ['MSE', 'R^2', 'Rp']


# Load in data
R_true = numpy.loadtxt(input_folder+"R_true.txt")


# For each noise ratio, generate mask matrices for each attempt
M_attempts = 100
all_Ms = [ 
    [try_generate_M(I,J,fraction_unknown,M_attempts) for r in range(0,repeats)]
    for noise in noise_ratios
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
        
for Ms in all_Ms:
    for M in Ms:
        check_empty_rows_columns(M,fraction_unknown)


# For each noise ratio, add that level of noise to the true R
all_R = []
variance_signal = R_true.var()
for noise in noise_ratios:
    tau = 1. / (variance_signal * noise)
    print "Noise: %s%%. Variance in dataset is %s. Adding noise with variance %s." % (100.*noise,variance_signal,1./tau)
    
    R = add_noise(R_true,tau)
    all_R.append(R)
    
    
# We now run the VB algorithm on each of the M's for each noise ratio    
all_performances = {metric:[] for metric in metrics} 
average_performances = {metric:[] for metric in metrics} # averaged over repeats
for (noise,R,Ms,Ms_test) in zip(noise_ratios,all_R,all_Ms,all_Ms_test):
    print "Trying noise ratio %s." % noise
    
    # Run the algorithm <repeats> times and store all the performances
    for metric in metrics:
        all_performances[metric].append([])
    for (repeat,M,M_test) in zip(range(0,repeats),Ms,Ms_test):
        print "Repeat %s of noise ratio %s." % (repeat+1, noise)
    
        BNMF = bnmf_vb_optimised(R,M,K,priors)
        BNMF.initialise(init_UV)
        BNMF.run(iterations)
    
        # Measure the performances
        performances = BNMF.predict(M_test)
        for metric in metrics:
            # Add this metric's performance to the list of <repeat> performances for this noise ratio
            all_performances[metric][-1].append(performances[metric])
            
    # Compute the average across attempts
    for metric in metrics:
        average_performances[metric].append(sum(all_performances[metric][-1])/repeats)
    

    
print "repeats=%s \nnoise_ratios = %s \nall_performances = %s \naverage_performances = %s" % \
    (repeats,noise_ratios,all_performances,average_performances)


'''
repeats=10 
noise_ratios = [0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5] 
all_performances = {'R^2': [[0.9999999395630335, 0.9999999928906743, 0.9999999590004002, 0.9999999508479446, 0.999999757014438, 0.999999907100087, 0.999999880185556, 0.9999996244272937, 0.9999999083062547, 0.9999998513969608], [0.9872169490478419, 0.9863889683626499, 0.984817832426098, 0.9856278442440845, 0.9856146819323769, 0.9885028768571681, 0.9863304928425066, 0.9874271629662636, 0.9865671464804635, 0.9862961906091414], [0.9697375793091526, 0.9706149806411103, 0.9765149060695575, 0.9742094901393421, 0.9724695705717665, 0.974154684735378, 0.9756863281921537, 0.9735716905367409, 0.9752339993100132, 0.9765299504821537], [0.9436462328820918, 0.9418321588252829, 0.928480558835162, 0.9402193834247614, 0.9455690563574064, 0.9467958046490395, 0.9481264583664385, 0.9418281243263402, 0.9398641994123804, 0.9394248335121694], [0.8971280760098098, 0.8738589556835731, 0.8928053890517526, 0.8901772514332932, 0.8779718162408898, 0.8767806888153943, 0.8939614687921615, 0.8679336867553407, 0.8894750692961866, 0.8895953762973924], [0.7862264389098523, 0.808333790105953, 0.8018722245953505, 0.7924915702877224, 0.8096894655192034, 0.7939443544248859, 0.7785449765135044, 0.7999495003396758, 0.7833464611402563, 0.7900159186332261], [0.5441174435798213, 0.5744997926480562, 0.6210823683894424, 0.6172189083306171, 0.5845544354406276, 0.6288273464193093, 0.598701255109894, 0.558433232576194, 0.5297921983250002, 0.5737022583011011]], 'MSE': [[1.9693638736380783e-06, 2.7174616009545132e-07, 1.4594105214996862e-06, 1.8671672448818662e-06, 9.943582358726527e-06, 3.6091081245595755e-06, 4.3433443420178594e-06, 1.4910672550793262e-05, 3.2274080927908365e-06, 6.4098288515402509e-06], [0.50341084952466064, 0.52642151754624433, 0.53263405324428748, 0.53032447880142031, 0.50194344492662568, 0.50746170247941746, 0.47565361624712899, 0.49580205114912018, 0.51082204852072222, 0.51015258789365758], [1.0286843071098091, 0.95962976568666492, 0.96886468858352515, 0.88641024274327518, 0.98756952604002923, 1.0195242602577523, 0.99645319621727235, 1.0397154858507411, 0.98895284948953144, 1.0240748127560262], [2.2431168745332344, 2.3031955079077924, 2.5490739076922129, 2.457468600117394, 2.3672191581961197, 2.3575156000867095, 2.2983479139483936, 2.4521279932537352, 2.5704584997811417, 2.6150944964815004], [4.7760531055198534, 5.0627976697211219, 4.7301559942625859, 4.7235578620679846, 5.0550308496407395, 5.41569724064846, 4.6725189202048707, 5.0417994742742067, 4.7964843971647584, 4.994895500141145], [9.4474967747969725, 8.9162357741669442, 9.3103572038663618, 10.003080948139354, 9.1066300110990444, 9.0434488602115479, 9.5352446053290283, 8.814148782789875, 9.5278482648628984, 9.4687145493834688], [22.887479259858381, 23.610321780133322, 24.00098625811648, 22.343700646745077, 20.634715226159372, 22.346291687082822, 24.950096858714669, 26.243294837406971, 26.171428153896887, 23.058509248124547]], 'Rp': [[0.9999999698371228, 0.999999996465607, 0.99999997983992472, 0.99999997568461951, 0.99999987877197793, 0.99999995388555019, 0.99999994051777052, 0.99999981307098074, 0.99999995455221102, 0.99999992581729635], [0.99362269314220852, 0.99320254565319221, 0.99239983287065958, 0.99284359358618146, 0.9928041011983888, 0.99427469205420016, 0.99315586856888594, 0.99378887530875248, 0.99326464956735838, 0.99312598414184683], [0.98479343626741234, 0.98524235910335189, 0.98820770804009739, 0.9870449483622854, 0.98623165841727833, 0.98700298327266811, 0.98777207947864942, 0.9867107696279287, 0.98755844912779522, 0.98825330697318692], [0.97142481308293416, 0.97072403328409052, 0.96366248240092245, 0.96965672529959046, 0.97242541306311392, 0.97304069807796933, 0.97374528790183901, 0.97057769534391958, 0.96960095592612716, 0.96928861204769523], [0.94741662869102961, 0.93480890323994525, 0.94495619258091768, 0.94386272824902551, 0.93727205951169545, 0.93637832283640909, 0.94633520308779828, 0.93169754301856544, 0.94315895431429753, 0.94324145431382267], [0.88687096585023806, 0.899746758539265, 0.89555265438109299, 0.89042028704526333, 0.89986524383552746, 0.89161437720571468, 0.88241878191236578, 0.89503770353555989, 0.88553899473769238, 0.88898675017138507], [0.73920977744055438, 0.7579960628412149, 0.78822373823017455, 0.78633874863460351, 0.76496879344497626, 0.79331481149741034, 0.77453291439063565, 0.74834035938584753, 0.73010821074595289, 0.75894190732501632]]} 
average_performances = {'R^2': [0.99999987707326432, 0.98647901457685949, 0.97387231799873697, 0.94157868105910736, 0.88496877783757932, 0.79444147004696308, 0.5830929239120064], 'MSE': [4.8011632120543395e-06, 0.50946263503332845, 0.98998791347346271, 2.4213618551998239, 4.9268991013645733, 9.3173205774645478, 23.624682395623854], 'Rp': [0.99999993884430594, 0.99324828360916739, 0.98688176986706522, 0.97041467164282014, 0.94091279898435065, 0.89160525172141047, 0.76419753239363852]}
'''


# Plot the MSE, R^2 and Rp
for metric in metrics:
    plt.figure()
    x = noise_ratios
    y = average_performances[metric]
    plt.plot(x,y)
    plt.xlabel("Noise ratios missing")
    plt.ylabel(metric)