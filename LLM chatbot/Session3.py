# -*- coding: utf-8 -*-
"""
Created on Oct 20 14:01:40 2024

@author: HP
"""

import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTextEdit

class CellTrackerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Layout
        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Enter your question:")
        layout.addWidget(self.label)

        # Textbox for user input
        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        # Button for submitting the question
        self.button = QPushButton('Submit', self)
        layout.addWidget(self.button)

        # Text area to display the API response
        self.response_area = QTextEdit(self)
        self.response_area.setReadOnly(True)
        layout.addWidget(self.response_area)

        # Set the layout
        self.setLayout(layout)

        # Button click event
        self.button.clicked.connect(self.on_click)

        # Window settings
        self.setWindowTitle("Cell Tracker")
        self.setGeometry(300, 300, 400, 300)
        self.show()

    def on_click(self):
        # Get user input from the textbox
        user_input = self.textbox.text()

        # Call the API and display the response
        if user_input:
            response = self.call_api(user_input)
            if response:
                self.response_area.setText(response)
            else:
                self.response_area.setText("Error: Could not get a valid response from the server.")
        else:
            self.response_area.setText("Please enter a valid question.")

    def call_api(self, user_input):
        try:
            # Set your API endpoint URL
            base_url = "https://3e00-34-142-246-179.ngrok-free.app"  # Update this with your actual base URL
            endpoint = f"{base_url}/generate"
            
            # API headers
            headers = {"Content-Type": "application/json"}
            
            # Create the request payload
            data = {
                "inputs": f"\n\n### Instructions:\n{user_input}\n\n### Response:\n",  # Use 'inputs'
                "parameters": {"stop": ["\n", "###"]}  # Use 'parameters' for additional options like 'stop'
            }
            
            # Send POST request to the API
            response = requests.post(endpoint, headers=headers, json=data)
            
            # Parse the response
            if response.status_code == 200:
                output = response.json()
                return output.get("generated_text", "No response text received.")
            else:
                return f"Error {response.status_code}: {response.text}"
        
        except Exception as e:
            return f"Exception occurred: {str(e)}"

# Main entry point for the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = CellTrackerGUI()
    sys.exit(app.exec_())
