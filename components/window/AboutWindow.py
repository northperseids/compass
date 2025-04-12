from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class AboutWindow(QDialog):
    def __init__(self, parent, compass_version):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.setWindowTitle('About')

        title = QLabel()
        title.setText('Compass Shortcuts')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel()
        version.setText(compass_version)
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        usage = QLabel()
        usage.setFixedWidth(300)
        usage.setWordWrap(True)
        usage.setContentsMargins(10, 10, 10, 10)
        usage.setText('To change the PARENT DIRECTORY:\n\n1. Right-click and choose Settings.\n2. Paste the FULL DIRECTORY PATH into the text box and click Submit.\n\n\nTo change colors:\n\n1. Right-click and open Settings.\n2. Paste either an HTML-compatible color name (white, black, etc.) or a hex code (#FFFFFF for white, for example) into the desired color fields.\n3. Click "Save Settings.')

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(usage)

        self.setLayout(layout)

        self.show()
