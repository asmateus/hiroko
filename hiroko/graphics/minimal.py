from graphics.QtAutogen.minimal_autogen import Ui_MainWindow
from graphics.map import Map
from interface.buffer import OnlineBuffer
from core.evolvement import ComposedNaturalEvolution
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

        self.last_data_extension = 0

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

        self.ui.previous_btn.clicked.connect(
            lambda: self.goPrevious())

        self.ui.next_btn.clicked.connect(
            lambda: self.goNext())

    def goPrevious(self):
        if not self.stop_signal:
            self.stopProcess()
            return

        if self.current_head > 0:
            self.scatter_x = self.scatter_x[0: len(self.scatter_x) - 2 * self.last_data_extension]
            self.scatter_y = self.scatter_y[0: len(self.scatter_y) - 2 * self.last_data_extension]

            self.loadEpochData(self.current_head - 1)

    def goNext(self):
        if not self.stop_signal:
            self.stopProcess()
            return

        if not self.prc.isPetriGlassFreezed():
            if self.petri_glass.getPersistentRuleBook()['method'] == 'genetic':
                self.prc.triggerEvolutionStep()
            elif self.petri_glass.getPersistentRuleBook()['method'] == 'random':
                self.prc.randomEvolutionStep()
        else:
            self._endProcess()
            return

        self.loadEpochData(self.current_head + 1)

    def repaintMap(self, map_array):
        h, w, _ = map_array.shape
        pixmap = QPixmap(QImage(map_array, w, h, 3 * w, QImage.Format_RGB888))
        self.ui.map_holder_label.setPixmap(pixmap)

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

        # Assign the correct number of days
        self.petri_glass.getPersistentRuleBook()['day-count'] = self.ui.day_count.value()
        self.petri_glass.spawnNewPopulation()

        # Create a composed natural evolution process
        self.prc = ComposedNaturalEvolution(petri_glass=self.petri_glass, max_epoch_count=500)

        # Update the UI with the data of the buffer using a Timer event
        self.ui_print_timer = QBasicTimer()
        self.ui_print_timer.start(0.1, self)

    def loadEpochData(self, epoch=-1):
        # Obtain data of last epoch by reading the Buffer
        last_data = OnlineBuffer.getInstance().readBuffer(epoch)

        if last_data is not None and len(last_data):
            # Determine whether the epoch count of the ui is up to date with the Buffer
            # If it is, do not do anything, else update plots

            # Reasign head
            self.current_head = last_data[0]

            # Build data for scatter plot
            self.last_data_extension = len(last_data[1][1])
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
            self.repaintMap(self.map.colorMap(best))

            # Set the label texts
            distance = self.prc._calculatePopulationDistance(best)
            deviation = self.prc._calculateStandardDeviation(
                best, self.petri_glass.getInputPopulationSmall())

            self.ui.epoch_counter.setText(
                'Epochs: ' + str(self.current_head) + '  Idle: ' + str(self.prc.count))

            self.ui.distance_info.setText('Best distance: ' + str(distance))
            self.ui.deviation_info.setText('Best deviation: ' + str(int(deviation)))
            self.ui.fitness_info.setText('Fitness Value: ' + str(min(fitness)))

            # Scatter plot
            max_x, max_y = max(self.scatter_x), max(self.scatter_y)
            min_x, min_y = min(self.scatter_x), min(self.scatter_y)
            delta_x, delta_y = (max_x - min_x) / 10, (max_y - min_y) / 10

            self.ui.scatter_plot.setXRange(min_x - delta_x, max_x + delta_x, padding=0)
            self.ui.scatter_plot.setYRange(min_y - delta_y, max_y + delta_y, padding=0)
            self.ui.scatter_plot.plot(
                self.scatter_x,
                self.scatter_y,
                pen=None,
                symbol='o',
                clear=True)

            # Bar plot
            max_x, max_y = len(sums), max(sums)
            min_x, min_y = 0, 0
            delta_x, delta_y = (max_x - min_x) / 10, (max_y - min_y) / 10

            self.ui.bar_plot.setXRange(min_x - delta_x, max_x + delta_x, padding=0)
            self.ui.bar_plot.setYRange(min_y - delta_y, max_y + delta_y, padding=0)
            self.ui.bar_plot.plot(list(range(max_x)), sums, symbol='o', clear=True)

    def timerEvent(self, event):
        if self.stop_signal:
            self.ui_print_timer.stop()
            return

        if not (self.prc.isPetriGlassFreezed() or self.stop_signal):
            if self.petri_glass.getPersistentRuleBook()['method'] == 'genetic':
                self.prc.triggerEvolutionStep()
            elif self.petri_glass.getPersistentRuleBook()['method'] == 'random':
                self.prc.randomEvolutionStep()
        else:
            self._endProcess()
            return

        self.loadEpochData()

    def _endProcess(self):
        # We finished, stop saving data. Close Buffer
        OnlineBuffer.getInstance().close(save=False)
        self.petri_glass.cleanGlass()

        self.stop_signal = True
        self.ui.start_btn.setText('Start')
