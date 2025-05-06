from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QSize
from PyQt6.QtGui import  QFontDatabase , QFont

from enum import Enum
import os

class InputVariant(Enum):
    DEFAULT = "default"
    OUTLINE = "outline"
    GHOST = "ghost"
    ERROR = "error"

class InputSize(Enum):
    DEFAULT = "default"
    SM = "sm"
    XS = "xs"
    LG = "lg"

class Input(QLineEdit):
    def __init__(self, parent=None, placeholder="", variant=InputVariant.DEFAULT, 
                 size=InputSize.DEFAULT, disabled=False, readonly=False):
        super().__init__(parent)
        
        self.variant = variant
        self.size = size
        self.setDisabled(disabled)
        self.setReadOnly(readonly)
        self.setPlaceholderText(placeholder)
        
        # Setup font and apply styling
        font = QFont()
        font.setFamily("Inter, sans-serif")
        font.setWeight(QFont.Weight.Medium)
        self.setFont(font)

        self.apply_styling()
    
    def apply_styling(self):
        # Base styles
        base_style = """
            QLineEdit {
                border-radius: 3px;
                letter-spacing: -0.011em;
                line-height: 1.4;
                background-color: #ffffff;
                color: #0f172a;
            }
            QLineEdit:focus {
                outline: none;
            }
        """
        
        # Size styles - SMALLER SIZES
        size_styles = {
            InputSize.DEFAULT: """
                QLineEdit {
                    padding: 6px 12px;
                    min-height: 32px;
                }
            """,
            InputSize.SM: """
                QLineEdit {
                    padding: 3px 10px;
                    min-height: 26px;
                }
            """,
            InputSize.XS: """
                QLineEdit {
                    padding: 2px 8px;
                    min-height: 22px;
                    border-radius: 2px;
                }
            """,
            InputSize.LG: """
                QLineEdit {
                    padding: 8px 16px;
                    min-height: 40px;
                }
            """
        }
        
        # Variant styles
        variant_styles = {
            InputVariant.DEFAULT: """
                QLineEdit {
                    border: 1px solid #e2e8f0;
                }
                QLineEdit:hover {
                    border-color: #cbd5e1;
                }
                QLineEdit:focus {
                    border-color: #94a3b8;
                    border-width: 1px;
                }
                QLineEdit:disabled {
                    background-color: #f8fafc;
                    color: #94a3b8;
                    border-color: #e2e8f0;
                }
            """,
            InputVariant.OUTLINE: """
                QLineEdit {
                    border: 1px solid #e2e8f0;
                    background-color: transparent;
                }
                QLineEdit:hover {
                    border-color: #cbd5e1;
                }
                QLineEdit:focus {
                    border-color: #94a3b8;
                    border-width: 1px;
                }
                QLineEdit:disabled {
                    background-color: #f8fafc;
                    color: #94a3b8;
                    border-color: #e2e8f0;
                }
            """,
            InputVariant.GHOST: """
                QLineEdit {
                    border: 1px solid transparent;
                    background-color: transparent;
                }
                QLineEdit:hover {
                    background-color: #f1f5f9;
                }
                QLineEdit:focus {
                    background-color: #f8fafc;
                    border-color: #94a3b8;
                }
                QLineEdit:disabled {
                    color: #94a3b8;
                }
            """,
            InputVariant.ERROR: """
                QLineEdit {
                    border: 1px solid #ef4444;
                }
                QLineEdit:hover {
                    border-color: #dc2626;
                }
                QLineEdit:focus {
                    border-color: #b91c1c;
                    border-width: 1px;
                }
                QLineEdit:disabled {
                    background-color: #fecaca;
                    color: #ef4444;
                    border-color: #ef4444;
                }
            """
        }
        
        # Combine styles
        combined_style = base_style + size_styles[self.size] + variant_styles[self.variant]
        self.setStyleSheet(combined_style)
        
    def sizeHint(self):
        if self.size == InputSize.XS:
            return QSize(150, 22)  # Extra small input
        elif self.size == InputSize.SM:
            return QSize(180, 26)  # Small input
        elif self.size == InputSize.LG:
            return QSize(240, 40)  # Large input
        else:
            return QSize(200, 32)  # Default input