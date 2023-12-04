from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLineEdit,
    QTreeWidgetItem,
    QWidget,
)

from kmap.library.qwidgetsub import (
    AngleSpinBox,
    BackgroundSpinBox,
    CenteredLabel,
    EnergySpinBox,
    InnerPotentialSpinBox,
    WeightSpinBox,
)


class SignalObject(QObject):
    value_changed = Signal()
    boundary_changed = Signal()
    expression_changed = Signal()
    vary_changed = Signal()


class LMFitTreeItem(QTreeWidgetItem):
    def __init__(self, tree):
        super().__init__(tree)

        self.children = []

    def is_vary(self):
        return self.vary.isChecked()

    def set_vary(self, state):
        self.vary.setChecked(state)

    def _setup(self, tree, name):
        self.name_label = CenteredLabel(name)

        self.vary = QCheckBox()
        layout = QHBoxLayout()
        layout.addWidget(self.vary)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        center_widget = QWidget()
        center_widget.setLayout(layout)

        tree.setItemWidget(self, 1, self.name_label)
        tree.setItemWidget(self, 3, center_widget)


class LMFitTreeTopLevelItem(LMFitTreeItem):
    def __init__(self, tree):
        super().__init__(tree)
        self.signals = SignalObject()

    def save_state(self):
        save = [child.save_state() for child in self.children]

        return save

    def restore_state(self, save):
        for i, child in enumerate(self.children):
            child.restore_state(save[i])

    def change_vary(self, state):
        for child in self.children:
            child.set_vary(state)

    def _change_to_matrix_state(self, state):
        self.vary.setEnabled(not state)

        for child in self.children:
            child._change_to_matrix_state(state)

    def _connect_child(self, child):
        # value_changed == redraw necessary
        child.signals.value_changed.connect(self.signals.value_changed.emit)
        child.signals.vary_changed.connect(self.signals.vary_changed.emit)

    def _connect(self):
        self.vary.stateChanged.connect(self.change_vary)

        for child in self.children:
            self._connect_child(child)


class BackgroundOptionsTreeItem(LMFitTreeTopLevelItem):
    def __init__(self, tree, parameters):
        super().__init__(tree)

        self._setup(tree, parameters)
        self._connect()

    def add_equation_parameter(self, tree, parameter):
        name = parameter.name
        if name not in self.parameters:
            item = BackgroundTreeItem(self, tree, parameter, "Eq. Parameter")
            self._connect_child(item)
            self.children.append(item)
            self.parameters.append(name)

        else:
            index = self.parameters.index(name)
            item = self.children[index]
            item.update_parameter(parameter)

    def _change_to_matrix_state(self, state):
        super()._change_to_matrix_state(state)

    def _setup(self, tree, parameters):
        super()._setup(tree, "Background Options")

        self.children = []
        self.parameters = []


class OrbitalOptionsTreeItem(LMFitTreeTopLevelItem):
    def __init__(self, tree, parameters):
        super().__init__(tree)

        self._setup(tree, parameters)
        self._connect()

    def _setup(self, tree, parameters):
        super()._setup(tree, "Orbital Options")

        alpha = AngleTreeItem(self, tree, parameters["alpha"], "Alpha")
        beta = AngleTreeItem(self, tree, parameters["beta"], "Beta")
        energy = EnergyTreeItem(self, tree, parameters["E_kin"], "Kinetic Energy")
        V0 = InnerPotentialTreeItem(self, tree, parameters["V0"], "Inner Potential")

        self.children = [alpha, beta, energy, V0]
        self.parameters = ["alpha", "beta", "E_kin", "V0"]


class OrbitalTreeItem(LMFitTreeTopLevelItem):
    def __init__(self, tree, orbital, parameters):
        super().__init__(tree)

        self.ID = orbital.ID
        self._setup(tree, orbital, parameters)
        self._connect()

    def _setup(self, tree, orbital, parameters):
        super()._setup(tree, orbital.name)

        self.ID_label = CenteredLabel("%i" % self.ID)
        self.name_label.setToolTip(str(orbital))
        tree.setItemWidget(self, 0, self.ID_label)

        weight = WeightTreeItem(self, tree, parameters["w_" + str(self.ID)], "Weight")
        phi = AngleTreeItem(self, tree, parameters["phi_" + str(self.ID)], "Phi")
        theta = AngleTreeItem(self, tree, parameters["theta_" + str(self.ID)], "Theta")
        psi = AngleTreeItem(self, tree, parameters["psi_" + str(self.ID)], "Psi")

        self.children = [weight, phi, theta, psi]


