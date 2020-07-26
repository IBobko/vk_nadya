import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


def get_time_str(t):
    return datetime.fromtimestamp(t).strftime("%H:%M:%S")


def get_date_str(t):
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d")


df = pd.read_csv("/home/igor/Nadya/onlines/{}.csv".format(datetime.now().strftime("%Y-%m-%d")),
                 names=["time", "online"],
                 dtype={'time': int, 'online': int})
start = -1

poses = []
last = -1
for index, row in df.iterrows():
    if row[1] == 1 and start == -1:
        start = index
    if last != row[1]:
        last = row[1]
        poses.append(row[0])

df = df.iloc[start:]

ax = df.plot(x="time", y="online", kind="scatter", marker='.', title=get_date_str(df.iloc[0, 0]), grid=True)
ax.set_xticks(poses)
ax.figure.canvas.draw()


labels = [get_time_str(item._x) for item in ax.get_xticklabels()]
ax.set_xticklabels(labels, rotation='vertical')
plt.show()
pd




