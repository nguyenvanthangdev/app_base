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

class ButtonSize(Enum):
    DEFAULT = "default"
    SM = "sm"
    LG = "lg"
    ICON = "icon"
    

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
        # Base styles with improved typography - REMOVED transition property
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
            """
        }
        
        # Combine styles
        combined_style = base_style + size_styles[self.size] + variant_styles[self.variant]
        self.setStyleSheet(combined_style)
        
    def sizeHint(self):
        if self.size == ButtonSize.ICON:
            return QSize(40, 40)
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