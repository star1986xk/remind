# -*-coding: UTF-8 -*-
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QFrame, QMenu, QSystemTrayIcon
from UI.ui_main import Ui_Form
from PyQt5 import QtGui, QtWidgets
import time
from mylogclass import MyLogClass


class MainWindow(QFrame, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)
        self.retranslateUi(self)

        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint)  # 窗口无边框，置前

        # 设置托盘
        self.trayIcon = QSystemTrayIcon(self)  # 创建托盘对象
        self.trayIcon.setToolTip('学习提醒工具')  # 设置托盘提示信息
        self.icon = QtGui.QIcon(":/newPrefix/title.ico")  # 定义一个图标
        self.trayIcon.setIcon(self.icon)  # 设置托盘图标
        self.trayIcon.activated.connect(self.trayClick)  # 点击托盘信号
        self.createMenu()  # 创建托盘右键菜单
        self.trayIcon.show()  # 显示托盘

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_run.clicked.connect(self.run)
        self.pushButton_1.clicked.connect(self.click)
        self.pushButton_2.clicked.connect(self.click)
        self.pushButton_3.clicked.connect(self.click)

        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.time)

    def click(self):
        self.setVisible(False)
        self.mylog.logger.info(self.sender().objectName()[-1])
        self.open()

    def createMenu(self):
        self.menu = QMenu()  # 创建菜单对象
        self.showAction1 = QtWidgets.QAction("显示", self, triggered=self.show_window)  # 创建菜单按钮
        self.showAction2 = QtWidgets.QAction("信息", self, triggered=self.showMsg)
        self.quitAction = QtWidgets.QAction("退出", self, triggered=self.close)

        self.menu.addAction(self.showAction1)  # 添加按钮
        self.menu.addAction(self.showAction2)
        self.menu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.menu)  # 设置托盘菜单

    def show_window(self):
        self.showNormal()

    def showMsg(self):
        self.trayIcon.showMessage('软件信息', '学习提醒工具', self.icon)

    def trayClick(self, reason):
        '''
        鼠标点击托盘图标的信号，返回一个整数参数
        :param reason: 1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        :return:
        '''
        if reason == 2 or reason == 3:
            if self.isMinimized() or not self.isVisible():
                # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.showNormal()
            else:
                self.setVisible(False)

    def run(self):
        self.setVisible(False)
        self.stackedWidget.setCurrentIndex(1)
        self.mylog = MyLogClass()
        self.mylog.logger.info('开始')
        self.open()

    def open(self):
        self.timer.start(1000 * 60 * 2)

    def time(self):
        self.timer.stop()
        self.showNormal()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '警告', '你确定要退出软件吗？',
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def getQss():
    with open('./UI/style.qss', 'r', encoding='utf8') as f:
        qss = f.read()
    return qss


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.setStyleSheet(getQss())
    win.show()
    sys.exit(app.exec_())
