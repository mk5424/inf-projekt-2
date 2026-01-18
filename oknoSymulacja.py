from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QLabel, QDialog, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen

from rury import Rura
from zbiornikBarwnik import zbiornikBarwnik
from zbiornikDuzy import zbiornikDuzy


class symulacja(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 800)
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)
        self.flow_speed = 0.8
        self.timer.start(20)

        self.btn1 = QPushButton("Zbiornik 1", self)
        self.btn1.setGeometry(50, 650, 100, 40)
        self.btn1.pressed.connect(lambda: self.zbiornikiBarwnik[0].otworz_zawor())
        self.btn1.released.connect(lambda: self.zbiornikiBarwnik[0].zamknij_zawor())

        self.btn2 = QPushButton("Zbiornik 2", self)
        self.btn2.setGeometry(170, 650, 100, 40)
        self.btn2.pressed.connect(lambda: self.zbiornikiBarwnik[1].otworz_zawor())
        self.btn2.released.connect(lambda: self.zbiornikiBarwnik[1].zamknij_zawor())

        self.btn3 = QPushButton("Zbiornik 3", self)
        self.btn3.setGeometry(290, 650, 100, 40)
        self.btn3.pressed.connect(lambda: self.zbiornikiBarwnik[2].otworz_zawor())
        self.btn3.released.connect(lambda: self.zbiornikiBarwnik[2].zamknij_zawor())

        self.btn1.setStyleSheet("background-color: rgb(255, 210, 210);")
        self.btn2.setStyleSheet("background-color: rgb(210, 255, 210);")
        self.btn3.setStyleSheet("background-color: rgb(210, 210, 255);")

        self.przelewa = [False, False, False]
        self.suwaki = []
        for i, x in enumerate([50, 170, 290]):
            slider = QSlider(Qt.Horizontal, self)
            slider.setGeometry(x, 700, 100, 20)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(80)
            self.suwaki.append(slider)

        self.labele = []
        for i, x in enumerate([280, 480, 680]):
            label = QLabel("80%", self)
            label.setGeometry(x, 256, 50, 20)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: rgb(180, 150, 180); border-radius: 10px;")
            self.labele.append(label)

        for i, slider in enumerate(self.suwaki):
            slider.valueChanged.connect(lambda val, idx=i: self.aktualizuj_label(idx, val))

        self.btn_doladuj = []
        for i, x in enumerate([50, 170, 290]):
            btn = QPushButton("+", self)
            btn.setGeometry(x, 750, 100, 30)
            btn.clicked.connect(lambda _, idx=i: self.doladuj_barwnik(idx))
            self.btn_doladuj.append(btn)

        self.btn_otworz_wszystkie = QPushButton("Otwórz wszystkie zawory", self)
        self.btn_otworz_wszystkie.setGeometry(450, 650, 200, 40)
        self.wszystkie_otwarte = False
        self.btn_otworz_wszystkie.clicked.connect(self.toggle_wszystkie_zawory)
        self.btn_otworz_wszystkie.setStyleSheet("background-color: rgb(220, 220, 220);")

        self.btn_wylej = QPushButton("Wylej i zapisz", self)
        self.btn_wylej.setGeometry(700, 650, 150, 40)
        self.btn_wylej.setStyleSheet("background-color: rgb(200,200,200);")
        self.btn_wylej.clicked.connect(self.wylej_i_zapisz)

        self.historia_duzego_zbiornika = []
        self.zbiornikDuzy = zbiornikDuzy(305, 450)
        self.zbiornikiBarwnik = [
            zbiornikBarwnik(200, 50, QColor(200, 50, 50)),
            zbiornikBarwnik(400, 50, QColor(50, 200, 50)),
            zbiornikBarwnik(600, 50, QColor(50, 50, 200))
        ]
        self.rury = [
            Rura([(self.zbiornikiBarwnik[0].ruraPrzylaczeX, self.zbiornikiBarwnik[0].ruraPrzylaczeY),
                  (self.zbiornikiBarwnik[0].ruraPrzylaczeX, self.zbiornikiBarwnik[0].ruraPrzylaczeY + 50),
                  (self.zbiornikiBarwnik[0].ruraPrzylaczeX + 130, self.zbiornikiBarwnik[0].ruraPrzylaczeY + 50),
                  (self.zbiornikiBarwnik[0].ruraPrzylaczeX + 130, self.zbiornikiBarwnik[0].ruraPrzylaczeY + 120),
                  (self.zbiornikiBarwnik[0].ruraPrzylaczeX + 130, self.zbiornikDuzy.y + 148 * (1 - self.zbiornikDuzy.poziom))],
                 QColor(200, 50, 50)),
            Rura([(self.zbiornikiBarwnik[1].ruraPrzylaczeX, self.zbiornikiBarwnik[1].ruraPrzylaczeY),
                  (self.zbiornikiBarwnik[1].ruraPrzylaczeX, self.zbiornikiBarwnik[1].ruraPrzylaczeY + 120),
                  (self.zbiornikiBarwnik[1].ruraPrzylaczeX, self.zbiornikDuzy.y + 148 * (1 - self.zbiornikDuzy.poziom))],
                 QColor(50, 200, 50)),
            Rura([(self.zbiornikiBarwnik[2].ruraPrzylaczeX, self.zbiornikiBarwnik[2].ruraPrzylaczeY),
                  (self.zbiornikiBarwnik[2].ruraPrzylaczeX, self.zbiornikiBarwnik[2].ruraPrzylaczeY + 50),
                  (self.zbiornikiBarwnik[2].ruraPrzylaczeX - 130, self.zbiornikiBarwnik[2].ruraPrzylaczeY + 50),
                  (self.zbiornikiBarwnik[2].ruraPrzylaczeX - 130, self.zbiornikiBarwnik[2].ruraPrzylaczeY + 120),
                  (self.zbiornikiBarwnik[2].ruraPrzylaczeX - 130, self.zbiornikDuzy.y + 148 * (1 - self.zbiornikDuzy.poziom))],
                 QColor(50, 50, 200)),
        ]

    def ustaw_przelew(self, idx, stan):
        self.przelewa[idx] = stan

    def logika_przeplywu(self):
        for i in range(3):
            zb = self.zbiornikiBarwnik[i]
            przeplyw = self.suwaki[i].value() / 100.0
            if self.przelewa[i] or zb.zawor_otwarty:
                ilosc = zb.usun_ciecz(przeplyw)
                if ilosc > 0:
                    self.zbiornikDuzy.dodaj_ciecz(ilosc, zb.kolor)
                    self.rury[i].ustaw_przeplyw(True)
                else:
                    self.rury[i].ustaw_przeplyw(False)
            else:
                self.rury[i].ustaw_przeplyw(False)
        self.update()

    def aktualizuj_label(self, idx, val):
        self.labele[idx].setText(f"{val}%")

    def paintEvent(self, event):
        malarz = QPainter(self)
        malarz.setRenderHint(QPainter.Antialiasing)
        for x in self.zbiornikiBarwnik:
            x.rysujZbiornik(malarz)
        for x in self.rury:
            x.draw(malarz)
        self.zbiornikDuzy.rysujZbiornik(malarz)

    def doladuj_barwnik(self, idx):
        zbiornik = self.zbiornikiBarwnik[idx]
        brak = zbiornik.pojemnosc - zbiornik.aktualna_ilosc
        if brak > 0:
            zbiornik.dodaj_ciecz(brak)
        self.update()

    def otworz_wszystkie_zawory(self):
        for zb in self.zbiornikiBarwnik:
            zb.otworz_zawor()

    def zamknij_wszystkie_zawory(self):
        for zb in self.zbiornikiBarwnik:
            zb.zamknij_zawor()

    def wylej_i_zapisz(self):
        zb = self.zbiornikDuzy
        stan = {
            "data": "2026-01-18 12:58:01",
            "ilosc": zb.aktualna_ilosc / zb.pojemnosc,
            "kolor": {"r": int(zb.ilosc_r), "g": int(zb.ilosc_g), "b": int(zb.ilosc_b)}
        }
        self.historia_duzego_zbiornika.append(stan)
        zb.aktualna_ilosc = 0
        zb.ilosc_r = zb.ilosc_g = zb.ilosc_b = 0
        zb.aktualizuj_poziom()
        zb.aktualizuj_kolor()
        self.update()
        self.pokaz_raport()

    def pokaz_raport(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Raport dużego zbiornika")
        dialog.resize(400, 300)
        layout = QVBoxLayout()
        for stan in self.historia_duzego_zbiornika:
            tekst = f"Data: {stan['data']} | Ilość: {int(stan['ilosc']*100)}%"
            label = QLabel(tekst)
            kolor = stan["kolor"]
            label.setStyleSheet(f"background-color: rgb({kolor['r']},{kolor['g']},{kolor['b']}); padding: 5px;")
            layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec_()

    def toggle_wszystkie_zawory(self):
        if not self.wszystkie_otwarte:
            for zb in self.zbiornikiBarwnik:
                zb.otworz_zawor()
            self.wszystkie_otwarte = True
            self.btn_otworz_wszystkie.setText("Zamknij wszystkie zawory")
        else:
            for zb in self.zbiornikiBarwnik:
                zb.zamknij_zawor()
            self.wszystkie_otwarte = False
            self.btn_otworz_wszystkie.setText("Otwórz wszystkie zawory")