# PyQt5 Imports
from PyQt5.QtWidgets import (
    QTreeWidgetItem, QCheckBox, QWidget, QHBoxLayout, QLineEdit)
from PyQt5.QtCore import Qt

# Own Imports
from kmap.library.qwidgetsub import (
    CenteredLabel, WeightSpinBox, AngleSpinBox, EnergySpinBox)


class LMFitTreeItem(QTreeWidgetItem):

    def __init__(self, tree):

        super().__init__(tree)

        self.children = []

    def set_vary(self, state):

        self.vary.setChecked(state)

    def change_vary(self, state):

        for child in self.children:
            child.set_vary(state)

    def get_parameters(self):

        parameters = [self.alias_label.text(), self.vary.isChecked(),
                      self.initial_spinbox.value(),
                      self.min_spinbox.value(),
                      self.max_spinbox.value(), self.expression.text()]

        return parameters


class OtherTreeItem(LMFitTreeItem):

    def __init__(self, tree):

        super().__init__(tree)

        self._setup(tree)
        self._connect()

    def get_parameters(self):

        parameters = []

        for i in range(self.childCount()):
            parameters.append(self.child(i).get_parameters())

        return parameters

    def _setup(self, tree):

        self.name_label = CenteredLabel('Other Options')

        self.vary = QCheckBox()
        layout = QHBoxLayout()
        layout.addWidget(self.vary)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        center_widget = QWidget()
        center_widget.setLayout(layout)

        tree.setItemWidget(self, 1, self.name_label)
        tree.setItemWidget(self, 3, center_widget)

        self.alpha = AngleTreeItem(self, tree, '', 'Alpha')
        self.beta = AngleTreeItem(self, tree, '', 'Beta')
        self.background = BackgroundTreeItem(self, tree)
        self.energy = EnergyTreeItem(self, tree)

        self.children = [self.alpha, self.beta, self.background, self.energy]

    def _connect(self):

        self.vary.stateChanged.connect(self.change_vary)


class OrbitalTreeItem(LMFitTreeItem):

    def __init__(self, tree, orbital):

        super().__init__(tree)

        self._setup(tree, orbital)
        self._connect()

    def get_parameters(self):

        parameters = []

        for i in range(self.childCount()):
            parameters.append(self.child(i).get_parameters())

        return parameters

    def _setup(self, tree, orbital):

        self.ID = orbital.ID
        self.ID_label = CenteredLabel('%i' % self.ID)

        self.name_label = CenteredLabel(orbital.name)
        self.name_label.setToolTip(str(orbital))

        self.vary = QCheckBox()
        layout = QHBoxLayout()
        layout.addWidget(self.vary)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        center_widget = QWidget()
        center_widget.setLayout(layout)

        tree.setItemWidget(self, 0, self.ID_label)
        tree.setItemWidget(self, 1, self.name_label)
        tree.setItemWidget(self, 3, center_widget)

        self.weight = WeightTreeItem(self, tree, orbital.ID)
        self.phi = AngleTreeItem(self, tree, orbital.ID, 'Phi')
        self.theta = AngleTreeItem(self, tree, orbital.ID, 'Theta')
        self.psi = AngleTreeItem(self, tree, orbital.ID, 'Psi')

        self.children = [self.weight, self.phi, self.theta, self.psi]

    def _connect(self):

        self.vary.stateChanged.connect(self.change_vary)


class DataTreeItem(LMFitTreeItem):

    def __init__(self, tree):

        super().__init__(tree)

    def _setup(self, tree):

        self.name_label = CenteredLabel('')
        self.alias_label = CenteredLabel('')
        self.expression = QLineEdit()

        self.vary = QCheckBox()
        layout = QHBoxLayout()
        layout.addWidget(self.vary)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        center_widget = QWidget()
        center_widget.setLayout(layout)

        tree.setItemWidget(self, 1, self.name_label)
        tree.setItemWidget(self, 2, self.alias_label)
        tree.setItemWidget(self, 3, center_widget)
        tree.setItemWidget(self, 7, self.expression)


class AngleTreeItem(DataTreeItem):

    def __init__(self, parent, tree, ID, angle):

        super().__init__(parent)

        self._setup(tree, ID, angle)

    def _setup(self, tree, ID, angle):

        super()._setup(tree)

        self.initial_spinbox = AngleSpinBox(0, 'initial_spinbox')
        self.min_spinbox = AngleSpinBox(-90, 'min_spinbox')
        self.max_spinbox = AngleSpinBox(90, 'max_spinbox')

        self.name_label.setText(angle)
        self.alias_label.setText('%s_%s' % (angle.lower(), ID))

        tree.setItemWidget(self, 4, self.initial_spinbox)
        tree.setItemWidget(self, 5, self.min_spinbox)
        tree.setItemWidget(self, 6, self.max_spinbox)


class BackgroundTreeItem(DataTreeItem):

    def __init__(self, parent, tree):

        super().__init__(parent)

        self._setup(tree)

    def _setup(self, tree):

        super()._setup(tree)

        self.initial_spinbox = WeightSpinBox()
        self.min_spinbox = WeightSpinBox(value=-99999.9)
        self.max_spinbox = WeightSpinBox(value=99999.9)

        self.name_label.setText('Background')
        self.alias_label.setText('c')

        tree.setItemWidget(self, 4, self.initial_spinbox)
        tree.setItemWidget(self, 5, self.min_spinbox)
        tree.setItemWidget(self, 6, self.max_spinbox)


class EnergyTreeItem(DataTreeItem):

    def __init__(self, parent, tree):

        super().__init__(parent)

        self._setup(tree)

    def _setup(self, tree):

        super()._setup(tree)

        self.initial_spinbox = EnergySpinBox()
        self.min_spinbox = EnergySpinBox(value=5)
        self.max_spinbox = EnergySpinBox(value=150)

        self.name_label.setText('Kinetic Energy')
        self.alias_label.setText('E_kin')

        tree.setItemWidget(self, 4, self.initial_spinbox)
        tree.setItemWidget(self, 5, self.min_spinbox)
        tree.setItemWidget(self, 6, self.max_spinbox)


class WeightTreeItem(DataTreeItem):

    def __init__(self, parent, tree, ID):

        super().__init__(parent)

        self._setup(tree, ID)

    def _setup(self, tree, ID):

        super()._setup(tree)

        self.initial_spinbox = WeightSpinBox()
        self.min_spinbox = WeightSpinBox(value=-99999.9)
        self.max_spinbox = WeightSpinBox(value=99999.9)

        self.name_label.setText('Weight')
        self.alias_label.setText('w_%i' % ID)

        tree.setItemWidget(self, 4, self.initial_spinbox)
        tree.setItemWidget(self, 5, self.min_spinbox)
        tree.setItemWidget(self, 6, self.max_spinbox)
