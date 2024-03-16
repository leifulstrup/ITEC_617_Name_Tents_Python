#%%
import os
import pandas as pd
from PyPDF2 import PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth

import tkinter as tk
from tkinter import filedialog

#%%
# Function to open file dialog and return the selected file path
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path


# Function to create name tents PDF
def create_name_tents(first_name, last_name, pdf_file):
    # Create a PDF file
    c = canvas.Canvas(pdf_file, pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # Set up font size and type
    font_size = 72
    c.setFont("Helvetica", font_size)
    
    # Calculate the width of the names at the current font size
    first_name_width = stringWidth(first_name, "Helvetica", font_size)
    last_name_width = stringWidth(last_name, "Helvetica", font_size)
    
    # Decrease the font size until both names fit within the page width
    while max(first_name_width, last_name_width) > width:
        font_size -= 1
        first_name_width = stringWidth(first_name, "Helvetica", font_size)
        last_name_width = stringWidth(last_name, "Helvetica", font_size)
    
    # Set the new font size
    c.setFont("Helvetica", font_size)
    
    # Calculate the position of the names
    x = width / 2
    y = height / 3  # Below the halfway point
    
    # Draw the names
    c.setFillColorRGB(0, 0, 0)  # Set color to black for first name
    c.drawCentredString(x, y, first_name)
    
    c.setFillColorRGB(0.5, 0.5, 0.5)  # Set color to gray for last name
    c.drawCentredString(x, y - font_size, last_name)  # Below the first name

    # Draw a dark line at the fold point along the width of the page
    c.setLineWidth(1)
    c.setStrokeColorRGB(0, 0, 0)  # Set color to black for the line
    c.line(0, height / 2, width, height / 2)  # Draw the line

    # Add "ITEC-617 Spring 2024" in 12 point font in the lower right corner of the page
    c.setFont("Helvetica", 12)
    course_info = "ITEC-617 Spring 2024"
    course_info_width = stringWidth(course_info, "Helvetica", 12)
    c.drawString(width - course_info_width - 10, 10, course_info)  # Adjusted to the lower right corner

    # Save the PDF
    c.save()

def merge_pdfs_in_directory(dir_path, output_filename):
    merger = PdfMerger()

    for item in sorted(os.listdir(dir_path)):
        if item.endswith('.pdf'):
            merger.append(os.path.join(dir_path, item))

    merger.write(output_filename)
    merger.close()
    
def reverse_name(name):
    name_parts = name.split(",")
    return (name_parts[1].strip() + ' ' + name_parts[0]).strip().replace(',', '')

def collect_student_names(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)
    
    # Extract student names; adjust the column name if necessary
    student_names = df['Student'].astype(str).tolist()
    student_names = [name.strip() for name in student_names]
    remove_these_names = ['Student, Test', 'nan', 'Points Possible']
    student_names = [name for name in student_names if not name in remove_these_names]  # Remove empty names
    student_names = [reverse_name(name) for name in student_names]
    return student_names

#%%
def main():
    # Example usage
    # Use file dialog to select the CSV file
    csv_file = select_file()
    student_names = collect_student_names(csv_file)
    if not os.path.isdir('name_tents'):
        os.mkdir('name_tents')
    if csv_file:  # Proceed only if a file was selected
        for name in student_names:
            first_name, last_name = name.split(' ', 1)
            file_name = f"{last_name}_{first_name}.pdf"
            pdf_file = os.path.join('name_tents', file_name)
            create_name_tents(first_name, last_name, pdf_file)
            print(f"PDF file '{pdf_file}' has been created.")
    else:
        print("File selection was cancelled.")

    merge_pdfs_in_directory('name_tents', 'name_tents_all.pdf')

#%%
if __name__ == "__main__":
    main()