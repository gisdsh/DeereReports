from PySide6.QtWidgets import QMainWindow, QHeaderView, QVBoxLayout

import logic.logic
from ui.ui_mainwindow import Ui_MainWindow
from logic.logic import process_machine_measurements
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.centralwidget.setVisible(False)
        self.btnQuery.clicked.connect(self.trigger_process_machine_measurements)
        self.canvas = MplCanvas(width=12, height=6, dpi=100)
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.canvas)
        self.wdg1.setLayout(self.layout1)
        self.plot_ref = None

    def trigger_process_machine_measurements(self):
        process_machine_measurements(self)


class MplCanvas(FigureCanvas):
    """A canvas that integrates a Matplotlib Figure directly as a QWidget."""

    def __init__(self, parent=None, width=12, height=6, dpi=100):
        # Create the standard Matplotlib Figure and Axes
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        # Initialize the FigureCanvas with the figure
        super().__init__(self.fig)
