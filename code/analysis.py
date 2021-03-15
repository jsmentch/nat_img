def simple_ridgeCV(X,Y):
    from sklearn.linear_model import RidgeCV
    from sklearn.model_selection import KFold
    from sklearn.metrics import r2_score
    import numpy as np
    estimator = RidgeCV(alphas=[0.1, 1.0, 10.0, 100])
    cv = KFold(n_splits=5)
    scores = []
    weights=[]
    for train, test in cv.split(X=X):
        train = train[2:-2] #remove the first and last 3 seconds of each test and train partition
        test = test[2:-2]
        # print(f'training... {train}')
        # we train the Ridge estimator on the training set
        # and predict the fMRI activity for the test set
        predictions = estimator.fit(X.reshape(-1, X.shape[1])[train], Y[train]).predict(
            X.reshape(-1, X.shape[1])[test])
        # we compute how much variance our encoding model explains in each voxel
        scores.append(r2_score(Y[test], predictions,
                               multioutput='raw_values'))
        weights.append(estimator.coef_)
    scores_mean = np.mean(scores, axis=0)
    weights_mean = np.mean(weights, axis=0)
    return scores_mean,weights_mean