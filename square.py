import numpy as np
import math
import matplotlib.pyplot as plt 
num_ptc = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200, 102400]
num_ptc_ext = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200, 102400, 114564, 204800, 409600, 819200, 1638400, 3276800, 6553600, 13107200]
res = [34.667, 23.111, 10.947, 8.32, 6.82, 4.78, 4.25, 3.78, 3.35, 3.27, 3.25]
res_unsharp = [36.36, 36.36, 18.97, 19.83, 10.39, 8.39, 7.15, 5.32, 4.19, 3.73, 3.44]
ln_num_ptc = [float(np.log(i)) for i in num_ptc]
ln_num_ptc_ext = [float(np.log(i)) for i in num_ptc_ext]
res_inv = [1/(i*i) for i in res]
res_inv_unsharp = [1/(i*i) for i in res_unsharp]
lin_fit = np.polyfit(ln_num_ptc[5:], res_inv_unsharp[5:], 1)
nynquist = 1/(3.4*3.4)
labels_x = ['3.2','6.4','12.8','25.6','51.2','102.4']
labels_y = ['10.39', '8.39', '7.15', '5.32', '4.19', '3.73', '3.44']
#inv_res_sqr = [float(1/i** for i in list]
#for i in list_2:
#   print(f"{i:.2f}")
A0, m = lin_fit
straight = [A0*i+m for i in ln_num_ptc_ext]
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(res_inv, ln_num_ptc)
ax.set_ylim(0.005, 0.10)
ax.set_xlim(8, 12)
ax.scatter(ln_num_ptc[5:-1], res_inv_unsharp[5:-1])
for i in range(5,len(ln_num_ptc)):
	ax.scatter(ln_num_ptc[i], res_inv_unsharp[i], s=100, edgecolors=None, c='limegreen')
#ax.scatter(ln_num_ptc[-1], res_inv[-1], s=100, c='limegreen', edgecolors=None)
ax.plot(ln_num_ptc_ext[5:-1], straight[5:-1], c='gray', linewidth=2)
ax.hlines(nynquist, 8, ln_num_ptc_ext[-1], colors='darkmagenta', linestyles='--', linewidth=2.5, label='Nyquist')
ax.set_xticks(ln_num_ptc[5:])
ax.set_xticklabels(labels_x)
ax.set_yticks(res_inv_unsharp[5:])
ax.set_yticklabels(labels_y[:-1])
plt.xlabel('x1000 Particles', fontweight='bold')
plt.ylabel('Resolution (Å)', fontweight='bold')
plt.text(8.025, 0.089, 'Nyquist limit', fontweight='bold', c='darkmagenta')
plt.text(9.2, 0.105, '2.0/slope= 91.53 Å$^2$', fontweight='bold', c='dimgray', fontsize=12)
for i in range(5, 11):
	ax.hlines(res_inv_unsharp[i], 8, ln_num_ptc[i], linestyles='--', colors='silver', linewidth=1)
for i in range(5, 11):
	ax.vlines(ln_num_ptc[i], 0.005, res_inv_unsharp[i], linestyles='--', colors='silver', linewidth=1)
plt.savefig('cug_bplot.png', dpi=300)
plt.show()
print(A0,m)
