import sys
from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtCharts import QChart, QChartView, QPieSeries

app = QApplication(sys.argv)

"""
series = QPieSeries()
series.append("Math", 30)
series.append("Science", 25)
series.append("English", 45)

chart = QChart()
chart.addSeries(series)
chart.setTitle("2025 Credits")

chart_view = QChartView(chart)
chart_view.setRenderHint(chart_view.renderHints())
"""

window = QMainWindow()
# window.setCentralWidget(chart_view) --> gonna be used later on
window.resize(1900, 1600)  # fullscreen on macbook air m1
window.show()

app.exec()
