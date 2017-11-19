from graphics.QtAutogen.minimal_autogen import Ui_MainWindow
from graphics.map import Map
from interface.buffer import OnlineBuffer
from core.evolvement import ComposedNaturalEvolution
from threading import Thread
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QBasicTimer
import sys


class MinimalApplication(QtWidgets.QMainWindow):
    def __init__(self, petri_glass, app=QtWidgets.QApplication(sys.argv)):
        super(MinimalApplication, self).__init__()
        self.petri_glass = petri_glass

        self.stop_signal = True
        self.current_head = None
        self.app = app
        self.ui = None

        self.print_timer = None

        self.scatter_x = list()
        self.scatter_y = list()

        # Create a map object for the map holder
        self.map = Map(self.petri_glass.getNeighborhoodEnumerator())

    def startApplication(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.setup()

        sys.exit(self.app.exec_())

    def setup(self):
        self.ui.scatter_plot.setMouseEnabled(x=False, y=False)
        self.ui.scatter_plot.setXRange(1, 100, padding=0)
        self.ui.scatter_plot.setYRange(0.35, 0.4, padding=0)

        # Inialize map holder with mask
        self.repaintMap(self.map.colorMap())

        # Action connections
        self.ui.start_btn.clicked.connect(
            lambda: self.startProcess() if self.stop_signal else self.stopProcess())

    def repaintMap(self, map_array):
        h, w, _ = map_array.shape
        pixmap = QPixmap(QImage(map_array, w, h, 3 * w, QImage.Format_RGB888))
        # self.ui.map_holder_label.setPixmap(pixmap)

    def stopProcess(self):
        # Visual signal to user that process stopped
        self.stop_signal = True
        self.ui.start_btn.setText('Start')

    def startProcess(self):
        # Visual signal to user that process began
        self.stop_signal = False
        self.ui.start_btn.setText('Stop')

        # ****************
        # Starting process
        # ****************

        # Open buffer for data registration
        OnlineBuffer.getInstance().open()

        # Start the genetic algorithm with the current configuration. In a new thread
        algorithm = Thread(None, target=self._process, args=())
        algorithm.daemon = True  # Bind it to the external context
        algorithm.start()

        # Update the UI with the data of the buffer using a Timer event
        self.ui_print_timer = QBasicTimer()
        self.ui_print_timer.start(0.1, self)

    def timerEvent(self, event):
        if self.stop_signal:
            self.ui_print_timer.stop()

        # Obtain data of last epoch by reading the Buffer
        last_data = OnlineBuffer.getInstance().readBuffer()

        if last_data is not None and len(last_data):
            # Determine whether the epoch count of the ui is up to date with the Buffer
            # If it is, do not do anything, else update plots
            if self.current_head is None or self.current_head != last_data[0]:
                # Reasign head
                self.current_head = last_data[0]

                # Build data for scatter plot
                self.scatter_x.extend([self.current_head] * len(last_data[1][1]))
                self.scatter_y.extend(last_data[1][1])

                # Build data for bar plot
                fitness = last_data[1][1]
                best_index = fitness.index(min(fitness))
                best = last_data[1][0][best_index]
                sums = ComposedNaturalEvolution._getCountsPerDay(
                    best,
                    self.petri_glass.getInputPopulationSmall())

                # ***********************************
                # Set up the plot containers and plot
                # ***********************************

                # Paint map
                while(1):
                    self.repaintMap(self.map.colorMap(best))

                # Scatter plot
                max_x, max_y = max(self.scatter_x), max(self.scatter_y)
                min_x, min_y = min(self.scatter_x), min(self.scatter_y)
                delta_x, delta_y = (max_x - min_x) / 10, (max_y - min_y) / 10

                # self.ui.scatter_plot.setXRange(min_x - delta_x, max_x + delta_x, padding=0)
                # self.ui.scatter_plot.setYRange(min_y - delta_y, max_y + delta_y, padding=0)
                # self.ui.scatter_plot.plot(
                #    self.scatter_x,
                #    self.scatter_y,
                #    pen=None,
                #    symbol='o',
                #    clear=True)

                # Bar plot
                max_x, max_y = len(sums), max(sums)
                min_x, min_y = 0, 0
                delta_x, delta_y = (max_x - min_x) / 10, (max_y - min_y) / 10

                # self.ui.bar_plot.setXRange(min_x - delta_x, max_x + delta_x, padding=0)
                # self.ui.bar_plot.setYRange(min_y - delta_y, max_y + delta_y, padding=0)
                # self.ui.bar_plot.plot(list(range(max_x)), sums, symbol='o', clear=True)

    def _process(self):
        # Create a composed natural evolution process
        prc = ComposedNaturalEvolution(petri_glass=self.petri_glass, max_epoch_count=1)

        # Iterate over the epochs while the petriglass is not freezed or no stop signal is called
        while not (prc.isPetriGlassFreezed() or self.stop_signal):
            if self.petri_glass.getPersistentRuleBook()['method'] == 'genetic':
                pass  # prc.triggerEvolutionStep()
            elif self.petri_glass.getPersistentRuleBook()['method'] == 'random':
                pass  # prc.randomEvolutionStep()

        self._endProcess()

    def _endProcess(self):
        # We finished, stop saving data. Close Buffer
        OnlineBuffer.getInstance().close(save=False)
        self.petri_glass.cleanGlass()

        self.stop_signal = True
        self.ui.start_btn.setText('Start')
