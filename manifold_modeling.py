# Starter code for implmenting manifold modeling.
# Marc Feldman (mfeldm21)
# Jonathan Liu (jliu118)


import sklearn.manifold
import statsmodels.api as sm
# http://statsmodels.sourceforge.net/devel/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html

# C is a set of predicted centers (x_i, y_i, z_i)
def manifold_filter(C):
    lowess = sm.nonparametric.lowess
    H = manifold.Isomap().fit(C)    # fix this lol      (might not be .fit(C) -- should look up)
                                    # Some parameters for this can also be changed.
    d = []                          # Stores final return values
    for i in range(len(C)):         # for i = 1, ..., n (len(C) might be wrong)
        H_remove_point = H.pop(i)   # This needs to be looked at.
        C_remove_point = C.pop(i)   # Hardcore, all of this stuff is wrong.
        f = lowess(H, C)            # Not sure if makes sense.
        d_add = np.linalg.norm(f[i] - H_remove_point)   # definitely doesn't make sense
        H.insert(i, H_remove_point)
        C.insert(i, C_remove_point)
        d.append(d_add)

    return d