import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageTk
from datetime import datetime
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# PDF Class with enhanced functionality
class PDF(FPDF):
    def header(self):
        # Add logo (replace with actual logo path)
        try:
            self.image('logo.png', 10, 8, 33)  # Adjust path and size
        except Exception as e:
            print(f"Error loading logo: {e}")
            
        # Add Report number and details on the right
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'S40037 - T02 - 20241015 - 104655', 0, 1, 'R')

        # Add an empty line
        self.ln(10)

        # Add report title in bold
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'T02 TEST REPORT ON INSULATION RESISTANCE AND DIELECTRIC STRENGTH', 0, 1, 'C')

        # Add current date below title
        current_date = datetime.today().strftime("%d/%m/%Y")
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, f'Date: {current_date}', 0, 1, 'C')

        # Add a small space
        self.ln(10)

    def add_table(self, title, data):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_font('Arial', '', 10)
        
        for row in data:
            for item in row:
                self.cell(50, 10, f"{item[0]}:", 0)
                self.cell(100, 10, item[1], 0, 1)

    def add_signature(self, signature_path):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Signature:', 0, 1, 'L')
        self.image(signature_path, x=50, y=self.get_y(), w=60, h=30)  # Add signature image

    def add_picture(self, picture_path):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Picture:', 0, 1, 'L')
        self.image(picture_path, x=50, y=self.get_y(), w=60, h=60)  # Add picture image

# Function to capture a picture using the webcam
def capture_picture():
    cap = cv2.VideoCapture(0)  # Open the webcam
    ret, frame = cap.read()
    
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        cv2.imshow('Captured Image', frame)
        cap.release()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        picture_path_label.config(text="Picture taken: captured_image.jpg")

# Function to create a signature with a drawing tool
def create_signature():
    sign_window = tk.Toplevel(root)
    sign_window.title("Sign Here")

    canvas = tk.Canvas(sign_window, width=400, height=200, bg="white")
    canvas.grid(row=0, column=0)

    # PIL Image for drawing
    image = Image.new("RGB", (400, 200), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    def paint(event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_line(x1, y1, x2, y2, fill="black", width=3)
        draw.line([x1, y1, x2, y2], fill="black", width=3)

    def save_signature():
        image.save("signature.jpg")
        signature_path_label.config(text="Signature saved: signature.jpg")
        sign_window.destroy()

    canvas.bind("<B1-Motion>", paint)

    ttk.Button(sign_window, text="Save Signature", command=save_signature).grid(row=1, column=0)

# Function to generate the PDF with user input data, signature, and picture
def generate_pdf(data):
    pdf = PDF()
    pdf.add_page()

    # Fetch current date
    current_date = datetime.today().strftime("%d/%m/%Y")

    # Add Details Table
    details_data = [
        [("Template Name", "T02 TEST REPORT ON INSULATION RESISTANCE AND DIELECTRIC STRENGTH"), ("Project Name", data['Project'])],
        [("Status", "Draft"), ("Creation Date", current_date)],  # Use current date
        [("Creator", data['Creator']), ("Last Modified Date", current_date)]  # Use current date
    ]
    pdf.add_table('Details', details_data)

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

    # Add Picture if available
    if 'picture_path' in data:
        pdf.add_picture(data['picture_path'])

    # Add Signature if available
    if 'signature_path' in data:
        pdf.add_signature(data['signature_path'])

    # Output the PDF
    pdf.output("GeneratedForm.pdf")
    print("PDF generated successfully!")

# Function to send the PDF via email
def send_email():
    try:
        sender_email = "sashakhoo8@gmail.com"
        sender_password = "jmua ijci eurc qrqr" 
        receiver_email = "receiver-email@example.com"
        subject = "Test Report"
        body = "Please find attached the test report."
        filename = "GeneratedForm.pdf"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(filename, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
        msg.attach(part)

        # Establish server connection (Replace with your SMTP server details)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, "your-password")
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        

# Function to collect data from the form and generate PDF
def submit_form():
    data = {key: entry_widgets[key].get() for key in entry_widgets}
    data['Result'] = result_var.get()  # Get the result from the radio buttons

    # Add signature and picture paths if available
    data['signature_path'] = "signature.jpg" if signature_path_label.cget("text") != "" else None
    data['picture_path'] = "captured_image.jpg" if picture_path_label.cget("text") != "" else None

    generate_pdf(data)

# Setup the GUI
root = tk.Tk()
root.title("Insulation and Dielectric Strength Test Report") 

entry_widgets = {}

# Labels and Entries for form
labels = ['Project', 'Location', 'Equipment Name', 'Rated Voltage (Volts)', 'Rated Current (Ampere)', 'Operating Frequency (Hertz)', 'Rated Short Circuit (Ampere)', 'Creator']
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

# Picture capture button
ttk.Button(root, text="Capture Picture", command=capture_picture).grid(row=y_pos + 2, column=0, padx=10, pady=10)

# Display picture status
picture_path_label = tk.Label(root, text="")
picture_path_label.grid(row=y_pos + 3, column=0, columnspan=2)

# Signature button
ttk.Button(root, text="Create Signature", command=create_signature).grid(row=y_pos + 4, column=0, padx=10, pady=10)

# Display signature status
signature_path_label = tk.Label(root, text="")
signature_path_label.grid(row=y_pos + 5, column=0, columnspan=2)

# Submit and Generate PDF Button
submit_btn = ttk.Button(root, text="Generate PDF", command=submit_form)
submit_btn.grid(row=y_pos + 6, column=0, padx=10, pady=20)

# Send Email Button
email_btn = ttk.Button(root, text="Send via Email", command=send_email)
email_btn.grid(row=y_pos + 6, column=1, padx=10, pady=20)

root.mainloop()
