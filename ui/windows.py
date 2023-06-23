from datetime import datetime
from typing import NamedTuple

from PyQt5.QtWidgets import QLabel, QSizePolicy

from client.client_utils.client_router import RouterMixin
from client.client_utils.utils import current_user
from ui.ui_utils.controller import context
from ui.main_window import Ui_MainWindow as main_window_ui
from ui.login import Ui_LoginWindow as login_ui
from ui.register import Ui_RegisterWindow as register_ui
from ui.chat_window import Ui_ChatWindow as chat_ui
from ui.add_contact_window import Ui_AddContactWindow as add_contact_ui
from PyQt5 import QtWidgets, QtCore, QtGui


class Msg(NamedTuple):
    username: str
    message: str
    time: datetime


class AddContactModalWindow(QtWidgets.QMainWindow, RouterMixin):
    def __init__(self):
        super().__init__()
        self.ui = add_contact_ui()
        self.parent_context = context.context_ui
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.ui.ok_btn.clicked.connect(self.add_user_contact)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.enter_name_edit.textEdited.connect(self.validate_inputs)

    def validate_inputs(self):
        if self.ui.enter_name_edit.text():
            self.ui.ok_btn.setEnabled(True)
        else:
            self.ui.ok_btn.setDisabled(True)

    def add_user_contact(self):
        contact_username = self.ui.enter_name_edit.text()
        self.add_contact(contact_username)

    def add_contact_failed(self, error):
        self.ui.extra_label.setText(error)
        self.ui.extra_label.setStyleSheet("color: red")
        self.ui.extra_label.show()

    def contact_added(self):
        self.ui.extra_label.setText("Contact added!")
        self.ui.extra_label.setStyleSheet("color: green")
        self.ui.extra_label.show()

    def cancel(self):
        self.close()

    def closeEvent(self, event):
        context.context_ui = self.parent_context


