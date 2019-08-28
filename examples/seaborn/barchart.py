import seaborn as sns
import matplotlib.pyplot as plt
iris = sns.load_dataset("iris")    # 붓꽃 데이터
x = iris.petal_length.values
sns.rugplot(x)
plt.title("leaf length of Iris")
plt.show()
