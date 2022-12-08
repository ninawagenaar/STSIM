import numpy as np
import math
import matplotlib.pyplot as plt

# Calculates the average waiting time for a mmc queue using Adan and Resing (2002)
def waittime_mmc(lam, mu, c):
    rho = lam / (c * mu)
    blockprob = PIw(rho, c)
    return blockprob * (1/(1-rho)) * (1/(c*mu))

# Calculates the blocking probability as described in Adan and Resing (2002)
def PIw(rho, c):
    numerator = (c*rho)**c / math.factorial(c)
    summation = 0
    for n in range(0, c):
        summation += (c*rho)**n / math.factorial(n)
    denominator = ((1-rho) * summation + ((c*rho)**c/ math.factorial(c)))
    return numerator / denominator

if __name__ == "__main__":
    min = 1
    max = 100
    c = np.arange(min, max)
    averages = np.arange(min, max)
    lam = 0.9
    mu = 1
    # for i in range(0, max-min):
    #     averages[i] = waittime_mmc(c[i]*lam, mu, c[i])

    # plt.plot(c, np.log(averages))
    # plt.show()

    for i in range(1, 10000):
        print(i, waittime_mmc(i*lam, mu, i))
