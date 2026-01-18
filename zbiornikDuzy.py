from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath

class zbiornikDuzy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pojemnosc = 300.0
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0
        self.ilosc_r = 0.0
        self.ilosc_g = 0.0
        self.ilosc_b = 0.0
        self.kolor = QColor(0, 0, 0)

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc

    def aktualizuj_kolor(self):
        if self.aktualna_ilosc <= 0:
            self.kolor = QColor(0, 0, 0)
            return
        r = int((self.ilosc_r / self.aktualna_ilosc) * 255)
        g = int((self.ilosc_g / self.aktualna_ilosc) * 255)
        b = int((self.ilosc_b / self.aktualna_ilosc) * 255)
        self.kolor = QColor(r, g, b)

    def dodaj_ciecz(self, ilosc, kolor):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        if dodano <= 0:
            return 0
        r = kolor.red() / 255.0
        g = kolor.green() / 255.0
        b = kolor.blue() / 255.0
        self.ilosc_r += dodano * r
        self.ilosc_g += dodano * g
        self.ilosc_b += dodano * b
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        self.aktualizuj_kolor()
        return dodano

    def usun_ciecz(self, ilosc):
        if self.aktualna_ilosc <= 0:
            return 0
        usunieto = min(ilosc, self.aktualna_ilosc)
        proporcja = usunieto / self.aktualna_ilosc
        self.ilosc_r -= self.ilosc_r * proporcja
        self.ilosc_g -= self.ilosc_g * proporcja
        self.ilosc_b -= self.ilosc_b * proporcja
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        self.aktualizuj_kolor()
        return usunieto

    def czy_pusty(self):
        return self.aktualna_ilosc <= 0.1

    def czy_pelny(self):
        return self.aktualna_ilosc >= self.pojemnosc - 0.1

    def rysujZbiornik(self, malarz):
        if self.poziom > 0:
            h = self.poziom * 147
            y = self.y + 150 - h
            malarz.setPen(Qt.NoPen)
            malarz.setBrush(self.kolor)
            malarz.drawRect(int(self.x + 1), int(y), 279, int(h))
        malarz.setPen(QPen(QColor(0, 0, 0), 3))
        malarz.setBrush(Qt.NoBrush)
        p = QPainterPath()
        p.moveTo(self.x, self.y)
        p.lineTo(self.x, self.y + 150)
        p.lineTo(self.x + 280, self.y + 150)
        p.lineTo(self.x + 280, self.y)
        malarz.drawPath(p)