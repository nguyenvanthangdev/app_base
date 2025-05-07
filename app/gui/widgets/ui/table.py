from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView,
    QWidget, QHBoxLayout, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from enum import Enum

class TableVariant(Enum):
    DEFAULT = "default"
    STRIPED = "striped"
    BORDERED = "bordered"
    COMPACT = "compact"

class TableSize(Enum):
    DEFAULT = "default"
    SM = "sm"
    LG = "lg"
    COMPACT = "compact"

class Table(QTableWidget):
    # Custom signals
    row_selected = pyqtSignal(int)  # Emits row index when selected
    checkbox_changed = pyqtSignal(int, bool)  # Emits row index and checked state

    def __init__(
        self,
        parent=None,
        variant=TableVariant.DEFAULT,
        size=TableSize.DEFAULT,
        show_checkbox=True,
        row_height=50,
        selection_mode=QTableWidget.SelectionMode.NoSelection
    ):
        super().__init__(parent)
        
        self.variant = variant
        self.size = size
        self.show_checkbox = show_checkbox
        self.row_height = row_height
        
        self._setup_table()
        self._apply_styling()

    def _setup_table(self):
        """Setup basic table properties"""
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(self.variant == TableVariant.STRIPED)

    def _apply_styling(self):
        """Apply styling based on variant and size"""
        # Base styles
        base_style = """
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """
        
        # Size styles
        size_styles = {
            TableSize.DEFAULT: """
                QTableWidget::item {
                    padding: 8px;
                }
            """,
            TableSize.SM: """
                QTableWidget::item {
                    padding: 6px;
                }
            """,
            TableSize.LG: """
                QTableWidget::item {
                    padding: 10px;
                }
            """,
            TableSize.COMPACT: """
                QTableWidget::item {
                    padding: 4px;
                }
            """
        }
        
        # Variant styles
        variant_styles = {
            TableVariant.DEFAULT: """
                QTableWidget {
                    border: none;
                }
            """,
            TableVariant.STRIPED: """
                QTableWidget {
                    alternate-background-color: #f8f9fa;
                }
            """,
            TableVariant.BORDERED: """
                QTableWidget {
                    border: 1px solid #e0e0e0;
                }
                QTableWidget::item {
                    border-bottom: 1px solid #e0e0e0;
                }
            """,
            TableVariant.COMPACT: """
                QTableWidget::item {
                    padding: 2px;
                }
            """
        }
        
        # Header styles
        header_style = """
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #e0e0e0;
                font-weight: bold;
                color: #2c3e50;
            }
        """
        
        # Combine all styles
        self.setStyleSheet(
            base_style +
            size_styles[self.size] +
            variant_styles[self.variant] +
            header_style
        )

    def set_headers(self, headers):
        """Set table headers"""
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Set header alignment
        for i in range(len(headers)):
            header_item = self.horizontalHeaderItem(i)
            if header_item:
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def add_row(self, data, row_index=None):
        """Add a row to the table"""
        if row_index is None:
            row_index = self.rowCount()
        
        self.insertRow(row_index)
        self.setRowHeight(row_index, self.row_height)
        
        # Add checkbox if enabled
        if self.show_checkbox:
            checkbox = QCheckBox()
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            
            # Connect checkbox signal
            checkbox.stateChanged.connect(
                lambda state, r=row_index: self.checkbox_changed.emit(r, state == Qt.CheckState.Checked.value)
            )
            
            self.setCellWidget(row_index, 0, checkbox_widget)
            start_col = 1
        else:
            start_col = 0
        
        # Add data cells
        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            if col == 0 and not self.show_checkbox:  # ID column
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row_index, col + start_col, item)

    def get_selected_rows(self):
        """Get list of selected row indices"""
        selected_rows = []
        for row in range(self.rowCount()):
            if self.show_checkbox:
                checkbox_widget = self.cellWidget(row, 0)
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    selected_rows.append(row)
        return selected_rows

    def clear_selection(self):
        """Clear all checkboxes"""
        for row in range(self.rowCount()):
            if self.show_checkbox:
                checkbox_widget = self.cellWidget(row, 0)
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(False)

    def set_variant(self, variant):
        """Change table variant"""
        self.variant = variant
        self.setAlternatingRowColors(variant == TableVariant.STRIPED)
        self._apply_styling()

    def set_size(self, size):
        """Change table size"""
        self.size = size
        self._apply_styling() 