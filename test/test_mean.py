import scipy.stats as stats
import numpy as np

# We'll use these two data sets as examples
x1 = [1, 2, 2, 3, 4, 5, 5, 7]
x2 = x1 + [100]
print(x2)
print('Mean of x1:', sum(x1), '/', len(x1), '=', np.mean(x1))
print('Mean of x2:', sum(x2), '/', len(x2), '=', np.mean(x2))
