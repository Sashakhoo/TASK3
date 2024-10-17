import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image

def generate_pdf(data):
    c = canvas.Canvas("GeneratedForm.pdf", pagesize=letter)
    width, height = letter  # Letter size page dimensions

    c.setFont("Helvetica-Bold", 12)
    
    # Adding a logo
    try:
        logo_path = "logo.png"  # Ensure this is the correct path to your logo file
        logo = Image.open(logo_path)
        aspect_ratio = logo.width / logo.height
        desired_height = 50  # Desired logo height in points
        c.drawInlineImage(logo_path, 30, height - 70, width=desired_height * aspect_ratio, height=desired_height)
    except Exception as e:
        print(f"Error loading logo: {e}")
        
    # Title
    c.drawString(30*mm, height-90*mm, "TEST REPORT ON INSULATION RESISTANCE LEVEL AND DIELECTRIC STRENGTH")

    # Input fields with labels and boxes
    form_fields = {
        'Project': height-110*mm,
        'Location': height-120*mm,
        'Equipment Name': height-130*mm,
        'Equipment Ref. No.': height-140*mm,
        'Rated Voltage (Volts)': height-150*mm,
        'Rated Current (Ampere)': height-160*mm,
        'Operating Frequency (Hertz)': height-170*mm,
        'Rated Short Circuit (Ampere)': height-180*mm
    }

    for field, y_position in form_fields.items():
        c.drawString(30, y_position, f"{field}: {data[field]}")
        c.rect(27, y_position-4, 460, 12)  # Adjust size and placement to match form

    # Test results area
    c.setFont("Helvetica", 10)
    c.drawString(30, height-200*mm, "Test Results (Please tick appropriate):")
    c.drawString(150, height-200*mm, "Pass")
    c.drawString(200, height-200*mm, "Fail")
    c.rect(145, height-201*mm, 12, 12)  # Checkbox for Pass
    c.rect(195, height-201*mm, 12, 12)  # Checkbox for Fail

    # Tick the appropriate checkbox
    if data.get('Result', 'Fail') == 'Pass':
        c.drawString(149, height-200*mm, "X")
    else:
        c.drawString(199, height-200*mm, "X")

    # Signatures
    c.drawString(30, height-220*mm, "Tested By:")
    c.line(90, height-220*mm, 190, height-220*mm)  # Line for signature
    c.drawString(30, height-230*mm, "Witnessed By:")
    c.line(110, height-230*mm, 210, height-230*mm)  # Line for signature

    # Save PDF
    c.save()
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
labels = ['Project', 'Location', 'Equipment Name', 'Equipment Ref. No.', 'Rated Voltage (Volts)', 'Rated Current (Ampere)', 'Operating Frequency (Hertz)', 'Rated Short Circuit (Ampere)']
y_pos = 0
for label in labels:
    ttk.Label(root, text=label).grid(row=y_pos, column=0, padx=10, pady=3, sticky='w')
    entry = ttk.Entry(root, width=40)
    entry.grid(row=y_pos, column=1, padx=10, pady=3, sticky='w')
    entry_widgets[label] = entry
    y_pos += 1

# Result as radio buttons
result_var = tk.StringVar()
result_var.set('Fail')  # Default set to Fail
ttk.Label(root, text="Test Result:").grid(row=y_pos, column=0, padx=10, pady=3, sticky='w')
ttk.Radiobutton(root, text='Pass', value='Pass', variable=result_var).grid(row=y_pos, column=1, padx=10, pady=3, sticky='w')
ttk.Radiobutton(root, text='Fail', value='Fail', variable=result_var).grid(row=y_pos + 1, column=1, padx=10, pady=3, sticky='w')

# Submit Button
submit_btn = ttk.Button(root, text="Generate PDF", command=submit_form)
submit_btn.grid(row=y_pos + 2, column=1, padx=10, pady=20)

root.mainloop()
