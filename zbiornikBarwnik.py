from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath

class zbiornikBarwnik:
    def __init__(self, x, y, kolor):
        self.x = x
        self.y = y
        self.kolor = kolor
        self.ruraPrzylaczeX = self.x + 50
        self.ruraPrzylaczeY = self.y + 246
        self.pojemnosc = 100.0
        self.aktualna_ilosc = 100.0
        self.poziom = 1.0
        self.zawor_otwarty = False

    def otworz_zawor(self):
        self.zawor_otwarty = True

    def zamknij_zawor(self):
        self.zawor_otwarty = False

    def przelacz_zawor(self):
        self.zawor_otwarty = not self.zawor_otwarty

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc

    def dodaj_ciecz(self, ilosc):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano

    def usun_ciecz(self, ilosc):
        if not self.zawor_otwarty:
            return 0.0
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        return usunieto

    def czy_pusty(self):
        return self.aktualna_ilosc <= 0.1

    def czy_pelny(self):
        return self.aktualna_ilosc >= self.pojemnosc - 0.1

    def rysujZbiornik(self, malarz):
        if self.poziom > 0:
            h_cieczy = 161 * self.poziom
            y_start = self.y + 190 - h_cieczy
            malarz.setPen(Qt.NoPen)
            malarz.setBrush(self.kolor)
            malarz.drawRect(int(self.x + 1), int(y_start), 98, int(h_cieczy))

            p = QPainterPath()
            p.moveTo(self.x + 100, self.y + 180)
            p.cubicTo(self.x + 100, self.y + 195, self.x, self.y + 195, self.x, self.y + 180)
            p.lineTo(self.x, self.y + 205)
            p.lineTo(self.x + 100, self.y + 205)
            p.closeSubpath()
            malarz.setBrush(QColor(240, 240, 240))
            malarz.drawPath(p)

            p = QPainterPath()
            p.moveTo(self.x, self.y + 50)
            p.cubicTo(self.x, self.y + 20, self.x + 100, self.y + 20, self.x + 100, self.y + 50)
            p.lineTo(self.x + 100, self.y - 10)
            p.lineTo(self.x, self.y - 10)
            p.closeSubpath()
            malarz.setBrush(QColor(240, 240, 240))
            malarz.drawPath(p)

        malarz.setPen(QPen(QColor(0, 0, 0), 3))
        malarz.setBrush(Qt.NoBrush)
        p = QPainterPath()
        p.moveTo(self.x, self.y + 180)
        p.lineTo(self.x, self.y + 50)
        p.cubicTo(self.x, self.y + 20, self.x + 100, self.y + 20, self.x + 100, self.y + 50)
        p.lineTo(self.x + 100, self.y + 180)
        p.cubicTo(self.x + 100, self.y + 195, self.x, self.y + 195, self.x, self.y + 180)
        p.closeSubpath()
        malarz.drawPath(p)

        malarz.setPen(QPen(QColor(0, 0, 0), 3))
        malarz.setBrush(QColor(180, 180, 180))
        p = QPainterPath()
        zawor_x = self.x + 50 - 20
        zawor_y = self.y + 190
        p.addRect(zawor_x + 6, zawor_y, 28, 6)
        p.addRect(zawor_x + 12, zawor_y + 6, 16, 40)
        p.addRect(zawor_x + 6, zawor_y + 46, 28, 6)
        p.moveTo(zawor_x, zawor_y + 20)
        p.lineTo(zawor_x + 40, zawor_y + 30)
        p.moveTo(zawor_x + 40, zawor_y + 20)
        p.lineTo(zawor_x, zawor_y + 30)
        malarz.drawPath(p)