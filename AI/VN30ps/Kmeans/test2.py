import seaborn as sns

# tips = sns.load_dataset("tips")
# print(tips)
penguins = sns.load_dataset("penguins")
print(type(penguins))
print(penguins['flipper_length_mm'])
sns.displot(penguins, x="flipper_length_mm")