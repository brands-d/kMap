# Imports
'''PlotData ist eine Klasse die ich geschrieben habe, die du wenn du es
für sinnvoll erachtest, verwenden kannst. Sie definiert im Prinzip nur
ein 2D data array mit x- und y-Achsen, kommt aber mit einer eingebauten
Interpolationsmethode und kann Achsen aus Range-Werten rechnen. Z.B. als
return value für get_kmap.'''
from plotdata import PlotData

# Hauptklasse
'''Nach außen nur eine Klasse Orbital die möglichst allgemein Cube Files
lest und die Daten in irgendeiner Form zu Verfügung stellt. Kann
beliebig viele private Methoden definieren (der Name von privaten
Attributen sollte mit _ beginnen) und sollte nur einige wenige
notwendige Methoden nach außen definieren.'''
class Orbital():

    # Konstruktor
    '''Map.py liefert das Cube File (vermutlich
    als String; das File-Handling sollte bevorzugterweise außerhalb
    dieser Klasse gemacht werden, dann kann Map.py verschiedene Arten
    wie das Einlesen aus einer Datenbank übernehmen) und alle anderen
    Parameter die du brauchst.'''
    def __init__(self, cube, *args, **kwargs):
        pass

    # Öffentliche Methoden
    '''Sollte eine fertige kmap zurückliefern (z.B. als PlotData Objekt,
    wenn du das für sinnvoll hälst. Ansonsten reicht denk ich eine 2D
    Liste auch). Welche Argumente du benötigst musst du vorgeben und Map
    wird diese dann liefern. Aus Performancegründen schlage ich vor die
    Berechnung lazy zu machen, also erst eine kmap zu berechnen wenn sie
    gefordert wird.'''
    def get_kmap(self, *args, **kwargs):
        pass
        return PlotData

    '''Eine Methode die alle relevanten Informationen in irgendeiner
    Form zurückgibt. Das wäre hilfreich um das Orbital als ganzes zu
    speichern oder dem User/der Userin anzuzeigen. Ich habe jetzt
    einfach mal ein dictionary als return Wert angenommen, du kannst
    aber ein beliebiges für dich sinnvolles Format wählen (z.B. die
    __str__ Methode überschreiben).'''
    def to_dict(self, *args, **kwargs):
        pass
        return {}

    '''Andere öffentliche Methoden die du vielleicht verwenden möchtest.
    Eine Alternative wäre, alle diese Werte als Argumente der get_kmap Methode zu geben, und diese Methoden hier auf private zu stellen.'''
    def set_polarization(self, *args, **kwargs):
        pass

    def set_orientation(self, *args, **kwargs):
        pass

    def set_kinetic_energy(self, *args, **kwargs):
        pass

    # Private Methoden
    '''Etwaige Hilfsmethoden innerhalb von Orbital. Sollten nicht von
    außerhalb aufgerufen werden und daher mit _ im Namen starten.'''
    def _aux_intern_method1(self, *args, **kwargs):
        pass


# Amerkungen:
'''Alle Methoden zum plotten z.B. denke ich kann man rausstreichen.
Wie und wo geplottet wird, darum soll sich der User außerhalb (Map.py)
selber kümmern.'''
'''Wenn möglich sollte Orbital die originalen Werte nicht überschreiben
sondern alle Berechnungen immer von diesen ausgehen machen.'''


# Hilfsklassen
'''Etwaige Hilfsklassen die du brauchst (zB. mommap). Im Optimalfall
sollten Map davon nichts mitbekommen.'''
class AuxClass1():
    pass


# Was ich damit machen möchte
'''Ich würde dann von Orbital erben und damit die gesamte Funktionalität
von Orbital haben, plus alle Map.py spezifischen Dinge die ich dann
hinzufügen kann. Ab hier kümmere ich mich darum!'''
class SimData(Orbital):

    def __init__(self):

        super().__init__()
