import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

pca_df = pd.read_csv('./pca_input_2d.csv')
pca_T = np.vstack((pca_df['x'], pca_df['y'])).T

x = pca_df['x']
y = pca_df['y']

mean_x = np.mean(x)
mean_y = np.mean(y)

pca = mlab.PCA(pca_T)

sig_x = np.std(pca_T['0']) # ~ 2.01
sig_y = np.std(pca_T['1']) # ~ 0.96

plt.figure(1)
plt.plot(pca.Y[0:,0], pca.Y[0:, 1], 'o', alpha = 0.5, color = 'blue')

#plt.axis('equal')
plt.title('Transformed PCA samples')
plt.xlim(xmin = (sig_x * -3), xmax = (sig_x * 3))
plt.xticks(np.arange((sig_x * -2), (sig_x * 3), sig_x))

plt.axvline(x = sig_x * - 2, linestyle = 'dotted')
plt.axvline(x = sig_x * - 1, linestyle = 'dotted')
plt.axvline(x = sig_x * 1, linestyle = 'dotted')
plt.axvline(x = sig_x * 2, linestyle = 'dotted')


plt.ylim(ymin = (sig_y * -3), ymax = (sig_y * 3))
plt.yticks(np.arange((sig_y * -2), (sig_y * 3), sig_y))
plt.axhline(y = sig_y * - 2, linestyle = 'dotted')
plt.axhline(y = sig_y * - 1, linestyle = 'dotted')
plt.axhline(y = sig_y * 1, linestyle = 'dotted')
plt.axhline(y = sig_y * 2, linestyle = 'dotted')

plt.figure(2)
plt.scatter(mean_x, mean_y, s = 40, c = 'r')
plt.title("Placing eigenvectors at original mean")
plt.scatter(x, y, alpha= 0.4)

plt.xlabel('x_values')
plt.ylabel('y_values')
plt.axis('equal')

s = pca.s / 999
wt = pca.Wt
wt[0][0] = (wt[0][0] * sig_x) + mean_x
wt[1][0] = (wt[1][0] * sig_x) + mean_y
wt[0][1] = (wt[0][1] * sig_y) + mean_x
wt[1][1] = (wt[1][1] * sig_y) + mean_y

vec = np.array( [ [mean_x, wt[0][0], mean_y, wt[1][0]], [mean_x, wt[0][1], mean_y, wt[1][1]] ])
X, Y, U, V = zip(*vec)

plt.plot([X[0], Y[0]], [U[0], V[0]], 'r-o', lw=3)
plt.plot([X[1], Y[1]], [U[1], V[1]], 'r-o', lw=3)


# plt.plot([wt[0][0], wt[1][0]], [wt[0][1], wt[1][1]])

# print "a: ", pca.a
# print "num_cols: ", pca.numcols
# print "num_rows", pca.numrows
# print "pca.s :", pca.s / 999
# print "pca.wt: ", pca.Wt
# print "pca.mu ", pca.mu
# print "sigma ", pca.sigma
# print "fracs ", pca.fracs
#
# print "X", X, "Y", Y, "U", U, "V", V
#print "Y ", pca.Y
#print [vec[0][0], vec[0][1], vec[0][2], vec[0][3]]
plt.show()