class LMFitDataTreeItem(LMFitTreeItem):
    def __init__(self, parent, parameter):
        self.parameter = parameter
        self.signals = SignalObject()

        super().__init__(parent)

    def save_state(self):
        save = {
            "vary": self.vary.isChecked(),
            "initial": self.initial_spinbox.value(),
            "min": self.min_spinbox.value(),
            "max": self.max_spinbox.value(),
            "expr": self.expression.text(),
        }

        return save

    def restore_state(self, save):
        self.vary.setChecked(save["vary"])
        self.initial_spinbox.setValue(save["initial"])
        self.min_spinbox.setValue(save["min"])
        self.max_spinbox.setValue(save["max"])
        self.expression.setText(save["expr"])

    def _change_to_matrix_state(self, state):
        self.vary.setEnabled(not state)
        self.min_spinbox.setEnabled(not state)
        self.max_spinbox.setEnabled(not state)
        self.expression.setEnabled(not state)

    def _change_initial(self, value):
        self.parameter.value = value
        self.signals.value_changed.emit()

    def _change_min(self, value):
        self.parameter.min = value
        self.signals.boundary_changed.emit()

    def _change_max(self, value):
        self.parameter.max = value
        self.signals.boundary_changed.emit()

    def _change_expression(self):
        self.parameter.expr = self.expression.text()
        self.signals.expression_changed.emit()

    def _change_vary(self, state):
        self.parameter.vary = bool(state)
        self.signals.vary_changed.emit()

    def _setup(self, tree, name):
        name = self.parameter.name if name is None else name
        super()._setup(tree, name)

        self.alias_label = CenteredLabel(self.parameter.name)
        expression = "" if self.parameter.expr is None else self.parameter.expr
        self.expression = QLineEdit(expression)

        tree.setItemWidget(self, 2, self.alias_label)
        tree.setItemWidget(self, 4, self.initial_spinbox)
        tree.setItemWidget(self, 5, self.min_spinbox)
        tree.setItemWidget(self, 6, self.max_spinbox)
        tree.setItemWidget(self, 7, self.expression)

    def _connect(self):
        self.initial_spinbox.valueChanged.connect(self._change_initial)
        self.min_spinbox.valueChanged.connect(self._change_min)
        self.max_spinbox.valueChanged.connect(self._change_max)
        self.expression.returnPressed.connect(self._change_expression)
        self.vary.stateChanged.connect(self._change_vary)


class AngleTreeItem(LMFitDataTreeItem):
    def __init__(self, parent, tree, parameter, name=None):
        super().__init__(parent, parameter)

        self._setup(tree, name)
        self._connect()

    def _setup(self, tree, name):
        initial = self.parameter.value
        min_ = self.parameter.min
        max_ = self.parameter.max

        self.initial_spinbox = AngleSpinBox(initial, "initial_spinbox")
        self.min_spinbox = AngleSpinBox(min_, "min_spinbox")
        self.max_spinbox = AngleSpinBox(max_, "max_spinbox")

        super()._setup(tree, name)


class BackgroundTreeItem(LMFitDataTreeItem):
    def __init__(self, parent, tree, parameter, name=None):
        super().__init__(parent, parameter)

        self._setup(tree, name)
        self._connect()

    def update_parameter(self, parameter):
        initial = self.parameter.value
        min_ = self.parameter.min
        max_ = self.parameter.max
        expr = self.parameter.expr
        vary = self.parameter.vary

        self.parameter = parameter

        self._change_initial(initial)
        self._change_min(min_)
        self._change_max(max_)
        self._change_expression(expr)
        self._change_vary(vary)

    def _change_to_matrix_state(self, state):
        super()._change_to_matrix_state(state)

        if state and self.parameter.name == "c":
            if self.initial_spinbox.value() == 0.0:
                self.initial_spinbox.setValue(1.0)

            self.vary.setEnabled(True)

    def _setup(self, tree, name):
        initial = self.parameter.value
        min_ = self.parameter.min
        max_ = self.parameter.max

        self.initial_spinbox = BackgroundSpinBox(value=initial)
        self.min_spinbox = BackgroundSpinBox(value=min_)
        self.max_spinbox = BackgroundSpinBox(value=max_)

        super()._setup(tree, name)


class EnergyTreeItem(LMFitDataTreeItem):
    def __init__(self, parent, tree, parameter, name=None):
        super().__init__(parent, parameter)

        self._setup(tree, name)
        self._connect()

    def _setup(self, tree, name):
        initial = self.parameter.value
        min_ = self.parameter.min
        max_ = self.parameter.max

        self.initial_spinbox = EnergySpinBox(value=initial)
        self.min_spinbox = EnergySpinBox(value=min_)
        self.max_spinbox = EnergySpinBox(value=max_)

        super()._setup(tree, name)


class InnerPotentialTreeItem(LMFitDataTreeItem):
    def __init__(self, parent, tree, parameter, name=None):
        super().__init__(parent, parameter)

        self._setup(tree, name)
        self._connect()

    def _setup(self, tree, name):
        initial = self.parameter.value
        min_ = self.parameter.min
        max_ = self.parameter.max

        self.initial_spinbox = InnerPotentialSpinBox(value=initial)
        self.min_spinbox = InnerPotentialSpinBox(value=min_)
        self.max_spinbox = InnerPotentialSpinBox(value=max_)

        super()._setup(tree, name)


