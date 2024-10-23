from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QFileDialog, QTabWidget, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from off_face_verification import match_faces, rec_face  
import sys
import os
import time  # Import time module to add delays

class App(QWidget):
    def __init__(self):
        super().__init__()

        # Main UI setup
        self.setWindowTitle("Face Matcher")
        self.setGeometry(100, 100, 1320, 700)  # Set window size

        # Create tabs
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()  # Verification tab
        self.tab2 = QWidget()  # Identification tab

        self.init_tab1()
        self.init_tab2()

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.tab1, "Verification")
        self.tab_widget.addTab(self.tab2, "Identification")  

        # Set layout for the widget (main window)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def init_tab1(self):
        # Grid layout for more structured placement
        self.tab1_layout = QGridLayout(self.tab1)
    
        # Desired size for both images
        self.image_width = 500
        self.image_height = 500
    
        # First image
        self.pic = QLabel(self.tab1)
        self.image_path = r"1.jpg"
        pixmap = QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(self.image_width, self.image_height, Qt.KeepAspectRatio)
        self.pic.setPixmap(scaled_pixmap)
    
        # Second image
        self.pic1 = QLabel(self.tab1)
        self.image_path1 = r"2.jpg"
        pixmap1 = QPixmap(self.image_path1)
        scaled_pixmap1 = pixmap1.scaled(self.image_width, self.image_height, Qt.KeepAspectRatio)
        self.pic1.setPixmap(scaled_pixmap1)
    
        # Browse button
        browse_button = QPushButton('Upload picture', self.tab1)
        browse_button.clicked.connect(self.browse_image)
    
        # Match button
        match_button = QPushButton('Match picture', self.tab1)
        match_button.clicked.connect(self.match)
    
        # Result label to display match result
        self.result_label = QLabel(self.tab1)
        self.result_label.setText("Click match to display")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 25px; color: black;")
    
        # Add widgets to grid layout
        self.tab1_layout.addWidget(self.pic, 0, 0)  # Add first image at (0, 0)
        self.tab1_layout.addWidget(self.pic1, 0, 2)  # Add second image at (0, 2)
        self.tab1_layout.addWidget(browse_button, 1, 1)  # Add browse button in the middle
        self.tab1_layout.addWidget(match_button, 2, 1)  # Add match button below browse
        self.tab1_layout.addWidget(self.result_label, 3, 1)  # Add result label at the bottom


    def init_tab2(self):
        # Setup for "Tab 2" using QVBoxLayout for vertical alignment
        self.tab2_layout = QVBoxLayout(self.tab2)
        
        # Center alignment for the layout
        self.tab2_layout.setAlignment(Qt.AlignCenter)
    
        # Image for Identification
        self.id_image_label = QLabel(self.tab2)
        self.id_image_path = r"presidents.jpg"  # Set the default image path here
        pixmap = QPixmap(self.id_image_path)
        scaled_pixmap = pixmap.scaled(self.image_width, self.image_height, Qt.KeepAspectRatio)
        self.id_image_label.setPixmap(scaled_pixmap)
        self.id_image_label.setFixedSize(self.image_width, self.image_height)
        self.id_image_label.setAlignment(Qt.AlignCenter)
    
        # Browse button for Identification
        browse_button_id = QPushButton('Upload picture', self.tab2)
        browse_button_id.setFixedSize(200, 50)  # Adjust button size if needed
        browse_button_id.clicked.connect(self.browse_image)
    
        # Recognize button
        recognize_button = QPushButton('Recognize', self.tab2)
        recognize_button.setFixedSize(200, 50)  # Adjust button size if needed
        recognize_button.clicked.connect(self.recognize_face)
    
        
        # Add widgets to the identification tab layout (all centered)
        self.tab2_layout.addWidget(self.id_image_label, alignment=Qt.AlignCenter)  # Centered image
        self.tab2_layout.addSpacing(20)  # Add some space between widgets
        self.tab2_layout.addWidget(browse_button_id, alignment=Qt.AlignCenter)  # Centered browse button
        self.tab2_layout.addSpacing(20)
        self.tab2_layout.addWidget(recognize_button, alignment=Qt.AlignCenter)  # Centered recognize button
        self.tab2_layout.addSpacing(20)
             

    def browse_image(self):
        # Open file dialog to let the user choose an image for verification
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

        # If a valid file path is selected, load the image
        if file_path:
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(self.image_width, self.image_height, Qt.KeepAspectRatio)
            self.image_path1 = file_path
            self.pic1.setPixmap(scaled_pixmap)

    def match(self):
        # Update the result_label instead of showing a QMessageBox
        if match_faces(self.image_path, self.image_path1):
            self.result_label.setText("Faces Matched!")
        else:
            self.result_label.setText("Faces Did NOT Match!")

    def recognize_face(self):
        # Call the rec_face function and wait for output.jpg to be created
        if self.id_image_path:
            rec_face(self.id_image_path, "Faces")  # Call rec_face
            output_path = "output.jpg"
            # Wait until output.jpg is created
            while not os.path.exists(output_path):
                print("Waiting for output.jpg to be created...")
                time.sleep(0.5)  # Wait for 500 milliseconds before checking again
            
            # Load and display output.jpg in the identification label
            pixmap = QPixmap(output_path)
            scaled_pixmap = pixmap.scaled(self.image_width, self.image_height, Qt.KeepAspectRatio)
            self.id_image_label.setPixmap(scaled_pixmap)  # Update the label to show output.jpg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
