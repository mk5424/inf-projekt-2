from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainterPath, QPen, QColor

class Rura:
    def __init__(self, punkty, kolor, grubosc=12):
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.kolor_rury = Qt.gray
        self.kolor_obrys = Qt.black
        self.kolor_cieczy = kolor
        self.czy_plynie = False

    def ustaw_przeplyw(self, plynie):
        self.czy_plynie = plynie

    def draw(self, painter):
        if len(self.punkty) < 2:
            return
        path = QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:-1]:
            path.lineTo(p)
        pen_obrys = QPen(self.kolor_obrys, self.grubosc)
        painter.setPen(pen_obrys)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        pen_rura = QPen(self.kolor_rury, self.grubosc - 6)
        painter.setPen(pen_rura)
        painter.drawPath(path)
        if self.czy_plynie:
            pen_ciecz = QPen(self.kolor_cieczy, self.grubosc - 6)
            painter.setPen(pen_ciecz)
            path.lineTo(self.punkty[-1])
            painter.drawPath(path)