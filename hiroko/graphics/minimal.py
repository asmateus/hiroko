from graphics.QtAutogen.minimal_autogen import Ui_MainWindow
from interface.buffer import OnlineBuffer
from core.evolvement import ComposedNaturalEvolution
from threading import Thread
from PyQt5 import QtWidgets
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

    def startApplication(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.setup()

        sys.exit(self.app.exec_())

    def setup(self):
        self.ui.scatter_plot.setXRange(1, 100, padding=0)
        self.ui.scatter_plot.setYRange(0.35, 0.4, padding=0)

        self.ui.start_btn.clicked.connect(self.startProcess)

    def startProcess(self):
        if self.ui.start_btn.text() == 'Start':
            self.stop_signal = False

            # Open buffer
            OnlineBuffer.getInstance().open()

            self.print_timer = QBasicTimer()
            self.print_timer.start(10, self)

            # Open process in new thread
            prc = Thread(None, target=self._process, args=())
            prc.daemon = True
            prc.start()

            self.ui.start_btn.setText('Stop')
        else:
            self.stop_signal = True
            print('>> Stop signal reached')
            self.ui.start_btn.setText('Start')

    def timerEvent(self, event):
        if self.stop_signal:
            self.print_timer.stop()

        last_data = OnlineBuffer.getInstance().readBuffer()
        if last_data is not None and len(last_data) > 0:
            if self.current_head is None or self.current_head != last_data[0]:
                self.current_head = last_data[0]
                self.scatter_x.extend([self.current_head] * len(last_data[1][1]))
                self.scatter_y.extend(last_data[1][1])

                self.ui.scatter_plot.plot(self.scatter_x, self.scatter_y, pen=None, symbol='o')

    def _process(self):
        # Trigger evolution process
        evolution_prc = ComposedNaturalEvolution(
            petri_glass=self.petri_glass,
            max_epoch_count=100)
        while not evolution_prc.isPetriGlassFreezed() and not self.stop_signal:
            if self.petri_glass.getPersistentRuleBook()['method'] == 'genetic':
                evolution_prc.triggerEvolutionStep()
            elif self.petri_glass.getPersistentRuleBook()['method'] == 'random':
                evolution_prc.randomEvolutionStep()

        # We finished, close buffer
        self.stop_signal = True
        print('>> Stop signal reached')

        OnlineBuffer.getInstance().close(save=False)

        self.ui.start_btn.setText('Start')
