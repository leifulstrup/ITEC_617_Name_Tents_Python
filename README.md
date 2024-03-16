ITEC 617 Name Tents

This Python script is used to create name tents for the ITEC-617 course in Spring 2024. The script reads student names from a CSV file, creates individual PDF files for each student, and then merges all the PDFs into a single file.

Dependencies
The script uses the following Python libraries:

os
pandas
PyPDF2
reportlab
tkinter
Functions
The script contains the following functions:

select_file: Opens a file dialog and returns the selected file path.
create_name_tents: Creates a PDF file for a name tent given a first name, last name, and a PDF file path. The name tent includes the first name, last name, and the course information "ITEC-617 Spring 2024".
merge_pdfs_in_directory: Merges all PDF files in a given directory into a single PDF file.
reverse_name: Reverses the order of a name.
collect_student_names: Collects student names from a given CSV file.
Usage
To use this script, run the main function. This will open a file dialog for you to select the CSV file containing the student names. The script will then create individual PDF files for each student in the same directory as the CSV file, and finally merge all the PDFs into a single file named "merged.pdf".

if __name__ == "__main__":
    main()

Please ensure that the CSV file is formatted correctly, with columns for first names and last names.
