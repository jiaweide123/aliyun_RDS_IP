#!/usr/bin/env python
# # coding=utf-8
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QDesktopWidget,QFormLayout,QLineEdit,QMessageBox,QComboBox
import sys
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import ModifySecurityIpsRequest
import requests

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.data = []
        f = open('./1.json', 'r',encoding='utf-8')
        self.data = eval(f.read())
        self.initUi(self.data)

    def initUi(self,data):
        items = []
        for k in data:
            items.append(k['name'])
        self.setWindowTitle('阿里云RDS设置IP白名单')
        self.resize(500,500)
        self.center()
        layout = QFormLayout()

        self.combobox = QComboBox()
        self.combobox.addItem('请选择')
        self.combobox.addItems(items)
        self.combobox.currentIndexChanged[int].connect(self.selectionchange)
        layout.addRow('选项',self.combobox)

        self.IP = QLineEdit()
        layout.addRow('IP', self.IP)
        try:
            self.IP.setText(str(self.get_ip()))

        except:
            self.IP.setPlaceholderText('ip获取失败，请手动输入！！！')

        self.name = QLineEdit()
        layout.addRow('name', self.name)
        self.name.setPlaceholderText('imput name')

        self.AccessKey = QLineEdit()
        layout.addRow('AccessKey',self.AccessKey)
        self.AccessKey.setPlaceholderText('imput AccessKey')


        self.AccessSecret = QLineEdit()
        layout.addRow('AccessSecret',self.AccessSecret)
        self.AccessSecret.setPlaceholderText('imput AccessSecret')


        self.RegionId = QLineEdit()
        layout.addRow('RegionId', self.RegionId)
        self.RegionId.setPlaceholderText('imput RegionId')


        self.dbInstanceId = QLineEdit()
        layout.addRow('dbInstanceId', self.dbInstanceId)
        self.dbInstanceId.setPlaceholderText('imput dbInstanceId')


        self.dbInstanceIPArrayName = QLineEdit()
        layout.addRow('dbInstanceIPArrayName', self.dbInstanceIPArrayName)
        self.dbInstanceIPArrayName.setPlaceholderText('imput dbInstanceIPArrayName')


        self.bt1 = QPushButton('提交')
        layout.addWidget(self.bt1)
        self.bt1.clicked.connect(self.clicked_bt1)

        self.setLayout(layout)
        self.show()

    def selectionchange(self,i):
        if i ==0:
            self.name.setText('')
            self.AccessKey.setText('')
            self.AccessSecret.setText('')
            self.RegionId.setText('')
            self.dbInstanceId.setText('')
            self.dbInstanceIPArrayName.setText('')
        else:
            data = self.data[i-1]
            self.name.setText(data['name'])
            self.AccessKey.setText(data['AccessKey'])
            self.AccessSecret.setText(data['AccessSecret'])
            self.RegionId.setText(data['RegionId'])
            self.dbInstanceId.setText(data['dbInstanceId'])
            self.dbInstanceIPArrayName.setText(data['dbInstanceIPArrayName'])


    def get_ip(self):
        r = requests.post(url='http://ip-api.com/json/?lang=zh-CN ')
        return r.json()['query']

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newleft = (screen.width()-size.width())/2
        newright = (screen.height()-size.height())/2
        self.move(int(newleft),int(newright))

    def clicked_bt1(self):
        name = self.name.text()
        AccessKey = self.AccessKey.text()
        AccessSecret =self.AccessSecret.text()
        RegionId = self.RegionId.text()
        dbInstanceId = self.dbInstanceId.text()
        dbInstanceIPArrayName = self.dbInstanceIPArrayName.text()
        ip = self.IP.text()
        if AccessKey == '' or AccessSecret == '' or RegionId == '' or dbInstanceId == '' or dbInstanceIPArrayName == '' or ip == '':
            QMessageBox.information(self, '提示', '仔细检查检查，是不是哪里没有填！！！')
        else:
            dbInstanceIPArrayAttribute = ''
            ali = Alis(AccessKey, AccessSecret, RegionId)  # 阿里云后台创建
            clt = ali.client()
            req = ali.modifySecurityIpsRequest(dbInstanceId, ip,
                dbInstanceIPArrayName, dbInstanceIPArrayAttribute)
            try:
                clt.do_action_with_exception(req)
                QMessageBox.information(self, '提示', '%s修改ip地址白名单成功!' % name)
            except:
                QMessageBox.information(self, '提示', '修改白名单ip失败，请检查你输入的内容对不对！！！')



class Alis():
    def __init__(self, AccessKey, AccessSecret, RegionId):
        self.AccessKey = AccessKey
        self.AccessSecret = AccessSecret
        self.RegionId = RegionId


    def client(self):
        c = client.AcsClient(self.AccessKey, self.AccessSecret, self.RegionId)
        return c

    #设置ip白名单
    def modifySecurityIpsRequest(self, DBInstanceId, SecurityIps, DBInstanceIPArrayName, DBInstanceIPArrayAttribute):
        """修改数据库实例白名单
        """
        request = ModifySecurityIpsRequest.ModifySecurityIpsRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_SecurityIps(SecurityIps)
        request.set_DBInstanceIPArrayName(DBInstanceIPArrayName)
        request.set_DBInstanceIPArrayAttribute(DBInstanceIPArrayAttribute)
        request.set_WhitelistNetworkType('Classic')

        return request



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Demo()
    sys.exit(app.exec_())