import io
import sys
import sqlite3
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QMainWindow

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>515</width>
    <height>329</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QComboBox" name="parameterSelection">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>131</width>
      <height>22</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="queryButton">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>50</y>
      <width>81</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Пуск</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>150</x>
      <y>10</y>
      <width>351</width>
      <height>281</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>515</width>
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
        self.initUi()
        self.add_items()
    
    def initUi(self):
        self.queryButton.clicked.connect(self.request)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Название фильма", "Жанр", "Год"])

    def request(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('films_db.sqlite')
        db.open()
        
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        selected_genre = self.parameterSelection.currentText()
        query = QSqlQuery(f"""
            SELECT f.title, g.title, f.year
            FROM films f
            JOIN genres g ON f.genre = g.id
            WHERE g.title = '{selected_genre}'
            ORDER BY f.title ASC
        """)
        
        row = 0
        while query.next():
            self.tableWidget.insertRow(row)
            
            title_item = QTableWidgetItem(query.value(0))
            genre_item = QTableWidgetItem(query.value(1))
            year_item = QTableWidgetItem(str(query.value(2)))
            
            self.tableWidget.setItem(row, 0, title_item)
            self.tableWidget.setItem(row, 1, genre_item)
            self.tableWidget.setItem(row, 2, year_item)
            
            row += 1
        db.close()

    def add_items(self):
        db = "films_db.sqlite"
        connect = sqlite3.connect(db)
        cursor = connect.cursor()

        result = cursor.execute("SELECT title FROM genres")

        for elem in result:
            self.parameterSelection.addItem(*elem)
        cursor.close()
        connect.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())