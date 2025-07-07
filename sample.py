import sys
import random
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Graph import MainWindow as GraphWindow
from pyModbusTCP.client import ModbusClient


class TemperatureWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperature Monitoring")
        self.setGeometry(200, 200, 600, 400)

        # Modbus client setup
        self.client = ModbusClient(host='localhost', port=5020, auto_open=True)

        self.init_ui()

        # Timer to update readings every 2 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temperatures)
        self.timer.start(2000)  # 2000 ms = 2 seconds

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Temperature Sensors")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Grid layout for sensor displays
        grid_layout = QGridLayout()
        self.temp_labels = []
        self.temp_lcds = []

        for i in range(10):
            label = QLabel(f"T{i + 1:03d}")
            label.setStyleSheet("font-weight: bold; margin: 5px;")

            lcd = QLCDNumber()
            lcd.setDigitCount(5)
            lcd.setStyleSheet("background-color: black; color: lime;")

            self.temp_labels.append(label)
            self.temp_lcds.append(lcd)

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

    def update_temperatures(self):
        try:
            # Attempt to read 10 registers
            regs = self.client.read_holding_registers(0, 10)
            if regs:
                for i in range(10):
                    temp_value = regs[i] / 10.0  # Convert to float (e.g., 235 -> 23.5°C)
                    self.temp_lcds[i].display(temp_value)
                print(f"Temperatures updated: {[r / 10 for r in regs]}")
            else:
                print("Failed to read Modbus registers")
        except Exception as e:
            print(f"Error reading Modbus: {e}")

    def closeEvent(self, event):
        self.timer.stop()
        try:
            self.client.close()
        except:
            pass
        event.accept()


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
            label = QLabel(f"P{i + 1:03d}")
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
            label = QLabel(f"L{i + 1:03d}")
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
            label = QLabel(f"F{i + 1:03d}")
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
        self.setGeometry(200, 200, 500, 400)

        # Initialize Modbus client
        self.client = ModbusClient(host='localhost', port=5020, auto_open=True)

        # Test connection
        self.test_connection()

        self.init_ui()
        self.refresh_valve_states()

        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_valve_states)
        self.refresh_timer.start(2000)  # Refresh every 2 seconds

    def test_connection(self):
        """Test the Modbus connection"""
        try:
            # Try to read a coil to test connection
            result = self.client.read_coils(0, 1)
            if result is not None:
                print(f"✓ Modbus connection successful! Read coil 0: {result}")
            else:
                print("✗ Modbus connection failed - read_coils returned None")
        except Exception as e:
            print(f"✗ Modbus connection error: {e}")

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Valve Controls")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Connection status
        self.status_label = QLabel("Status: Connecting...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: blue; margin: 5px;")
        layout.addWidget(self.status_label)

        # Create valve buttons
        grid_layout = QGridLayout()
        self.valve_buttons = []

        for i in range(7):
            btn = QPushButton(f"VAL{i + 1:03d}")
            btn.setMinimumHeight(50)
            btn.setStyleSheet(self.closed_style())
            btn.clicked.connect(lambda checked, valve_id=i + 1: self.valve_clicked(valve_id))
            self.valve_buttons.append(btn)

            row = i // 3
            col = i % 3
            grid_layout.addWidget(btn, row, col)

        layout.addLayout(grid_layout)

        # Control buttons
        button_layout = QVBoxLayout()

        refresh_btn = QPushButton("Refresh States")
        refresh_btn.clicked.connect(self.refresh_valve_states)
        button_layout.addWidget(refresh_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def refresh_valve_states(self):
        """Read coils from Modbus and update button colors accordingly"""
        try:
            print("Refreshing valve states...")
            # Read 7 coils starting at address 0
            coil_states = self.client.read_coils(0, 7)

            if coil_states is not None:
                print(f"Read coil states: {coil_states}")
                self.status_label.setText("Status: Connected")
                self.status_label.setStyleSheet("color: green; margin: 5px;")

                for i, state in enumerate(coil_states):
                    btn = self.valve_buttons[i]
                    if state:
                        btn.setStyleSheet(self.open_style())
                        btn.setText(f"VAL{i + 1:03d}\n(OPEN)")
                    else:
                        btn.setStyleSheet(self.closed_style())
                        btn.setText(f"VAL{i + 1:03d}\n(CLOSED)")
            else:
                print("Failed to read coils from Modbus server - returned None")
                self.status_label.setText("Status: Read Failed")
                self.status_label.setStyleSheet("color: red; margin: 5px;")

        except Exception as e:
            print(f"Error reading coils: {e}")
            self.status_label.setText(f"Status: Error - {e}")
            self.status_label.setStyleSheet("color: red; margin: 5px;")

    def valve_clicked(self, valve_id):
        """Handle valve button clicks"""
        print(f"Valve {valve_id} clicked")

        # Read current valve coil state
        try:
            print(f"Reading coil {valve_id - 1} state...")
            state = self.client.read_coils(valve_id - 1, 1)

            if state is None:
                QMessageBox.warning(self, "Error", "Failed to read valve state from Modbus.")
                return

            current_state = state[0]  # True or False
            print(f"Current state of valve {valve_id}: {current_state}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Modbus read error: {e}")
            print(f"Error reading valve {valve_id}: {e}")
            return

        # Ask user confirmation
        if current_state:
            msg = f"VAL{valve_id:03d} is currently OPEN.\nDo you want to CLOSE it?"
            new_state = False
        else:
            msg = f"VAL{valve_id:03d} is currently CLOSED.\nDo you want to OPEN it?"
            new_state = True

        reply = QMessageBox.question(self, 'Valve Control', msg,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Write the new coil state
            try:
                print(f"Writing coil {valve_id - 1} = {new_state}")
                success = self.client.write_single_coil(valve_id - 1, new_state)

                if success:
                    action = "opened" if new_state else "closed"
                    QMessageBox.information(self, 'Valve Status',
                                            f'VAL{valve_id:03d} has been {action}!')
                    print(f"Successfully {action} valve {valve_id}")

                    # Refresh button states after change
                    self.refresh_valve_states()
                else:
                    QMessageBox.warning(self, 'Valve Status', 'Failed to write valve state to Modbus.')
                    print(f"Failed to write valve {valve_id} state")

            except Exception as e:
                QMessageBox.warning(self, 'Valve Status', f'Error writing to Modbus: {e}')
                print(f"Error writing valve {valve_id}: {e}")
        else:
            QMessageBox.information(self, 'Valve Status', f'VAL{valve_id:03d} operation cancelled.')

    def open_style(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #45a049;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

    def closed_style(self):
        return """
            QPushButton {
                background-color: #D9534F;
                color: white;
                border: 2px solid #C9302C;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C9302C;
            }
        """

    def closeEvent(self, event):
        """Clean up when closing"""
        print("Closing valve window...")
        self.refresh_timer.stop()
        try:
            self.client.close()
        except:
            pass
        event.accept()


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
            label = QLabel(f"LEAK{i + 1:03d}")
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
        self.client = ModbusClient(host='localhost', port=5020, auto_open=True)

        # Setup timer for updating system time
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_system_time)
        self.time_timer.start(1000)  # Update every second

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

        # System Time Display
        self.create_time_display()
        main_layout.addWidget(self.time_display_widget)

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

    def create_time_display(self):
        """Create the system time display widget"""
        self.time_display_widget = QWidget()
        time_layout = QHBoxLayout()

        # Create time components
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                        stop:0 #e3f2fd, stop:1 #bbdefb);
            border: 2px solid #42a5f5;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        """)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1a237e;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                        stop:0 #c8e6c9, stop:1 #a5d6a7);
            border: 2px solid #4caf50;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        """)

        self.system_status_label = QLabel("SYSTEM ONLINE")
        self.system_status_label.setAlignment(Qt.AlignCenter)
        self.system_status_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                        stop:0 #66bb6a, stop:1 #4caf50);
            border: 2px solid #2e7d32;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        """)

        time_layout.addWidget(self.date_label)
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.system_status_label)

        self.time_display_widget.setLayout(time_layout)

        # Initialize with current time
        self.update_system_time()

    def update_system_time(self):
        """Update the system time display"""
        now = datetime.now()

        # Format date
        date_str = now.strftime("%A, %B %d, %Y")
        self.date_label.setText(date_str)

        # Format time with colorful display
        time_str = now.strftime("%H:%M:%S")
        self.time_label.setText(time_str)

        # Change colors based on time of day
        hour = now.hour
        if 6 <= hour < 12:  # Morning
            self.time_label.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #e65100;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #fff3e0, stop:1 #ffe0b2);
                border: 2px solid #ff9800;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            """)
        elif 12 <= hour < 18:  # Afternoon
            self.time_label.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #1565c0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #e3f2fd, stop:1 #bbdefb);
                border: 2px solid #2196f3;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            """)
        elif 18 <= hour < 22:  # Evening
            self.time_label.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #4a148c;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #f3e5f5, stop:1 #e1bee7);
                border: 2px solid #9c27b0;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            """)
        else:  # Night
            self.time_label.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #e8eaf6;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #1a237e, stop:1 #303f9f);
                border: 2px solid #3f51b5;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            """)

        # Update system status with blinking effect
        if now.second % 2 == 0:
            self.system_status_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #66bb6a, stop:1 #4caf50);
                border: 2px solid #2e7d32;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            """)
        else:
            self.system_status_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #81c784, stop:1 #66bb6a);
                border: 2px solid #388e3c;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
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
        self.trends_window = GraphWindow()
        self.trends_window.show()

    def reports_clicked(self):
        QMessageBox.information(self, "Reports", "Reports generation window would open here")

    def closeEvent(self, event):
        """Clean up when closing the main window"""
        self.time_timer.stop()
        try:
            self.client.close()
        except:
            pass
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look

    # Set application icon and properties
    app.setApplicationName("Sodium Facility for Component Testing (SFCT)")
    app.setApplicationVersion("1.0")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
