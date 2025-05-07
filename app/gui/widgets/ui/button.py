from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from enum import Enum
import sys
import os

class ButtonVariant(Enum):
    DEFAULT = "default"
    DESTRUCTIVE = "destructive"
    OUTLINE = "outline"
    SECONDARY = "secondary"
    GHOST = "ghost"
    LINK = "link"
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"
    DARK = "dark"
    LIGHT = "light"

class ButtonSize(Enum):
    DEFAULT = "default"
    SM = "sm"
    LG = "lg"
    ICON = "icon"
    XXS = "xxs"  # Extra extra small
    XXL = "xxl"  # Extra extra large
    COMPACT = "compact"  # Very compact size
    SQUARE = "square"  # Square button with equal width and height

class Button(QPushButton):
    def __init__(self, text, parent=None, variant=ButtonVariant.DEFAULT, 
                 size=ButtonSize.DEFAULT, icon=None, disabled=False):
        super().__init__(text, parent)
        
        self.variant = variant
        self.size = size
        self.setDisabled(disabled)
        
        if icon:
            self.setIcon(icon)
        
        # Setup font 
        font = QFont()
        font.setFamily("Inter, sans-serif")
        font.setWeight(QFont.Weight.Medium)
        self.setFont(font)
        
        # Apply styling
        self.apply_styling()
    
    def apply_styling(self):
        # Base styles with improved typography
        base_style = """
            QPushButton {
                border-radius: 4px;
                font-weight: 500;
                text-align: center;
                letter-spacing: -0.011em;
                line-height: 1.6;
            }
            QPushButton:focus {
                outline: none;
            }
        """
        
        # Size styles with better vertical alignment
        size_styles = {
            ButtonSize.DEFAULT: """
                QPushButton {
                    padding: 4px 12px;
                    font-size: 12px;
                    min-height: 28px;
                }
            """,
            ButtonSize.SM: """
                QPushButton {
                    padding: 4px 12px;
                    font-size: 12px;
                    min-height: 26px;
                }
            """,
            ButtonSize.LG: """
                QPushButton {
                    padding: 6px 14px;
                    font-size: 14px;
                    min-height: 36px;
                }
            """,
            ButtonSize.ICON: """
                QPushButton {
                    padding: 8px;
                    font-size: 14px;
                    min-height: 40px;
                    min-width: 40px;
                }
            """,
            ButtonSize.XXS: """
                QPushButton {
                    padding: 2px 8px;
                    font-size: 10px;
                    min-height: 20px;
                    border-radius: 2px;
                }
            """,
            ButtonSize.XXL: """
                QPushButton {
                    padding: 8px 20px;
                    font-size: 16px;
                    min-height: 44px;
                }
            """,
            ButtonSize.COMPACT: """
                QPushButton {
                    padding: 1px 6px;
                    font-size: 10px;
                    min-height: 18px;
                    border-radius: 2px;
                }
            """,
            ButtonSize.SQUARE: """
                QPushButton {
                    padding: 8px;
                    font-size: 12px;
                    min-height: 32px;
                    min-width: 32px;
                }
            """
        }
        
        # Variant styles with refined colors
        variant_styles = {
            ButtonVariant.DEFAULT: """
                QPushButton {
                    background-color: #020817;
                    color: #ffffff;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #1a2c4d;
                }
                QPushButton:pressed {
                    background-color: #0f172a;
                }
                QPushButton:disabled {
                    background-color: #e2e8f0;
                    color: #94a3b8;
                }
            """,
            ButtonVariant.DESTRUCTIVE: """
                QPushButton {
                    background-color: #ef4444;
                    color: #ffffff;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #dc2626;
                }
                QPushButton:pressed {
                    background-color: #b91c1c;
                }
                QPushButton:disabled {
                    background-color: #fecaca;
                    color: #ef4444;
                }
            """,
            ButtonVariant.OUTLINE: """
                QPushButton {
                    background-color: transparent;
                    color: #020817;
                    border: 1px solid #e2e8f0;
                }
                QPushButton:hover {
                    background-color: #f8fafc;
                    border-color: #cbd5e1;
                }
                QPushButton:pressed {
                    background-color: #f1f5f9;
                }
                QPushButton:disabled {
                    color: #94a3b8;
                    border-color: #e2e8f0;
                }
            """,
            ButtonVariant.SECONDARY: """
                QPushButton {
                    background-color: #f1f5f9;
                    color: #0f172a;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #e2e8f0;
                }
                QPushButton:pressed {
                    background-color: #cbd5e1;
                }
                QPushButton:disabled {
                    background-color: #f8fafc;
                    color: #94a3b8;
                }
            """,
            ButtonVariant.GHOST: """
                QPushButton {
                    background-color: transparent;
                    color: #0f172a;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #f1f5f9;
                }
                QPushButton:pressed {
                    background-color: #e2e8f0;
                }
                QPushButton:disabled {
                    color: #94a3b8;
                }
            """,
            ButtonVariant.LINK: """
                QPushButton {
                    background-color: transparent;
                    color: #0f172a;
                    border: none;
                    text-decoration: underline;
                    padding: 0;
                }
                QPushButton:hover {
                    color: #1e293b;
                }
                QPushButton:pressed {
                    color: #0f172a;
                }
                QPushButton:disabled {
                    color: #94a3b8;
                }
            """,
            ButtonVariant.SUCCESS: """
                QPushButton {
                    background-color: #22c55e;
                    color: #ffffff;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #16a34a;
                }
                QPushButton:pressed {
                    background-color: #15803d;
                }
                QPushButton:disabled {
                    background-color: #dcfce7;
                    color: #22c55e;
                }
            """,
            ButtonVariant.WARNING: """
                QPushButton {
                    background-color: #f59e0b;
                    color: #ffffff;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #d97706;
                }
                QPushButton:pressed {
                    background-color: #b45309;
                }
                QPushButton:disabled {
                    background-color: #fef3c7;
                    color: #f59e0b;
                }
            """,
            ButtonVariant.INFO: """
                QPushButton {
                    background-color: #3b82f6;
                    color: #ffffff;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
                QPushButton:pressed {
                    background-color: #1d4ed8;
                }
                QPushButton:disabled {
                    background-color: #dbeafe;
                    color: #3b82f6;
                }
            """,
            ButtonVariant.DARK: """
                QPushButton {
                    background-color: #0f172a;
                    color: #ffffff;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #1e293b;
                }
                QPushButton:pressed {
                    background-color: #334155;
                }
                QPushButton:disabled {
                    background-color: #1e293b;
                    color: #64748b;
                }
            """,
            ButtonVariant.LIGHT: """
                QPushButton {
                    background-color: #f8fafc;
                    color: #0f172a;
                    border: 1px solid #e2e8f0;
                }
                QPushButton:hover {
                    background-color: #f1f5f9;
                }
                QPushButton:pressed {
                    background-color: #e2e8f0;
                }
                QPushButton:disabled {
                    background-color: #f8fafc;
                    color: #94a3b8;
                    border-color: #e2e8f0;
                }
            """
        }
        
        # Combine styles
        combined_style = base_style + size_styles[self.size] + variant_styles[self.variant]
        self.setStyleSheet(combined_style)
        
    def sizeHint(self):
        if self.size == ButtonSize.ICON:
            return QSize(40, 40)
        elif self.size == ButtonSize.XXS:
            return QSize(60, 20)
        elif self.size == ButtonSize.XXL:
            return QSize(200, 44)
        elif self.size == ButtonSize.COMPACT:
            return QSize(50, 18)
        elif self.size == ButtonSize.SQUARE:
            return QSize(32, 32)
        return super().sizeHint()


# # Example usage
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
    
#     # Create buttons with different variants
#     default_button = Button("Default Button")
#     destructive_button = Button("Destructive", variant=ButtonVariant.DESTRUCTIVE)
#     outline_button = Button("Outline", variant=ButtonVariant.OUTLINE)
#     secondary_button = Button("Secondary", variant=ButtonVariant.SECONDARY)
#     ghost_button = Button("Ghost", variant=ButtonVariant.GHOST)
#     link_button = Button("Link", variant=ButtonVariant.LINK)
    
#     # Create buttons with different sizes
#     sm_button = Button("Small Button", size=ButtonSize.SM)
#     lg_button = Button("Large Button", size=ButtonSize.LG)
#     icon_button = Button("", size=ButtonSize.ICON)
    
#     # Create a disabled button
#     disabled_button = Button("Disabled Button", disabled=True)
    
#     # Show buttons
#     default_button.show()
#     destructive_button.show()
#     outline_button.show()
#     secondary_button.show()
#     ghost_button.show()
#     link_button.show()
#     sm_button.show()
#     lg_button.show()
#     icon_button.show()
#     disabled_button.show()
    
#     sys.exit(app.exec())