class WeightTreeItem(LMFitDataTreeItem):
    def __init__(self, parent, tree, parameter, name=None):
        super().__init__(parent, parameter)

        self._setup(tree, name)
        self._connect()

    def _change_to_matrix_state(self, state):
        super()._change_to_matrix_state(state)
        self.min_spinbox.setMinimum(-99999999 if state else 0)
        self.min_spinbox.setValue(-99999999 if state else 0)
        self.initial_spinbox.setMinimum(-99999999 if state else 0)
        self.vary.setEnabled(True)

    def _setup(self, tree, name):
        initial = self.parameter.value
        min_ = self.parameter.min
        max_ = self.parameter.max

        self.initial_spinbox = WeightSpinBox(value=initial)
        self.min_spinbox = WeightSpinBox(value=min_)
        self.max_spinbox = WeightSpinBox(value=max_)

        super()._setup(tree, name)


class LMFitResultTreeItem(QTreeWidgetItem):
    def __init__(self, parent):
        super().__init__(parent)

        self.children = []
        self.parameters = []

    def update_result(self, result):
        for child, param in zip(self.children, self.parameters):
            child.update_result(result[param])

    def _setup(self, tree, name):
        self.name_label = CenteredLabel(name)

        tree.setItemWidget(self, 1, self.name_label)


class BackgroundOptionsResultTreeItem(LMFitResultTreeItem):
    def __init__(self, tree, result, background_variables=[]):
        super().__init__(tree)

        self._setup(tree, result, background_variables)

    def _setup(self, tree, result, background_variables):
        super()._setup(tree, "Background Options")

        self.parameters = []
        self.children = []

        for key in background_variables:
            item = DataResultTreeItem(
                self, tree, result[key], "Eq. Parameter", units="", decimals=1
            )
            self.parameters.append(key)
            self.children.append(item)


class OrbitalOptionsResultTreeItem(LMFitResultTreeItem):
    def __init__(self, tree, result):
        super().__init__(tree)

        self._setup(tree, result)

    def _setup(self, tree, result):
        super()._setup(tree, "Orbital Options")

        alpha = DataResultTreeItem(
            self, tree, result["alpha"], "Alpha", units="°", decimals=3
        )
        beta = DataResultTreeItem(
            self, tree, result["beta"], "Beta", units="°", decimals=3
        )
        energy = DataResultTreeItem(
            self, tree, result["E_kin"], "Kinetic Engery", units="  eV", decimals=2
        )
        V0 = DataResultTreeItem(
            self, tree, result["V0"], "Inner Potential", units="  eV", decimals=2
        )

        self.parameters = ["alpha", "beta", "E_kin", "V0"]
        self.children = [alpha, beta, energy, V0]


class OrbitalResultTreeItem(LMFitResultTreeItem):
    def __init__(self, tree, orbital, result):
        super().__init__(tree)

        self._setup(tree, orbital, result)

    def _setup(self, tree, orbital, result):
        super()._setup(tree, orbital.name)
        self.name_label.setToolTip(str(orbital))

        self.ID = orbital.ID
        self.ID_label = CenteredLabel("%i" % self.ID)
        tree.setItemWidget(self, 0, self.ID_label)

        weight = DataResultTreeItem(
            self, tree, result["w_" + str(self.ID)], "Weight", units="", decimals=2
        )
        phi = DataResultTreeItem(
            self, tree, result["phi_" + str(self.ID)], "Phi", units="°", decimals=3
        )
        theta = DataResultTreeItem(
            self, tree, result["theta_" + str(self.ID)], "Theta", units="°", decimals=3
        )
        psi = DataResultTreeItem(
            self, tree, result["psi_" + str(self.ID)], "Psi", units="°", decimals=3
        )

        self.parameters = [
            variable + "_" + str(self.ID) for variable in ["w", "phi", "theta", "psi"]
        ]
        self.children = [weight, phi, theta, psi]


class DataResultTreeItem(LMFitResultTreeItem):
    def __init__(self, parent, tree, parameter, name, units, decimals):
        self.units = units
        self.decimals = decimals

        super().__init__(parent)
        self._setup(tree, parameter, name)

    def update_result(self, parameter):
        self.parameter = parameter
        self._update_text()

    def _update_text(self):
        value = self.parameter.value
        stderr = self.parameter.stderr

        alias = self.parameter.name

        value = "%.{0}f%s".format(self.decimals) % (value, self.units)

        if stderr is None:
            stderr = "-"

        else:
            stderr = "%.{0}f%s".format(self.decimals) % (stderr, self.units)

        self.alias_label.setText(alias)
        self.result.setText(value)
        self.stderr.setText(stderr)

    def _setup(self, tree, parameter, name):
        super()._setup(tree, name)

        self.alias_label = CenteredLabel()
        self.result = CenteredLabel("")
        self.stderr = CenteredLabel("")

        tree.setItemWidget(self, 2, self.alias_label)
        tree.setItemWidget(self, 3, self.result)
        tree.setItemWidget(self, 4, self.stderr)

        self.update_result(parameter)
