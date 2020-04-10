from sklearn import metrics
def calAcc(real, newleb):
    precision_score = metrics.precision_score(real, newleb)
    f1_score = metrics.f1_score(real, newleb)
    recall_score = metrics.recall_score(real, newleb)
    accuracy_score = metrics.accuracy_score(real, newleb)
    return precision_score, recall_score, f1_score, accuracy_score
