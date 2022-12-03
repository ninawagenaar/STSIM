import numpy as np
import math

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
    lam = 0.9
    mu = 1
    for i in range(1, 100):
        print(i, waittime_mmc(lam, mu, i))
