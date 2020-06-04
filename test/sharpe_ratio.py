# import numpy as np
# import pandas as pd
#
# # Simulate cumulative returns of 100 days
# N = 100
# R = pd.DataFrame(np.random.normal(size=100)).cumsum()
# # print(R)
#
# # Approach 1
# r = (R - R.shift(1))/R.shift(1)
#
# # Approach 2
# r = R.diff()
# print(r)
#
# sr = r.mean()/r.std() * np.sqrt(252)
#
# print(sr)