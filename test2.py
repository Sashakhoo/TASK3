from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Add logo
        self.image('logo.png', 10, 8, 33)  # Adjust the path and size accordingly
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

pdf = PDF()
pdf.add_page()

# Add Details Table
details_data = [
    [("Template Name", "T02 TEST REPORT ON INSULATION RESISTANCE AND DIELECTRIC STRENGTH"), ("Project Name", "MS2240037 CHENGSAN CC")],
    [("Status", "Draft"), ("Creation Date", "15/10/2024")],
    [("Creator & Company Name", "Anthony Leong\nCantal Switchgear Pte Ltd"), ("Last Modified Date", "15/10/2024")]
]
pdf.add_table('Details', details_data)

# Add Workflow History
workflow_history = [
    ["Anthony Leong", "15/10/2024", "Location", ""]
]
pdf.add_workflow_history(workflow_history)

# Add Test Report Title
pdf.add_section_title('T02 TEST REPORT ON INSULATION RESISTANCE AND DIELECTRIC STRENGTH')

# Add Switchboard/Panel Information
panel_info = [
    [("Project Name", "Thomson CC"), ("Location", "541 Yishun Industry Park A")],
    [("Equipment Name", "LV msb"), ("Rated Voltage (Volts)", "415")],
    [("Rated Current (Ampere)", "1600"), ("Operating Frequency (Hertz)", "50Hz")],
    [("Rated Short Circuit (Ampere)", "50kA")]
]
pdf.add_table('Switchboard/Panel Information', panel_info)

# Add Test Results
test_results = [
    ("Insulation Resistance Level Test at 500V DC", "Before 28Y Test (Units: Mohms): 54, After 28Y Test: 47"),
    ("Dielectric Strength Test at 2kV for 60 sec", "62 (Results)")
] 
pdf.add_test_results(test_results)

# Output the PDF
pdf.output("T02_test_report.pdf")
