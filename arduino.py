import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QFileDialog, 
                           QMessageBox, QFrame, QSpacerItem, QSizePolicy,
                           QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
import pandas as pd
import serial
import sqlite3

ser = serial.Serial(port="COM4",baudrate=9600,timeout=1);

class CycleCounterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cycle_count = 0
        self.is_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.increment_cycle)
        self.cycle_interval = 1000
        self.previous_count = 0
        self.session_id = None  
        self.offset = 0
        
        # Initialize database first
        self.init_database()
        
        # Initialize UI
        self.initUI()
        
        # AFTER UI is initialized, restore session
        self.restore_session_after_crash()
        
    def get_last_saved_count(self):
        """Get the last saved count from historical data"""
        try:
            query = QSqlQuery("SELECT cycle_count FROM cycle_data ORDER BY id DESC LIMIT 1")
            if query.next():
                return query.value(0)
            return 0
        except Exception as e:
            print(f"Error getting last saved count: {e}")
            return 0
            
    def init_database(self):
        """Initialize SQLite database and create table if it doesn't exist"""
        try:
            self.db_name = 'cycle_counter.db'
            
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.db_name)
            
            if not self.db.open():
                QMessageBox.critical(self, 'Database Error', 'Unable to establish database connection')
                return
            
            # Create main table for historical data
            query = QSqlQuery()
            query.exec_('''
                CREATE TABLE IF NOT EXISTS cycle_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    cycle_count INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create current session table (only one record)
            query.exec_('''
                CREATE TABLE IF NOT EXISTS current_session (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    current_count INTEGER NOT NULL DEFAULT 0,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    session_start DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_running BOOLEAN DEFAULT 0,
                    was_crashed BOOLEAN DEFAULT 0
                )
            ''')
            
            print(f"Database initialized: {self.db_name}")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            QMessageBox.critical(self, 'Database Error', f'Failed to initialize database: {str(e)}')
    
    def restore_session_after_crash(self):
        """Restore session after a potential crash - called AFTER UI initialization"""
        try:
            query = QSqlQuery()
            query.exec_("SELECT current_count, is_running, was_crashed FROM current_session WHERE id = 1")
            
            if query.next():
                stored_count = query.value(0)
                was_running = query.value(1)
                was_crashed = query.value(2)
                
                # If the app was running when it crashed, restore the count
                if was_running or was_crashed:
                    self.cycle_count = stored_count
                    self.previous_count = stored_count
                    self.offset = 0  # Reset offset since we're restoring full count
                    
                    # Update UI with restored values
                    self.cycle_display.setText(str(stored_count))
                    self.session_count_label.setText(str(stored_count))
                    
                    # Show crash recovery message
                    if was_running:
                        self.status_label.setText(f'Recovered from crash - Count restored to {stored_count}')
                        self.status_label.setStyleSheet("color: #f39c12; margin-top: 10px;")
                        
                        # Show save buttons since we have unsaved data
                        self.save_db_button.setVisible(True)
                        self.save_excel_button.setVisible(True)
                        
                        QMessageBox.information(
                            self, 
                            'Crash Recovery', 
                            f'Application recovered from unexpected shutdown.\n\nRestored cycle count: {stored_count}\n\nYou can now save this data or continue counting.'
                        )
                    
                    print(f"Restored session with count: {stored_count}")
                
                # Mark as no longer crashed and not running
                update_query = QSqlQuery()
                update_query.prepare("UPDATE current_session SET is_running = 0, was_crashed = 0, last_updated = ? WHERE id = 1")
                update_query.addBindValue(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                update_query.exec_()
                
            else:
                # Create new session if none exists
                self.create_new_session()
                
        except Exception as e:
            print(f"Session restoration error: {e}")
            # Create new session on error
            self.create_new_session()
    
    def create_new_session(self):
        """Create a new session record"""
        try:
            insert_query = QSqlQuery()
            insert_query.prepare('''
                INSERT OR REPLACE INTO current_session (id, current_count, last_updated, session_start, is_running, was_crashed) 
                VALUES (1, 0, ?, ?, 0, 0)
            ''')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_query.addBindValue(current_time)
            insert_query.addBindValue(current_time)
            insert_query.exec_()
            
            print("Created new session")
            
        except Exception as e:
            print(f"Error creating new session: {e}")
    
    def update_current_session(self, count):
        """Update the current session with new count - called immediately when serial data arrives"""
        try:
            query = QSqlQuery()
            query.prepare('''
                UPDATE current_session 
                SET current_count = ?, last_updated = ?, is_running = ?, was_crashed = 0
                WHERE id = 1
            ''')
            query.addBindValue(count)
            query.addBindValue(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            query.addBindValue(self.is_running)
            
            if query.exec_():
                print(f"Auto-saved count {count} to database")
            else:
                print(f"Failed to auto-save: {query.lastError().text()}")
                
        except Exception as e:
            print(f"Auto-save error: {e}")
    
    def save_to_database(self):
        """Save current session to historical data"""
        current_count = self.cycle_count
        if current_count == 0:
            QMessageBox.warning(self, 'Warning', 'No cycles to save!')
            return
            
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            query = QSqlQuery()
            query.prepare("INSERT INTO cycle_data (timestamp, cycle_count, status) VALUES (?, ?, ?)")
            query.addBindValue(current_time)
            query.addBindValue(int(current_count))
            query.addBindValue('Completed')
            
            if query.exec_():
                self.refresh_table()
                self.status_label.setText(f'Saved {current_count} cycles to historical data')
                self.status_label.setStyleSheet("color: #27ae60; margin-top: 10px;")
                
                # Reset session after successful save
                self.reset_session_after_save()
                
                QMessageBox.information(
                    self, 
                    'Success', 
                    f'Cycle data saved to historical records!\n\nCycles: {current_count}\nTime: {current_time}'
                )
            else:
                raise Exception(query.lastError().text())
                
        except Exception as e:
            QMessageBox.critical(self, 'Database Error', f'Failed to save to database: {str(e)}')
            self.status_label.setText(f'Error saving to database: {str(e)}')
            self.status_label.setStyleSheet("color: #e74c3c; margin-top: 10px;")
    
    def reset_session_after_save(self):
        """Reset session counts after successful save to historical data"""
        try:
            # Reset in-memory counts
            self.cycle_count = 0
            self.previous_count = 0
            self.offset = 0
            
            # Update UI
            self.cycle_display.setText('0')
            self.session_count_label.setText('0')
            
            # Reset in database
            query = QSqlQuery()
            query.prepare('''
                UPDATE current_session 
                SET current_count = 0, last_updated = ?, is_running = 0, was_crashed = 0
                WHERE id = 1
            ''')
            query.addBindValue(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            query.exec_()
            
            # Hide save buttons
            self.save_db_button.setVisible(False)
            self.save_excel_button.setVisible(False)
            
            print("Session reset after save")
            
        except Exception as e:
            print(f"Error resetting session: {e}")
    
    def refresh_table(self):
        """Refresh the table with latest data from database"""
        try:
            query = QSqlQuery("SELECT id, timestamp, cycle_count, status, created_at FROM cycle_data ORDER BY id DESC")
            
            self.table.setRowCount(0)
            
            row = 0
            while query.next():
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # ID
                self.table.setItem(row, 1, QTableWidgetItem(str(query.value(1))))  # Timestamp
                self.table.setItem(row, 2, QTableWidgetItem(str(query.value(2))))  # Cycle Count
                self.table.setItem(row, 3, QTableWidgetItem(str(query.value(3))))  # Status
                self.table.setItem(row, 4, QTableWidgetItem(str(query.value(4))))  # Created At
                
                row += 1
            
            print("Table refreshed")
                
        except Exception as e:
            QMessageBox.critical(self, 'Database Error', f'Failed to refresh table: {str(e)}')
        
    def initUI(self):
        self.setWindowTitle('Cycle Counter Application')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLabel {
                color: #333333;
                font-weight: bold;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f5f5f5;
                selection-background-color: #3498db;
                gridline-color: #ddd;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.tab_widget = QTabWidget()
        central_widget_layout = QVBoxLayout(central_widget)
        central_widget_layout.addWidget(self.tab_widget)
        
        # Counter Tab
        counter_tab = QWidget()
        self.tab_widget.addTab(counter_tab, "Counter")
        
        main_layout = QVBoxLayout(counter_tab)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
      
        title_label = QLabel('Cycle Counter Application')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.cycle_frame = QFrame()
        self.cycle_frame.setFrameStyle(QFrame.Box)
        self.cycle_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        cycle_layout = QVBoxLayout(self.cycle_frame)
        
        cycle_label = QLabel('Current Cycle Count:')
        cycle_label.setAlignment(Qt.AlignCenter)
        cycle_label.setFont(QFont('Arial', 16))
        cycle_label.setStyleSheet("color: #2c3e50; border: none;")
        
        self.cycle_display = QLabel('0')
        self.cycle_display.setAlignment(Qt.AlignCenter)
        self.cycle_display.setFont(QFont('Arial', 48, QFont.Bold))
        self.cycle_display.setStyleSheet("color: #e74c3c; border: none;")
        
        cycle_layout.addWidget(cycle_label)
        cycle_layout.addWidget(self.cycle_display)
        main_layout.addWidget(self.cycle_frame)
        
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_counting)
        self.start_button.setStyleSheet("QPushButton { background-color: #27ae60; }")
        
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_counting)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("QPushButton { background-color: #e74c3c; }")
        
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_count)
        
        self.crash_btn = QPushButton("Simulate Crash")
        self.crash_btn.clicked.connect(self.crash_it)
        self.crash_btn.setStyleSheet("QPushButton { background-color: #8e44ad; }")
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.crash_btn)
        main_layout.addLayout(button_layout)
        
        # Database buttons
        db_button_layout = QHBoxLayout()
        db_button_layout.setSpacing(15)
        
        self.save_db_button = QPushButton('Save to Historical Data')
        self.save_db_button.clicked.connect(self.save_to_database)
        self.save_db_button.setVisible(False)
        self.save_db_button.setStyleSheet("QPushButton { background-color: #9b59b6; }")
        
        self.save_excel_button = QPushButton('Save to Excel')
        self.save_excel_button.clicked.connect(self.save_to_excel)
        self.save_excel_button.setVisible(False)
        self.save_excel_button.setStyleSheet("QPushButton { background-color: #3498db; }")
        
        db_button_layout.addWidget(self.save_db_button)
        db_button_layout.addWidget(self.save_excel_button)
        main_layout.addLayout(db_button_layout)
        
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.status_label = QLabel('Ready to start counting - Data auto-saves on every update')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Arial', 12))
        self.status_label.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        main_layout.addWidget(self.status_label)
        
        # Database Table Tab
        table_tab = QWidget()
        self.tab_widget.addTab(table_tab, "Historical Records")
        
        table_layout = QVBoxLayout(table_tab)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        # Current Session Info
        session_info_layout = QHBoxLayout()
        session_info_label = QLabel('Current Session Auto-Saved Count:')
        session_info_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        
        self.saved_count = QPushButton("Quick Save to DB")
        self.saved_count.clicked.connect(self.to_the_db)
        self.saved_count.setStyleSheet("QPushButton { background-color: #16a085; }")
        
        self.session_count_label = QLabel('0')
        self.session_count_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 16px;")
        
        session_info_layout.addWidget(session_info_label)
        session_info_layout.addWidget(self.session_count_label)
        session_info_layout.addWidget(self.saved_count)
        session_info_layout.addStretch()
        
        table_layout.addLayout(session_info_layout)
        
        # Table controls
        table_controls = QHBoxLayout()
        
        refresh_button = QPushButton('Refresh Table')
        refresh_button.clicked.connect(self.refresh_table)
        refresh_button.setStyleSheet("QPushButton { background-color: #3498db; }")
        
        clear_button = QPushButton('Clear All Records')
        clear_button.clicked.connect(self.clear_database)
        clear_button.setStyleSheet("QPushButton { background-color: #e74c3c; }")
        
        table_controls.addWidget(refresh_button)
        table_controls.addWidget(clear_button)
        table_controls.addStretch()
        
        table_layout.addLayout(table_controls)
        
        # Create table widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Timestamp', 'Cycle Count', 'Status', 'Created At'])
        
        # Set table properties
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSortingEnabled(True)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        table_layout.addWidget(self.table)
        
        # Load initial data
        self.refresh_table()
        
        # Initialize session count display (will be updated by restore_session_after_crash)
        self.session_count_label.setText('0')
        
    def to_the_db(self):
        """Quick save current count to database"""
        current_count = self.cycle_count
        if current_count == 0:
            QMessageBox.warning(self, 'Warning', 'No cycles to save!')
            return
            
        try:
            query = QSqlQuery()
            query.prepare("INSERT INTO cycle_data (timestamp, cycle_count, status) VALUES (?, ?, ?)")
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query.addBindValue(current_time)
            query.addBindValue(int(current_count))
            query.addBindValue('Quick Save')

            if query.exec_():
                self.refresh_table()
                print(f"Quick saved to DB: {current_count}")
                QMessageBox.information(self, 'Success', f'Quick saved {current_count} cycles to database!')
            else:
                print("DB Error:", query.lastError().text())
                QMessageBox.critical(self, 'Error', f'Failed to save: {query.lastError().text()}')
                
        except Exception as e:
            print(f"Error in quick save: {e}")
            QMessageBox.critical(self, 'Error', f'Error saving to database: {str(e)}')
        
    def crash_it(self):
        """Simulate a crash by marking as crashed and entering infinite loop"""
        # Mark as crashed in database before crashing
        try:
            query = QSqlQuery()
            query.prepare("UPDATE current_session SET was_crashed = 1, last_updated = ? WHERE id = 1")
            query.addBindValue(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            query.exec_()
            print("Marked as crashed in database")
        except Exception as e:
            print(f"Error marking crash: {e}")
        
        # Simulate crash with infinite loop
        while True:
            pass
        
    def clear_database(self):
        """Clear all records from database"""
        reply = QMessageBox.question(
            self, 
            'Confirm Clear', 
            'Are you sure you want to clear all records from the database?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                query = QSqlQuery()
                query.exec_("DELETE FROM cycle_data")
                self.refresh_table()
                QMessageBox.information(self, 'Success', 'All historical records cleared from database')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to clear database: {str(e)}')
        
    def start_counting(self):
        """Start counting cycles"""
        ser.write(b"start")
        self.is_running = True
        self.timer.start(self.cycle_interval)
        
        # Update session status
        self.update_session_status(True)
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.save_db_button.setVisible(False)
        self.save_excel_button.setVisible(False)
        
        self.status_label.setText('Counting cycles... (Auto-saving to database)')
        self.status_label.setStyleSheet("color: #27ae60; margin-top: 10px;")
        
    def stop_counting(self):
        """Stop the cycle counting"""
        self.is_running = False
        self.timer.stop()
        
        # Update session status
        self.update_session_status(False)
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # Show save buttons if we have data
        if self.cycle_count > 0:
            self.save_db_button.setVisible(True)
            self.save_excel_button.setVisible(True)
        
        self.status_label.setText(f'Stopped at {self.cycle_count} cycles (Auto-saved)')
        self.status_label.setStyleSheet("color: #e74c3c; margin-top: 10px;")
        
        try:
            ser.write(b"stop")
        except Exception as e:
            print(f"Error sending stop command: {e}")
    
    def update_session_status(self, is_running):
        """Update the running status in current session"""
        try:
            query = QSqlQuery()
            query.prepare("UPDATE current_session SET is_running = ?, last_updated = ? WHERE id = 1")
            query.addBindValue(is_running)
            query.addBindValue(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            query.exec_()
        except Exception as e:
            print(f"Failed to update session status: {e}")
    
    def reset_count(self):
        """Reset the cycle count"""
        if self.is_running:
            self.stop_counting()
        
        # Reset everything
        self.cycle_count = 0
        self.previous_count = 0
        self.offset = 0
        self.cycle_display.setText('0')
        self.session_count_label.setText('0')
        
        # Reset in database
        self.update_current_session(0)
        
        self.save_db_button.setVisible(False)
        self.save_excel_button.setVisible(False)
        
        self.status_label.setText('Count reset to 0 (Auto-saved)')
        self.status_label.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        
    def increment_cycle(self):
        """Read cycle count from Arduino and update display"""
        try:
            data = ser.readline().decode().strip()

            if data:
                try:
                    current_count = int(data)

                    # Update only if count has changed
                    if current_count != self.previous_count:
                        self.previous_count = current_count  # From device

                        # Real count = offset + device count
                        real_count = current_count + self.offset
                        self.cycle_count = real_count
                    
                        # Update GUI
                        self.cycle_display.setText(str(real_count))
                        self.session_count_label.setText(str(real_count))
                    
                        # Save to DB
                        self.update_current_session(real_count)
                        print(f"Updated and auto-saved cycle count: {real_count}")

                except ValueError:
                    print(f"Invalid data received: {data}")

        except Exception as e:
            print(f"Error reading serial data: {e}")

        
    def save_to_excel(self):
        """Save current count to Excel file"""
        current_count = self.cycle_count
        if current_count == 0:
            QMessageBox.warning(self, 'Warning', 'No cycles to save!')
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            'Save Cycle Data', 
            f'cycle_data_{datetime.now().strftime("%Y%m%d")}.xlsx',
            'Excel Files (*.xlsx);;All Files (*)'
        )
        
        if not file_path:
            return
            
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_data = {
                'Timestamp': [current_time],
                'Cycle Count': [current_count],
                'Status': ['Completed']
            }
            new_df = pd.DataFrame(new_data)
            
            if os.path.exists(file_path):
                try:
                    existing_df = pd.read_excel(file_path)
                    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                    self.status_label.setText(f'Data appended to existing file')
                except Exception as e:
                    combined_df = new_df
                    self.status_label.setText(f'Created new file (could not read existing): {str(e)}')
            else:
                combined_df = new_df
                self.status_label.setText('New file created')
            
            combined_df.to_excel(file_path, index=False)
            
            # Reset session after successful save
            self.reset_session_after_save()
            
            QMessageBox.information(
                self, 
                'Success', 
                f'Cycle data saved successfully!\n\nFile: {file_path}\nCycles: {current_count}\nTime: {current_time}'
            )
            
            self.status_label.setText(f'Saved {current_count} cycles to Excel')
            self.status_label.setStyleSheet("color: #27ae60; margin-top: 10px;")
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                'Error', 
                f'Failed to save data to Excel:\n{str(e)}'
            )
            self.status_label.setText(f'Error saving file: {str(e)}')
            self.status_label.setStyleSheet("color: #e74c3c; margin-top: 10px;")
    
    def closeEvent(self, event):
        """Handle application close event"""
        if hasattr(self, 'db') and self.db.isOpen():
            # Update session as not running before closing
            self.update_session_status(False)
            self.db.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = CycleCounterGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
