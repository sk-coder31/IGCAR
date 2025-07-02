import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TemperatureWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperature Monitoring")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Temperature Sensors")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Create grid for temperature sensors
        grid_layout = QGridLayout()
        self.temp_labels = []
        self.temp_lcds = []
        
        for i in range(10):
            # Label
            label = QLabel(f"T{i+1:03d}")
            label.setStyleSheet("font-weight: bold; margin: 5px;")
            
            # LCD Number
            lcd = QLCDNumber()
            lcd.setDigitCount(5)
            lcd.setStyleSheet("background-color: black; color: lime;")
            # Simulate temperature reading
            temp_value = round(random.uniform(20.0, 100.0), 1)
            lcd.display(temp_value)
            
            self.temp_labels.append(label)
            self.temp_lcds.append(lcd)
            
            # Arrange in 2 columns
            row = i // 2
            col = (i % 2) * 2
            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(lcd, row, col + 1)
        
        layout.addLayout(grid_layout)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class PressureWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pressure Monitoring")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Pressure Sensors")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Create grid for pressure sensors
        grid_layout = QGridLayout()
        self.pressure_labels = []
        self.pressure_lcds = []
        
        for i in range(10):
            # Label
            label = QLabel(f"P{i+1:03d}")
            label.setStyleSheet("font-weight: bold; margin: 5px;")
            
            # LCD Number
            lcd = QLCDNumber()
            lcd.setDigitCount(5)
            lcd.setStyleSheet("background-color: black; color: cyan;")
            # Simulate pressure reading
            pressure_value = round(random.uniform(1.0, 10.0), 2)
            lcd.display(pressure_value)
            
            self.pressure_labels.append(label)
            self.pressure_lcds.append(lcd)
            
            # Arrange in 2 columns
            row = i // 2
            col = (i % 2) * 2
            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(lcd, row, col + 1)
        
        layout.addLayout(grid_layout)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class LevelWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Level Monitoring")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Level Sensors")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        grid_layout = QGridLayout()
        
        for i in range(10):
            label = QLabel(f"L{i+1:03d}")
            label.setStyleSheet("font-weight: bold; margin: 5px;")
            
            lcd = QLCDNumber()
            lcd.setDigitCount(5)
            lcd.setStyleSheet("background-color: black; color: yellow;")
            level_value = round(random.uniform(0.0, 100.0), 1)
            lcd.display(level_value)
            
            row = i // 2
            col = (i % 2) * 2
            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(lcd, row, col + 1)
        
        layout.addLayout(grid_layout)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class FlowWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flow Monitoring")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Flow Sensors")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        grid_layout = QGridLayout()
        
        for i in range(10):
            label = QLabel(f"F{i+1:03d}")
            label.setStyleSheet("font-weight: bold; margin: 5px;")
            
            lcd = QLCDNumber()
            lcd.setDigitCount(5)
            lcd.setStyleSheet("background-color: black; color: orange;")
            flow_value = round(random.uniform(0.0, 50.0), 2)
            lcd.display(flow_value)
            
            row = i // 2
            col = (i % 2) * 2
            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(lcd, row, col + 1)
        
        layout.addLayout(grid_layout)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class ValvesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Valve Control")
        self.setGeometry(200, 200, 400, 300)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Valve Controls")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Create valve buttons
        grid_layout = QGridLayout()
        self.valve_buttons = []
        
        for i in range(7):
            btn = QPushButton(f"VAL{i+1:03d}")
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: 2px solid #45a049;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            btn.clicked.connect(lambda checked, valve_id=i+1: self.valve_clicked(valve_id))
            self.valve_buttons.append(btn)
            
            row = i // 3
            col = i % 3
            grid_layout.addWidget(btn, row, col)
        
        layout.addLayout(grid_layout)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def valve_clicked(self, valve_id):
        reply = QMessageBox.question(self, 'Valve Control', 
                                   f'Do you want to open VAL{valve_id:03d} right now?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, 'Valve Status', f'VAL{valve_id:03d} has been opened!')
        else:
            QMessageBox.information(self, 'Valve Status', f'VAL{valve_id:03d} operation cancelled.')

class LeakWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leak Detection")
        self.setGeometry(200, 200, 600, 350)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Leak Detection Sensors")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        grid_layout = QGridLayout()
        
        for i in range(9):
            label = QLabel(f"LEAK{i+1:03d}")
            label.setStyleSheet("font-weight: bold; margin: 5px;")
            
            lcd = QLCDNumber()
            lcd.setDigitCount(4)
            lcd.setStyleSheet("background-color: black; color: red;")
            leak_value = round(random.uniform(0.0, 10.0), 2)
            lcd.display(leak_value)
            
            row = i // 3
            col = (i % 3) * 2
            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(lcd, row, col + 1)
        
        layout.addLayout(grid_layout)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Industrial Control System")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Industrial Control System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50; 
            margin: 20px; 
            padding: 10px;
            background-color: #ecf0f1;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
        """)
        main_layout.addWidget(title)
        
        # Create grid layout for the four main boxes
        grid_layout = QGridLayout()
        
        # Box 1: Diagnostics
        diagnostics_box = self.create_diagnostics_box()
        grid_layout.addWidget(diagnostics_box, 0, 0)
        
        # Box 2: Process Parameters
        process_params_box = self.create_process_parameters_box()
        grid_layout.addWidget(process_params_box, 0, 1)
        
        # Box 3: Process Control
        process_control_box = self.create_process_control_box()
        grid_layout.addWidget(process_control_box, 1, 0)
        
        # Box 4: Alarms, Trends, Reports
        alarms_box = self.create_alarms_box()
        grid_layout.addWidget(alarms_box, 1, 1)
        
        main_layout.addLayout(grid_layout)
        central_widget.setLayout(main_layout)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #6c757d;
                border-radius: 10px;
                margin: 10px;
                padding-top: 20px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                color: #495057;
                font-size: 14px;
            }
        """)
    
    def create_diagnostics_box(self):
        group_box = QGroupBox("Diagnostics")
        layout = QVBoxLayout()
        
        buttons = [
            ("Quantum (Primary)", self.quantum_primary_clicked),
            ("Quantum (Secondary)", self.quantum_secondary_clicked),
            ("RIO-1", lambda: self.rio_clicked(1)),
            ("RIO-2", lambda: self.rio_clicked(2)),
            ("RIO-3", lambda: self.rio_clicked(3)),
            ("RIO-4", lambda: self.rio_clicked(4)),
            ("RIO-5", lambda: self.rio_clicked(5)),
            ("RIO-6", lambda: self.rio_clicked(6)),
            ("RIO-7", lambda: self.rio_clicked(7)),
            ("Ethernet Connection", self.ethernet_clicked)
        ]
        
        for btn_text, btn_function in buttons:
            btn = QPushButton(btn_text)
            btn.setMinimumHeight(35)
            btn.setStyleSheet(self.get_button_style("#007bff"))
            btn.clicked.connect(btn_function)
            layout.addWidget(btn)
        
        group_box.setLayout(layout)
        return group_box
    
    def create_process_parameters_box(self):
        group_box = QGroupBox("Process Parameters")
        layout = QVBoxLayout()
        
        buttons = [
            ("Temperature", self.temperature_clicked),
            ("Pressure", self.pressure_clicked),
            ("Level", self.level_clicked),
            ("Flow", self.flow_clicked),
            ("Valves", self.valves_clicked),
            ("Leak", self.leak_clicked)
        ]
        
        for btn_text, btn_function in buttons:
            btn = QPushButton(btn_text)
            btn.setMinimumHeight(40)
            btn.setStyleSheet(self.get_button_style("#28a745"))
            btn.clicked.connect(btn_function)
            layout.addWidget(btn)
        
        group_box.setLayout(layout)
        return group_box
    
    def create_process_control_box(self):
        group_box = QGroupBox("Process Control")
        layout = QVBoxLayout()
        
        buttons = [
            ("Set Pointer", self.set_pointer_clicked),
            ("TC Assignment", self.tc_assignment_clicked),
            ("Value Control", self.value_control_clicked),
            ("Enter TC", self.enter_tc_clicked)
        ]
        
        for btn_text, btn_function in buttons:
            btn = QPushButton(btn_text)
            btn.setMinimumHeight(45)
            btn.setStyleSheet(self.get_button_style("#ffc107"))
            btn.clicked.connect(btn_function)
            layout.addWidget(btn)
        
        group_box.setLayout(layout)
        return group_box
    
    def create_alarms_box(self):
        group_box = QGroupBox("Alarms, Trends, Reports")
        layout = QVBoxLayout()
        
        buttons = [
            ("Alarms", self.alarms_clicked),
            ("Trends", self.trends_clicked),
            ("Reports", self.reports_clicked)
        ]
        
        for btn_text, btn_function in buttons:
            btn = QPushButton(btn_text)
            btn.setMinimumHeight(60)
            btn.setStyleSheet(self.get_button_style("#dc3545"))
            btn.clicked.connect(btn_function)
            layout.addWidget(btn)
        
        group_box.setLayout(layout)
        return group_box
    
    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                background-color: {color}aa;
            }}
        """
    
    # Diagnostics button functions
    def quantum_primary_clicked(self):
        QMessageBox.information(self, "Diagnostics", "Quantum Primary System Status: Online")
    
    def quantum_secondary_clicked(self):
        QMessageBox.information(self, "Diagnostics", "Quantum Secondary System Status: Standby")
    
    def rio_clicked(self, rio_number):
        status = "Connected" if random.choice([True, False]) else "Disconnected"
        QMessageBox.information(self, "Diagnostics", f"RIO-{rio_number} Status: {status}")
    
    def ethernet_clicked(self):
        QMessageBox.information(self, "Diagnostics", "Ethernet Connection Status: Active")
    
    # Process Parameters button functions
    def temperature_clicked(self):
        self.temp_window = TemperatureWindow()
        self.temp_window.show()
    
    def pressure_clicked(self):
        self.pressure_window = PressureWindow()
        self.pressure_window.show()
    
    def level_clicked(self):
        self.level_window = LevelWindow()
        self.level_window.show()
    
    def flow_clicked(self):
        self.flow_window = FlowWindow()
        self.flow_window.show()
    
    def valves_clicked(self):
        self.valves_window = ValvesWindow()
        self.valves_window.show()
    
    def leak_clicked(self):
        self.leak_window = LeakWindow()
        self.leak_window.show()
    
    # Process Control button functions
    def set_pointer_clicked(self):
        QMessageBox.information(self, "Process Control", "Set Pointer function activated")
    
    def tc_assignment_clicked(self):
        QMessageBox.information(self, "Process Control", "TC Assignment window would open here")
    
    def value_control_clicked(self):
        QMessageBox.information(self, "Process Control", "Value Control panel activated")
    
    def enter_tc_clicked(self):
        text, ok = QInputDialog.getText(self, 'Enter TC', 'Enter TC Value:')
        if ok and text:
            QMessageBox.information(self, "Process Control", f"TC Value entered: {text}")
    
    # Alarms, Trends, Reports button functions
    def alarms_clicked(self):
        QMessageBox.information(self, "Alarms", "Alarms panel would open here")
    
    def trends_clicked(self):
        QMessageBox.information(self, "Trends", "Trends analysis window would open here")
    
    def reports_clicked(self):
        QMessageBox.information(self, "Reports", "Reports generation window would open here")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application icon and properties
    app.setApplicationName("Industrial Control System")
    app.setApplicationVersion("1.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
