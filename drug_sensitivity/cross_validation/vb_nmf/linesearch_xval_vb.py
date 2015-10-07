"""
Run the cross validation with line search for model selection using VB-NMF on
the Sanger dataset.
"""

import sys
sys.path.append("/home/tab43/Documents/Projects/libraries/")#("/home/thomas/Documenten/PhD/")#

import numpy, random
from BNMTF.code.bnmf_vb_optimised import bnmf_vb_optimised
from BNMTF.cross_validation.line_search_cross_validation import LineSearchCrossValidation
from BNMTF.drug_sensitivity.load_data import load_Sanger


# Settings
standardised = False
iterations = 200
init_UV = 'random'

K_range = [6,7,8,9,10]#[1,5,10,15,20,25,30]
no_folds = 5
restarts = 1

quality_metric = 'AIC'
output_file = "./results.txt"

alpha, beta = 1., 1.
lambdaU = 1./10.
lambdaV = 1./10.
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

# Load in the Sanger dataset
(_,X_min,M,_,_,_,_) = load_Sanger(standardised=standardised)

# Run the cross-validation framework
random.seed(42)
numpy.random.seed(9000)
nested_crossval = LineSearchCrossValidation(
    classifier=bnmf_vb_optimised,
    R=X_min,
    M=M,
    values_K=K_range,
    folds=no_folds,
    priors=priors,
    init_UV=init_UV,
    iterations=iterations,
    restarts=restarts,
    quality_metric=quality_metric,
    file_performance=output_file
)
nested_crossval.run()

"""
All model fits for fold 1, metric AIC: [255811.96901730512, 253583.03512810238, 251017.06193697051, 249836.74028335506, 249206.43061974549].
Best K for fold 1: 10.
Performance: {'R^2': 0.8043017372724052, 'MSE': 2.2741348860136021, 'Rp': 0.89744685708793959}.

All model fits for fold 2, metric AIC: [255769.45162500613, 253467.91870441529, 250315.97341406014, 250584.56832730354, 248936.02082391683].
Best K for fold 2: 10.
Performance: {'R^2': 0.8048243105274231, 'MSE': 2.2715328533140489, 'Rp': 0.89782890912597857}.

All model fits for fold 3, metric AIC: [254648.23575785581, 253637.15771884247, 252262.96785723488, 250281.6596186492, 248794.28418679864].
Best K for fold 3: 10.
Performance: {'R^2': 0.8026105759027818, 'MSE': 2.3514064860012156, 'Rp': 0.89669532298664012}.

All model fits for fold 4, metric AIC: [255828.12060055314, 252798.29012129191, 251354.43120788396, 249944.59595474516, 249382.94637582474].
Best K for fold 4: 10.
Performance: {'R^2': 0.7957643808490702, 'MSE': 2.3766401494664517, 'Rp': 0.89277955209189619}.

All model fits for fold 5, metric AIC: [255907.35899378607, 253378.37414917364, 251587.40285130066, 250341.34565106896, 249276.7813075498].
Best K for fold 5: 10.
Performance: {'R^2': 0.8080940639049262, 'MSE': 2.2387725598694779, 'Rp': 0.8995121106626599}.
"""