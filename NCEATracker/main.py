import sqlite3 as sql
import matplotlib.pyplot as plt

labels = ["A", "B", "C"]
sizes = [40, 35, 25]

plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
plt.axis("equal")  # keeps it circular instead of a sad oval
plt.show()
