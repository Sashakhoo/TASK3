import tkinter as tk
from tkinter import ttk
from fpdf import FPDF
from PIL import Image
from datetime import datetime

# Class for generating the PDF
class PDF(FPDF):
    def header(self):
        try:
            self.image('logo.png', 10, 8, 33)  # Adjust the path and size accordingly
        except Exception as e:
            print(f"Error loading logo: {e}")
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'S40037 - T02 - 20241015 - 104655', 0, 1, 'R')
        self.ln(20)

    def add_table(self, title, data):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_font('Arial', '', 10)
        
        for row in data:
            for item in row:
                self.cell(50, 10, f"{item[0]}:", 0)
                self.cell(100, 10, item[1], 0, 1)

    def add_section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def add_workflow_history(self, history_data):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Workflow History', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        # Add table headers
        self.cell(40, 10, 'Name', 1)
        self.cell(40, 10, 'Date', 1)
        self.cell(40, 10, 'Location', 1)
        self.cell(60, 10, 'Signature', 1, 1)

        # Add table data
        for row in history_data:
            self.cell(40, 10, row[0], 1)
            self.cell(40, 10, row[1], 1)
            self.cell(40, 10, row[2], 1)
            self.cell(60, 10, row[3], 1, 1)

    def add_test_results(self, results):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'T02 TEST REPORT ON INSULATION RESISTANCE AND DIELECTRIC STRENGTH', 0, 1, 'L')
        self.set_font('Arial', '', 10)

        for result in results:
            self.cell(60, 10, f"{result[0]}:", 1)
            self.cell(100, 10, result[1], 1, 1)

# Function to generate the PDF with data from form
def generate_pdf(data):
    pdf = PDF()
    pdf.add_page()
    
    current_date = datetime.today().strftime("%d/%m/%Y")  # Format as DD/MM/YYYY

    # Add Details Table
    details_data = [
        [("Template Name", "T02 TEST REPORT ON INSULATION RESISTANCE AND DIELECTRIC STRENGTH"), ("Project Name", data['Project'])],
        [("Status", "Draft"), ("Creation Date", "current_date")],
        [("Creator", "Anthony Leong"), ("Last Modified Date", current_date)]
    ]
    pdf.add_table('Details', details_data)

    # Add Workflow History
    workflow_history = [
        ["Anthony Leong", "current_date", "YiShun Ave", ""]
    ]
    pdf.add_workflow_history(workflow_history)

    # Add Test Report Title
    pdf.add_section_title('T02 TEST REPORT ON INSULATION RESISTANCE AND DIELECTRIC STRENGTH')

    # Add Switchboard/Panel Information
    panel_info = [
        [("Project Name", data['Project']), ("Location", data['Location'])],
        [("Equipment Name", data['Equipment Name']), ("Rated Voltage (Volts)", data['Rated Voltage (Volts)'])],
        [("Rated Current (Ampere)", data['Rated Current (Ampere)']), ("Operating Frequency (Hertz)", data['Operating Frequency (Hertz)'])],
        [("Rated Short Circuit (Ampere)", data['Rated Short Circuit (Ampere)'])]
    ]
    pdf.add_table('Switchboard/Panel Information', panel_info)

    # Add Test Results
    test_results = [
        ("Insulation Resistance Level Test at 500V DC", f"Before: 54, After: 47"),
        ("Dielectric Strength Test at 2kV for 60 sec", f"{data['Result']}")
    ]
    pdf.add_test_results(test_results)

    # Output the PDF
    pdf.output("GeneratedForm.pdf")
    print("PDF generated successfully!")

# Function to collect data from the form and generate PDF
def submit_form():
    data = {key: entry_widgets[key].get() for key in entry_widgets}
    data['Result'] = result_var.get()  # Get the result from the radio buttons
    generate_pdf(data)

# Setup the GUI
root = tk.Tk()
root.title("Insulation and Dielectric Strength Test Report")

entry_widgets = {}

# Labels and Entries for form
labels = ['Project', 'Location', 'Equipment Name', 'Rated Voltage (Volts)', 'Rated Current (Ampere)', 'Operating Frequency (Hertz)', 'Rated Short Circuit (Ampere)']
y_pos = 0
for label in labels:
    ttk.Label(root, text=label).grid(row=y_pos, column=0, padx=10, pady=3, sticky='w')
    entry = ttk.Entry(root, width=40)
    entry.grid(row=y_pos, column=1, padx=10, pady=3, sticky='w')
    entry_widgets[label] = entry
    y_pos += 1

# Result as radio buttons
result_var = tk.StringVar()
result_var.set('Pass')  # Default set to Pass 
ttk.Label(root, text="Test Result:").grid(row=y_pos, column=0, padx=10, pady=3, sticky='w')
ttk.Radiobutton(root, text='Pass', value='Pass', variable=result_var).grid(row=y_pos, column=1, padx=10, pady=3, sticky='w')
ttk.Radiobutton(root, text='Fail', value='Fail', variable=result_var).grid(row=y_pos + 1, column=1, padx=10, pady=3, sticky='w')

# Submit Button
submit_btn = ttk.Button(root, text="Generate PDF", command=submit_form)
submit_btn.grid(row=y_pos + 2, column=1, padx=10, pady=20)

root.mainloop()
