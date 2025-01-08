import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def format_as_fraction(x, pos):
    fractions = {0: "0", 0.005: "1/200", 0.01: "1/100", 0.015: "3/200", 0.02: "1/50"}
    return fractions.get(x, f'{x:.3f}')

# FS scenario
def plot_fs_exp(ax):
    beta = np.linspace(0, 1, 400)
    d_no_exp = np.zeros_like(beta)
    d_r_exp = np.zeros_like(beta)
    d_d_exp = np.zeros_like(beta)
    d_c_exp = np.zeros_like(beta)

    d_no_exp[beta > 0.5] = 10
    d_r_exp[beta > 0.5] = 5
    d_d_exp[beta > 0.5] = 5
    d_c_exp[beta > 0.5] = 10

    offset = 0.07
    ax.plot(beta, d_no_exp + offset, color='#507B58', linewidth=3.5, label=r'$T0$')
    ax.plot(beta, d_d_exp - offset, color='#AB3131', linewidth=3.5, label=r'$T1$')
    ax.plot(beta, d_r_exp + offset, color='#6495ED', linewidth=3.5, label=r'$T2$')
    ax.plot(beta, d_c_exp - offset, color='#D68452', linewidth=3.5, label=r'$T1&2$')

    ax.vlines(0.5, 0, 10, colors=['#507B58', '#AB3131', '#6495ED', '#D68452'], linestyle='--')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 13)
    ax.set_xlabel(r'$\beta$', fontsize=20)
    ax.set_ylabel(r'$FS\ donations$', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=18)

# BO scenario
def plot_bo_exp(ax):
    a_b = np.linspace(0, 1/50, 400)
    d_no_exp = 10 - 40**2 * a_b
    d_r_exp = 210 / 17 - 150**2 / 17 * a_b
    d_d_exp = 130 / 17 - 150**2 / 17 * a_b
    d_c_exp = 10 - 720 * a_b

    intersection_no_exp = np.where(d_no_exp <= 0)[0][0]
    intersection_r_exp = np.where(d_r_exp <= 0)[0][0]
    intersection_d_exp = np.where(d_d_exp <= 0)[0][0]
    intersection_c_exp = np.where(d_c_exp <= 0)[0][0]

    d_no_exp[intersection_no_exp:] = 0
    d_r_exp[intersection_r_exp:] = 0
    d_d_exp[intersection_d_exp:] = 0
    d_c_exp[intersection_c_exp:] = 0

    ax.plot(a_b, d_no_exp, color='#507B58', linewidth=3.5)
    ax.plot(a_b, d_d_exp, color='#AB3131', linewidth=3.5)
    ax.plot(a_b, d_r_exp, color='#6495ED', linewidth=3.5)
    ax.plot(a_b, d_c_exp, color='#D68452', linewidth=3.5)

    ax.set_xlabel(r'$a/b$', fontsize=20)
    ax.set_ylabel(r'$BO\ donations$', fontsize=20)
    
    ax.tick_params(axis='x', which='major', labelsize=18, pad=10)
    ax.tick_params(axis='both', which='major', labelsize=18)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

plot_fs_exp(ax1)
plot_bo_exp(ax2)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

handles = handles1  
labels = labels1 

fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=20)

plt.subplots_adjust(top=0.975, bottom=0.275)

plt.savefig('Figure 1.pdf', format='pdf')

plt.show()