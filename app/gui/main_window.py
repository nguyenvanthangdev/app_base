from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QLineEdit, QMessageBox, QTableWidget, QHBoxLayout,
    QGroupBox, QTableWidgetItem, QDialog, QFormLayout,
    QFrame, QSpacerItem, QSizePolicy, QCheckBox, QHeaderView
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QColor
from app.services.user_service import get_all_users, add_user, delete_user, update_user
from app.gui.widgets.ui.button import Button, ButtonVariant, ButtonSize
from app.gui.widgets.ui.input import Input, InputSize, InputVariant
from app.gui.widgets.ui.label import Label, LabelSize, LabelVariant
from app.gui.widgets.ui.table import Table, TableVariant, TableSize


class MainWindow(QMainWindow):
    """
    Main window class for the User Management System.
    Handles the main UI layout and user interactions.
    """
    def __init__(self):
        super().__init__()
        self._setup_window_properties()
        self._setup_styles()
        self._create_ui_components()
        self._setup_layout()
        self._connect_signals()
        self.load_users()

    def _setup_window_properties(self):
        """Initialize basic window properties"""
        self.setWindowTitle("User Management System")
        self.setMinimumSize(900, 600)

    def _setup_styles(self):
        """Setup the application stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                margin-top: 1em;
                padding: 15px;
            }
            QGroupBox::title {
                color: #333;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #e0e0e0;
            }
            QLabel {
                color: #333;
            }
        """)

    def _create_ui_components(self):
        """Create all UI components"""
        # Header components
        self.header = self._create_header()
        
        # Form components
        self.form_group = self._create_form_group()
        
        # Table components
        self.table_group = self._create_table_group()

    def _create_header(self):
        """Create the header section with title and user count"""
        header = QWidget()
        header.setStyleSheet("background-color: white; border-bottom: 1px solid #e0e0e0;")
        header_layout = QHBoxLayout(header)
        
        title_label = Label("User Management",size=LabelSize.XXL,variant=LabelVariant.DARK,bold=True)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.user_count_label = Label("Total Users: 0",size=LabelSize.SM,variant=LabelVariant.MUTED)
        header_layout.addWidget(self.user_count_label)
        
        return header

    def _create_form_group(self):
        """Create the form section for adding new users"""
        form_group = QGroupBox("Add New User")
        form_layout = QHBoxLayout()
        
        self.name_input = Input(placeholder="Enter name",size=InputSize.SM, variant=InputVariant.DEFAULT)
        self.name_input.setMinimumWidth(200)
        
        self.email_input = Input(placeholder="Enter email", size=InputSize.SM, variant=InputVariant.OUTLINE)
        self.email_input.setMinimumWidth(250)
        
        self.add_button = Button("Add User", size=ButtonSize.SM, variant= ButtonVariant.SUCCESS)
        self.add_button.setMinimumWidth(120)
        
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.add_button)
        form_layout.addStretch()
        form_group.setLayout(form_layout)
        
        return form_group

    def _create_table_group(self):
        """Create the table section for displaying users"""
        table_group = QGroupBox("User List")
        table_layout = QVBoxLayout()
        
        # Add action buttons for bulk operations
        action_buttons = QHBoxLayout()
        self.edit_selected_btn = Button("Edit Selected", size=ButtonSize.SM, variant=ButtonVariant.OUTLINE)
        self.delete_selected_btn = Button("Delete Selected", size=ButtonSize.SM, variant=ButtonVariant.DESTRUCTIVE)
        action_buttons.addWidget(self.edit_selected_btn)
        action_buttons.addWidget(self.delete_selected_btn)
        action_buttons.addStretch()
        table_layout.addLayout(action_buttons)
        
        # Create table with custom component
        self.table = Table(
            variant=TableVariant.DEFAULT,
            size=TableSize.DEFAULT,
            show_checkbox=True,
            row_height=50
        )
        
        # Set headers
        self.table.set_headers(["Select", "ID", "Name", "Email"])
        
        # Set column widths
        self.table.setColumnWidth(0, 50)  # Checkbox column
        self.table.setColumnWidth(1, 60)  # ID column
        self.table.setColumnWidth(2, 200)  # Name column
        self.table.setColumnWidth(3, 300)  # Email column
        
        # Set header to stretch
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        # Connect checkbox signal
        self.table.checkbox_changed.connect(self._handle_row_highlight)
        
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        
        return table_group

    def _setup_layout(self):
        """Setup the main layout of the window"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.form_group)
        main_layout.addWidget(self.table_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _connect_signals(self):
        """Connect all button signals to their respective slots"""
        self.add_button.clicked.connect(self.add_user)
        self.edit_selected_btn.clicked.connect(self.edit_selected_users)
        self.delete_selected_btn.clicked.connect(self.delete_selected_users)

    def load_users(self):
        """Load and display all users in the table"""
        users = get_all_users()
        self.table.setRowCount(0)  # Clear existing rows
        self.user_count_label.setText(f"Total Users: {len(users)}")

        for user in users:
            self.table.add_row([user.id, user.name, user.email])

    def _handle_row_highlight(self, row, checked):
        """Handle row highlighting when checkbox state changes"""
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                item.setBackground(QColor("#e3f2fd" if checked else "white"))

    def show_edit_dialog(self, user_id, name, email):
        """Show dialog for editing user information"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User")
        dialog.setMinimumWidth(400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        name_input = QLineEdit()
        name_input.setText(name)
        name_input.setPlaceholderText("Enter name")
        
        email_input = QLineEdit()
        email_input.setText(email)
        email_input.setPlaceholderText("Enter email")

        form_layout.addRow("Name:", name_input)
        form_layout.addRow("Email:", email_input)
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = Button("Save", size=ButtonSize.SM)
        cancel_button = Button("Cancel", size=ButtonSize.SM, variant=ButtonVariant.OUTLINE)
        
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        def save_changes():
            new_name = name_input.text().strip()
            new_email = email_input.text().strip()
            if not new_name or not new_email:
                QMessageBox.warning(dialog, "Error", "Please fill in all fields")
                return
            update_user(user_id, new_name, new_email)
            dialog.accept()
            self.load_users()

        save_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec()

    def add_user(self):
        """Add a new user to the system"""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        if not name or not email:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        user = add_user(name, email)
        QMessageBox.information(self, "Success", f"Added user: {user.name}")
        self.name_input.clear()
        self.email_input.clear()
        self.load_users()

    def delete_user(self, user_id):
        """Delete a user from the system"""
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this user?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            delete_user(user_id)
            self.load_users()

    def get_selected_users(self):
        """Get list of selected user IDs"""
        selected_rows = self.table.get_selected_rows()
        selected_users = []
        for row in selected_rows:
            user_id = int(self.table.item(row, 1).text())
            selected_users.append(user_id)
        return selected_users

    def edit_selected_users(self):
        """Edit the selected user"""
        selected_users = self.get_selected_users()
        if not selected_users:
            QMessageBox.warning(self, "Warning", "Please select a user to edit")
            return
        
        if len(selected_users) > 1:
            QMessageBox.warning(self, "Warning", "Please select only one user to edit")
            return
            
        user_id = selected_users[0]
        for row in range(self.table.rowCount()):
            if int(self.table.item(row, 1).text()) == user_id:
                name = self.table.item(row, 2).text()
                email = self.table.item(row, 3).text()
                self.show_edit_dialog(user_id, name, email)
                break

    def delete_selected_users(self):
        """Delete all selected users"""
        selected_users = self.get_selected_users()
        if not selected_users:
            QMessageBox.warning(self, "Warning", "Please select at least one user to delete")
            return

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Are you sure you want to delete {len(selected_users)} selected users?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for user_id in selected_users:
                delete_user(user_id)
            self.load_users()
