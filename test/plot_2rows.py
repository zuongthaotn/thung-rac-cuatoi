import numpy as np
import matplotlib.pyplot as plt

data = np.random.randn(30).cumsum()

plt.plot(data,  label='Default', color="red")

plt.plot(data, 'k-', drawstyle='steps-post', label='steps-post')
plt.legend(loc='best')

plt.show()
