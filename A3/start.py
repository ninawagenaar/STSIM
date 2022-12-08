
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = '14'



x = np.arange(0, 20)
y = x**2
# plt.figure(figsize=(20, 20), dpi=500)
plt.plot(x, y)
plt.xlabel("lorem ipsum dolor si amet")
plt.ylabel("lorem ipsum dolor si amet")
plt.title("lorem ipsum dolor si amet")
plt.legend()
plt.savefig("test.png", dpi=300)
plt.show()