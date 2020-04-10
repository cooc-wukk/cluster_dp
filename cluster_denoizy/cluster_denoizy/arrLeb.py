import numpy as np
#类别二值化
def arrLeb(x, y, label):
    r_mean = []
    xy_result = np.transpose(np.vstack((x, y, label)))
    labels = np.unique(label)
    for label in labels:
        equal2label = xy_result[xy_result[:, 2] == label]
        mean = np.mean(equal2label, axis=0)
        r_mean.append(mean[0] * mean[1])
    index = r_mean.index(max(r_mean))
    xy_result = np.where(xy_result[:, 2] == labels[index], 0, 1)
    return xy_result