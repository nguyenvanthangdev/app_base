from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QLineEdit, QMessageBox, QTableWidget, QHBoxLayout,
    QGroupBox, QTableWidgetItem, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt
from app.services.user_service import get_all_users, add_user, delete_user, update_user
from app.gui.widgets.ui.button import Button , ButtonVariant, ButtonSize
from app.gui.widgets.ui.input import Input ,InputSize,InputVariant


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard - Quản lý người dùng")
        self.setFixedSize(700, 500)

        self.user_count_label = QLabel("Tổng số người dùng: 0")
        self.refresh_button =  Button("Thêm người dùng",size=ButtonSize.SM)

        self.name_input = Input(size=InputSize.SM,variant=InputVariant.DEFAULT)
        self.name_input.setPlaceholderText("Tên")
        self.email_input = Input(size=InputSize.SM,variant=InputVariant.DEFAULT)
        self.email_input.setPlaceholderText("Email")
        self.add_button = Button("Thêm người dùng",size=ButtonSize.SM)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Tên", "Email", "Hành động"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 250)
        
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.user_count_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.refresh_button)

        table_group = QGroupBox("Danh sách người dùng")
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(stats_layout)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(table_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.refresh_button.clicked.connect(self.load_users)
        self.add_button.clicked.connect(self.add_user)

        self.load_users()

    def load_users(self):
        users = get_all_users()
        self.table.setRowCount(len(users))
        self.user_count_label.setText(f"Tổng số người dùng: {len(users)}")

        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.table.setItem(row, 1, QTableWidgetItem(user.name))
            self.table.setItem(row, 2, QTableWidgetItem(user.email))

            delete_btn = Button("Xoá",size=ButtonSize.SM,variant=ButtonVariant.DESTRUCTIVE)
            delete_btn.clicked.connect(lambda _, uid=user.id: self.delete_user(uid))

            edit_btn = Button("Sửa",size=ButtonSize.SM,variant=ButtonVariant.OUTLINE)
            edit_btn.clicked.connect(lambda _, uid=user.id, uname=user.name, uemail=user.email: self.show_edit_dialog(uid, uname, uemail))

            btn_layout = QHBoxLayout()
            btn_widget = QWidget()
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_widget.setLayout(btn_layout)

            self.table.setCellWidget(row, 3, btn_widget)

    def add_user(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        if not name or not email:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên và email")
            return
        user = add_user(name, email)
        QMessageBox.information(self, "Thành công", f"Đã thêm: {user.name}")
        self.name_input.clear()
        self.email_input.clear()
        self.load_users()

    def delete_user(self, user_id):
        delete_user(user_id)
        self.load_users()

    def show_edit_dialog(self, user_id, name, email):
        dialog = QDialog(self)
        dialog.setWindowTitle("Sửa người dùng")

        name_input = QLineEdit()
        name_input.setText(name)
        email_input = QLineEdit()
        email_input.setText(email)

        save_button = Button("Lưu",size=ButtonSize.SM,variant=ButtonVariant.DEFAULT)
        cancel_button = Button("Huỷ",size=ButtonSize.SM,variant=ButtonVariant.OUTLINE)

        layout = QFormLayout()
        layout.addRow("Tên:", name_input)
        layout.addRow("Email:", email_input)
        layout.addRow(save_button, cancel_button)
        dialog.setLayout(layout)

        def save_changes():
            new_name = name_input.text().strip()
            new_email = email_input.text().strip()
            if not new_name or not new_email:
                QMessageBox.warning(dialog, "Lỗi", "Không được để trống")
                return
            update_user(user_id, new_name, new_email)
            dialog.accept()
            self.load_users()

        save_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec()
