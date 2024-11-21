import io
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MyWidget</class>
 <widget class="QMainWindow" name="MyWidget">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>756</width>
    <height>318</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="queryButton">
    <property name="geometry">
     <rect>
      <x>670</x>
      <y>20</y>
      <width>81</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>Поиск</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="queryLine">
    <property name="geometry">
     <rect>
      <x>250</x>
      <y>19</y>
      <width>411</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QComboBox" name="parameterSelection">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>20</y>
      <width>221</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <stylestrategy>PreferDefault</stylestrategy>
     </font>
    </property>
    <item>
     <property name="text">
      <string>Год выпуска</string>
     </property>
    </item>
    <item>
     <property name="text">
      <string>Название</string>
     </property>
    </item>
    <item>
     <property name="text">
      <string>Продолжительность</string>
     </property>
    </item>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>70</y>
      <width>47</width>
      <height>13</height>
     </rect>
    </property>
    <property name="text">
     <string>ID:</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>110</y>
      <width>61</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Название:</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>150</y>
      <width>81</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Год выпуска:</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_4">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>190</y>
      <width>47</width>
      <height>13</height>
     </rect>
    </property>
    <property name="text">
     <string>Жанр:</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_5">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>230</y>
      <width>121</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Продолжительность:</string>
    </property>
   </widget>
   <widget class="QLabel" name="errorLabel">
    <property name="enabled">
     <bool>true</bool>
    </property>
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>250</y>
      <width>131</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Ничего не найдено</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="idEdit">
    <property name="geometry">
     <rect>
      <x>250</x>
      <y>60</y>
      <width>411</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="titleEdit">
    <property name="geometry">
     <rect>
      <x>250</x>
      <y>100</y>
      <width>411</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="yearEdit">
    <property name="geometry">
     <rect>
      <x>250</x>
      <y>140</y>
      <width>411</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="genreEdit">
    <property name="geometry">
     <rect>
      <x>250</x>
      <y>180</y>
      <width>411</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="durationEdit">
    <property name="geometry">
     <rect>
      <x>250</x>
      <y>220</y>
      <width>411</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>756</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.initUI()

    def initUI(self):
        self.queryButton.clicked.connect(self.search)
        self.errorLabel.hide()
        self.num = 0

    def search(self):
        menu_text = self.parameterSelection.currentText()
        input_text = self.queryLine.text()

        if menu_text == "Год выпуска":
            menu_text = "year"
        elif menu_text == "Название":
            menu_text = "title"
        elif menu_text == "Продолжительность":
            menu_text = "duration"

        if not input_text:
            self.errorLabel.setText("Неправильный запрос")
            self.errorLabel.show()
        else:
            self.errorLabel.hide()

        db = QSqlDatabase.addDatabase("QSQLITE", str(self.num))
        db.setDatabaseName("films_db.sqlite")
        db.open()

        query = QSqlQuery(db)
        result = f"SELECT * FROM films WHERE {menu_text} LIKE '{input_text}' ORDER BY id ASC LIMIT 1"
        query.exec(result)

        if query.next():
            self.idEdit.setText(str(query.value(0)))
            self.titleEdit.setText(str(query.value(1)))
            self.yearEdit.setText(str(query.value(2)))
            self.genreEdit.setText(str(query.value(3)))
            self.durationEdit.setText(str(query.value(4)))

            self.errorLabel.clear()
        else:
            self.idEdit.clear()
            self.titleEdit.clear()
            self.yearEdit.clear()
            self.genreEdit.clear()
            self.durationEdit.clear()
            self.errorLabel.setText("Ничего не найдено")
            if not input_text:
                self.errorLabel.setText("Неправильный запрос")
            self.errorLabel.show()
        self.num += 1
        db.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())