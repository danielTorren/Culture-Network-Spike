"""Generate plot of truncated quasi-hyperbolic discounting
A module that generates data for quasi-hyperbolic discounting this is then trucated to produce a
moving average of agent memory. Used for illustrative purporses to explain how individuals have a
cultural momentum which slows identity change.

Author: Daniel Torren Peraire Daniel.Torren@uab.cat dtorrenp@hotmail.com

Created: 10/10/2022
"""

#imports
import matplotlib.pyplot as plt
import numpy as np

#modules
def calc_discount_list(present_discount_factor,discount_factor,time_list_beahviours):
    discount_list = present_discount_factor*(discount_factor)**(time_list_beahviours)
    discount_list[0] = 1
    return discount_list

def calc_data_discount(beta_vals, delta_vals, time_list):
    
    const_delta_discount_list = [calc_discount_list(x,delta_vals[0],time_list) for x in  beta_vals]
    const_beta_discount_list = [calc_discount_list(beta_vals[0],x,time_list) for x in  delta_vals]
    return const_delta_discount_list , const_beta_discount_list

def plot_discount_factors_beta_delta(f, const_delta_discount_list, const_beta_discount_list,beta_vals, delta_vals,time_list,culture_momentum, dpi_save):
    fig, ax = plt.subplots()

    for i in range(len(beta_vals)):
        ax.plot(time_list,const_delta_discount_list[i],linestyle = "--",label =  r"$\beta$ = %s , $\delta$ = %s" % (beta_vals[i],delta_vals[0]))#bodge so that we dont repeat one of the lines
    for i in range(len(delta_vals) - 1):
        ax.plot(time_list, const_beta_discount_list[i+1], linestyle = "-",label =  r"$\beta$ = %s , $\delta$ = %s" % (beta_vals[0],delta_vals[i+1]) )

    ax.set_xlabel(r"Time/$\Delta t$")
    ax.set_ylabel(r"$D_s$")
    ax.set_xticks(np.arange(0, -culture_momentum, step=-5))
    ax.legend()

    fig.savefig(f, dpi=dpi_save,format='eps')

if __name__ == "__main__":

    delta_t = 0.5
    culture_momentum = 11
    beta_vals = [0.8,0.6,0.4]
    delta_vals = [0.8,0.7,0.6,0.5]

    FILENAME = "results/plot_discount_factors_beta_delta.eps"
    dpi_save = 1200
    steps = int(culture_momentum/delta_t)

    time_list =  np.asarray([delta_t*x for x in range(steps)])
    const_delta_discount_list, const_beta_discount_list = calc_data_discount(beta_vals, delta_vals,time_list)

    time_list_plot = np.asarray([-delta_t*x for x in range(steps)])#so time is negative, past influences less
    plot_discount_factors_beta_delta(FILENAME, const_delta_discount_list, const_beta_discount_list,beta_vals, delta_vals,time_list_plot,culture_momentum, dpi_save)

    plt.show()