class ChatWindow(QtWidgets.QMainWindow, RouterMixin):
    def __init__(self):
        super().__init__()
        self.ui = chat_ui()
        self.opened_chat = None
        self.ui.setupUi(self)
        self.ui.add_contact_btn.clicked.connect(self.add_contact_slot)
        self.ui.send_msg_btn.setDisabled(True)
        self.ui.send_msg_edit.setDisabled(True)

    @staticmethod
    def add_contact_slot():
        cui = AddContactModalWindow()
        context.context_ui = cui
        cui.show()

    def get_contacts_list(self):
        self.get_contacts()

    def get_contacts_result(self, contacts):
        for user in contacts:
            online_status = "Online" if user.online_status else "Offline"
            contact = QtWidgets.QListWidgetItem(self.ui.listWidget)
            contact.setText(f"{user.first_name} {user.last_name} {online_status}")
            contact.username = user.username
            contact.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            contact.setBackground(QtGui.QColor("#c9f6ff"))
            self.ui.listWidget.addItem(contact)
        self.ui.listWidget.itemClicked.connect(self.open_chat_by_item)

    def open_chat_by_item(self, contact):
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            item.setBackground(QtGui.QColor("#c9f6ff"))
        self.opened_chat = contact
        self.ui.send_msg_btn.disconnect()
        self.prepare_chat()
        contact.setBackground(QtGui.QColor("grey"))
        self.ui.send_msg_edit.setEnabled(True)
        self.ui.send_msg_btn.setEnabled(True)
        self.get_messages(contact)
        self.ui.send_msg_btn.clicked.connect(lambda: self.handle_send_msg(contact))

    def prepare_chat(self):
        self.ui.msg_list.clear()
        self.ui.send_msg_edit.clear()

    def handle_send_msg(self, contact):
        msg = self.ui.send_msg_edit.toPlainText()
        self.ui.send_msg_edit.clear()
        if msg:
            self.send_msg(msg, contact)

    def get_messages_result(self, messages):
        for message in messages:
            msg = Msg(username=message.user.username, message=message.message, time=message.time)
            self.add_message(msg)

    def get_message(self, msg):
        if self.opened_chat and (msg.username == self.opened_chat.username or msg.send_to == self.opened_chat.username):
            msg = Msg(username=msg.username, message=msg.message, time=msg.send_time)
            self.add_message(msg)

    def add_message(self, msg):
        self.create_list_item(msg)

    def create_list_item(self, msg):
        widget = QtWidgets.QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)

        win = self.create_widget(widget, msg)
        widget.setLayout(win)

        item = QtWidgets.QListWidgetItem(self.ui.msg_list)
        item.setSizeHint(widget.sizeHint())

        if msg.username == current_user.username:
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.ui.msg_list.addItem(item)
        self.ui.msg_list.setItemWidget(item, widget)
        self.ui.msg_list.scrollToBottom()

    def create_widget(self, widget, msg):
        verticalLayout_2 = QtWidgets.QVBoxLayout(widget)
        verticalLayout_2.setObjectName(u"verticalLayout_2")
        frame = QtWidgets.QFrame(widget)
        frame.setObjectName(u"frame")
        frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        verticalLayout = QtWidgets.QVBoxLayout(frame)
        verticalLayout.setObjectName(u"verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(frame)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.adjustSize()
        self.plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.plainTextEdit.setUndoRedoEnabled(False)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setMinimumWidth(380)
        self.plainTextEdit.setMaximumHeight(16777215)
        frame.setMaximumHeight(16777215)
        widget.setMaximumHeight(16777215)

        # hardcode
        self.plainTextEdit.setFixedHeight(500)
        one_line_height = 17
        chars_by_one_line = 46
        calculated_height = one_line_height * (len(msg.message) // chars_by_one_line)
        self.plainTextEdit.setFixedHeight(calculated_height if calculated_height > 22 else 23)

        verticalLayout.addWidget(self.plainTextEdit)
        time_label = QLabel(frame)
        time_label.setObjectName(u"label")
        time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight |
                           QtCore.Qt.AlignmentFlag.AlignTrailing |
                           QtCore.Qt.AlignmentFlag.AlignVCenter)
        verticalLayout.addWidget(time_label)

        if msg.username == current_user.username:
            verticalLayout_2.addWidget(frame, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        else:
            verticalLayout_2.addWidget(frame, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        time_label.setText(str(msg.time))

        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        frame.setContentsMargins(0, 0, 0, 0)
        style = """
        * {
        background: #{SENDER};
        }
        QLabel, #frame {
        background: #{SENDER};
        }
        QPlainTextEdit{
        background: #{SENDER};
        font: 10pt;
        }
        #verticalLayout_2 {
        border: none;
        }
        #frame {
        border: 0px solid {COLOR};
        border-radius: 10px;
        padding: 10px;
        }"""

        if msg.username == current_user.username:
            style = style.replace("{COLOR}", "#DADEE5").replace("{SENDER}", "EFFDDE")
            time_label.setStyleSheet("color: #7D9FAB;")
        else:
            style = style.replace("{COLOR}", "#182533").replace("{SENDER}", "f0f0f0")
            time_label.setStyleSheet("color: #4A768F;")

        frame.setStyleSheet(style)
        self.plainTextEdit.insertPlainText(msg.message.strip())

        self.plainTextEdit.setStyleSheet("""
            border: none;
        """)
        return verticalLayout_2


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window_ui()
        context.context_ui = self
        self.lui = LoginWindow()
        self.rui = RegisterWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.on_login_btn_pressed)
        self.ui.pushButton_2.clicked.connect(self.on_register_btn_pressed)

    def on_login_btn_pressed(self):
        self.close()
        context.context_ui = self.lui
        self.lui.show()

    def on_register_btn_pressed(self):
        self.close()
        context.context_ui = self.rui
        self.rui.show()


class LoginWindow(QtWidgets.QMainWindow, RouterMixin):
    def __init__(self):
        super().__init__()
        self.ui = login_ui()
        self.cui = ChatWindow()
        self.ui.setupUi(self)
        self.ui.loginEdit.textEdited.connect(self.validate_inputs)
        self.ui.passEdit.textEdited.connect(self.validate_inputs)
        self.ui.loginButton.clicked.connect(self.check_login)

    def validate_inputs(self):
        if self.ui.loginEdit.text() and self.ui.passEdit.text():
            self.ui.loginButton.setEnabled(True)
        else:
            self.ui.loginButton.setDisabled(True)

    def check_login(self):
        login = self.ui.loginEdit.text()
        password = self.ui.passEdit.text()
        self.login(login, password)

    def login_done(self):
        self.close()
        context.context_ui = self.cui
        self.cui.get_contacts_list()
        self.cui.show()

    def invalid_login(self):
        self.ui.error_label.setText("Incorrect login or password")
        self.ui.error_label.show()
        self.ui.loginEdit.clear()
        self.ui.loginButton.setDisabled(True)
        self.ui.passEdit.clear()


class RegisterWindow(QtWidgets.QMainWindow, RouterMixin):
    def __init__(self):
        super().__init__()
        self.ui = register_ui()
        self.ui.setupUi(self)
        self.inputs = self.ui.loginEdit, self.ui.passEdit, self.ui.firstNameEdit,  self.ui.lastNameEdit
        for input_ in self.inputs:
            input_.textEdited.connect(self.validate_inputs)
        self.ui.register_btn.clicked.connect(self.register_user)

    def validate_inputs(self):
        line_edits = self.ui.loginEdit, self.ui.passEdit, self.ui.firstNameEdit, self.ui.lastNameEdit
        if all(line_edit.text() for line_edit in line_edits):
            self.ui.register_btn.setEnabled(True)
        else:
            self.ui.register_btn.setDisabled(True)

    def register_user(self):
        username = self.ui.loginEdit.text()
        password = self.ui.passEdit.text()
        first_name = self.ui.firstNameEdit.text()
        last_name = self.ui.lastNameEdit.text()
        user_data = dict(username=username,
                         password=password,
                         first_name=first_name,
                         last_name=last_name)
        self.register(user_data)

    def register_done(self):
        self.ui.extra_label.setStyleSheet("color: green")
        self.ui.extra_label.setText("Registration done successfully")
        self.ui.extra_label.show()
        self.register_done_timer = QtCore.QTimer()
        self.register_done_timer.timeout.connect(self.register_done_timer_slot)
        self.register_done_timer.start(2000)

    def register_failed(self, error):
        self.ui.extra_label.setText(error)
        self.ui.register_btn.setDisabled(True)
        self.ui.extra_label.setStyleSheet("color: red")
        self.ui.extra_label.show()
        for input_ in self.inputs:
            input_.clear()
        self.register_failed_timer = QtCore.QTimer()
        self.register_failed_timer.timeout.connect(self.register_failed_timer_slot)
        self.register_failed_timer.start(2000)

    def register_done_timer_slot(self):
        self.register_done_timer.stop()
        lui = LoginWindow()
        context.context_ui = lui
        self.close()
        lui.show()

    def register_failed_timer_slot(self):
        self.ui.extra_label.hide()
        self.register_failed_timer.stop()
