from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from enum import Enum

class LabelVariant(Enum):
    DEFAULT = "default"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"
    DARK = "dark"
    LIGHT = "light"
    MUTED = "muted"

class LabelSize(Enum):
    DEFAULT = "default"
    SM = "sm"
    XS = "xs"
    LG = "lg"
    XXS = "xxs"  # Extra extra small
    XXL = "xxl"  # Extra extra large
    COMPACT = "compact"  # Very compact size

class Label(QLabel):
    def __init__(self, text="", parent=None, variant=LabelVariant.DEFAULT, 
                 size=LabelSize.DEFAULT, bold=False, italic=False, 
                 align=Qt.AlignmentFlag.AlignLeft):
        super().__init__(text, parent)
        
        self.variant = variant
        self.size = size
        self.setAlignment(align)
        
        # Setup font
        font = QFont()
        font.setFamily("Inter, sans-serif")
        font.setBold(bold)
        font.setItalic(italic)
        self.setFont(font)

        self.apply_styling()
    
    def apply_styling(self):
        # Base styles
        base_style = """
            QLabel {
                letter-spacing: -0.011em;
                line-height: 1.4;
            }
        """
        
        # Size styles
        size_styles = {
            LabelSize.DEFAULT: """
                QLabel {
                    font-size: 14px;
                    padding: 2px 0;
                }
            """,
            LabelSize.SM: """
                QLabel {
                    font-size: 13px;
                    padding: 1px 0;
                }
            """,
            LabelSize.XS: """
                QLabel {
                    font-size: 12px;
                    padding: 1px 0;
                }
            """,
            LabelSize.LG: """
                QLabel {
                    font-size: 16px;
                    padding: 3px 0;
                }
            """,
            LabelSize.XXS: """
                QLabel {
                    font-size: 11px;
                    padding: 0;
                }
            """,
            LabelSize.XXL: """
                QLabel {
                    font-size: 18px;
                    padding: 4px 0;
                }
            """,
            LabelSize.COMPACT: """
                QLabel {
                    font-size: 10px;
                    padding: 0;
                }
            """
        }
        
        # Variant styles
        variant_styles = {
            LabelVariant.DEFAULT: """
                QLabel {
                    color: #0f172a;
                }
            """,
            LabelVariant.PRIMARY: """
                QLabel {
                    color: #3b82f6;
                }
            """,
            LabelVariant.SECONDARY: """
                QLabel {
                    color: #64748b;
                }
            """,
            LabelVariant.SUCCESS: """
                QLabel {
                    color: #22c55e;
                }
            """,
            LabelVariant.WARNING: """
                QLabel {
                    color: #f59e0b;
                }
            """,
            LabelVariant.ERROR: """
                QLabel {
                    color: #ef4444;
                }
            """,
            LabelVariant.INFO: """
                QLabel {
                    color: #3b82f6;
                }
            """,
            LabelVariant.DARK: """
                QLabel {
                    color: #0f172a;
                }
            """,
            LabelVariant.LIGHT: """
                QLabel {
                    color: #f8fafc;
                }
            """,
            LabelVariant.MUTED: """
                QLabel {
                    color: #94a3b8;
                }
            """
        }
        
        # Combine styles
        combined_style = base_style + size_styles[self.size] + variant_styles[self.variant]
        self.setStyleSheet(combined_style)

    def set_text(self, text):
        """Set text with current styling"""
        self.setText(text)

    def set_bold(self, bold=True):
        """Set bold font weight"""
        font = self.font()
        font.setBold(bold)
        self.setFont(font)

    def set_italic(self, italic=True):
        """Set italic font style"""
        font = self.font()
        font.setItalic(italic)
        self.setFont(font)

    def set_align(self, align):
        """Set text alignment"""
        self.setAlignment(align)

    def set_variant(self, variant):
        """Change label variant"""
        self.variant = variant
        self.apply_styling()

    def set_size(self, size):
        """Change label size"""
        self.size = size
        self.apply_styling() 