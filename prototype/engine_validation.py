import numpy as np


def cross_validation(fit, test_set):
    # accumulate residuals
    residuals = []
    for i in test_set:
        i_target = i[target]
        del i[target]
        residuals.append((fit.predict(i) - i_target)**2)

    return np.sum(rss)


def mean_variance_validation(fit, validation_target, test_set, means):
    # accumulate residuals
    residuals = {}
    for i in test_set:
        i_target = i[target]
        del i[target]
        if i_target not in residuals.keys():
            residuals[i_target] = []
        
        residuals[i_target].append(fit.predict(i) - means[i_target])

    # calculate variances across the sample space
    variances = []
    for r in residuals:
        variances.append(np.var(r))

    # calculate mean variances
    mean_variance = np.mean(variances)

    return np.absolute(mean_variance)