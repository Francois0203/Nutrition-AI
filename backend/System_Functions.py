import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF

def generate_pdf(directory_path, pdf_name, content):
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    # Combine directory path and pdf name to get the full file path
    file_path = os.path.join(directory_path, f"{pdf_name}.pdf")
    
    # Create a PDF object
    pdf = FPDF()
    
    # Add a page to the PDF
    pdf.add_page()
    
    # Set font for the PDF
    pdf.set_font("Arial", size=12)

    # Map the content variables to their values
    data = {
        "BMI": content[0],
        "BAI": content[1],
        "WHR": content[2],
        "Body Fat": content[3],
        "Body Mass": content[4],
        "Exercise Category": content[5],
        "Main Calories": content[6],
        "Optimal Protein": content[7],
        "Optimal Fats": content[8],
        "Optimal Carbs": content[9],
    }

    # Add the health metrics to the PDF
    for key, value in data.items():
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(0, 10, f"{key}: ", ln=True)  # Print the variable name

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, str(value))  # Print the value
        pdf.ln()

    # Process the meals variable
    meals = content[10]  # Assuming meals is the last item in the content array
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(0, 10, "Meals: ", ln=True)
    pdf.set_font("Arial", size=12)

    # Check if meals is a list and add each meal's details
    if isinstance(meals, list):
        for meal in meals:
            # Expecting meal to be a dictionary or list with specific keys
            if isinstance(meal, dict):
                pdf.cell(0, 10, f"Diet Type: {meal.get('Diet_type', 'N/A')}", ln=True)
                pdf.cell(0, 10, f"Recipe Name: {meal.get('recipe_name', 'N/A')}", ln=True)
                pdf.cell(0, 10, f"Protein(g): {meal.get('Protein(g)', 0)}", ln=True)
                pdf.cell(0, 10, f"Carbs(g): {meal.get('Carbs(g)', 0)}", ln=True)
                pdf.cell(0, 10, f"Fat(g): {meal.get('Fat(g)', 0)}", ln=True)
                pdf.cell(0, 10, f"Calories: {meal.get('Calories', 0)}", ln=True)
                pdf.ln()
            else:
                pdf.multi_cell(0, 10, str(meal))  # Fallback for non-dictionary meal items

    # Output the PDF to the specified file path
    try:
        pdf.output(file_path)
        print(f"PDF generated successfully and saved as {file_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

def send_email(receiver_email, subject, body, attachment_path=None):
    sender_email = "38276909@mynwu.ac.za"  
    sender_password = "FMeiringEfundi0203$"  

    # Set up the email parameters
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the email body
    message.attach(MIMEText(body, 'plain'))

    # Attach a file if an attachment path is provided
    if attachment_path:
        # Open the file in binary mode
        try:
            with open(attachment_path, 'rb') as attachment_file:
                # Create MIMEBase object and encode the file
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
                encoders.encode_base64(part)

                # Add header to the attachment
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')

                # Attach the file to the email
                message.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")
            return

    try:
        # Set up the SMTP server for NWU (assuming Office365 is used)
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()  # Enable TLS security

        # Log in to your NWU email account
        server.login(sender_email, sender_password)

        # Send the email
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)

        # Close the server
        server.quit()
        print("Email sent successfully with attachment!" if attachment_path else "Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

def __main__():
    # Generate pdf
    pdf_name = "testing"
    file_path = r"C:\Personal Projects\Nutrition-AI\backend\Resources\Results" 
    
    content = [
        22.5,  # BMI
        24.7,  # BAI
        0.85,   # WHR
        15.5,   # Body Fat
        70.0,   # Body Mass
        "Moderate",  # Exercise Category
        2200,   # Main Calories
        110,    # Optimal Protein
        70,     # Optimal Fats
        300,    # Optimal Carbs
        [       # Meals
            {"Diet_type": "Keto", "recipe_name": "Avocado Salad", "Protein(g)": 10, "Carbs(g)": 5, "Fat(g)": 15, "Calories": 200},
            {"Diet_type": "Paleo", "recipe_name": "Grilled Chicken", "Protein(g)": 30, "Carbs(g)": 0, "Fat(g)": 10, "Calories": 300}
        ]
    ]

    generate_pdf(file_path, pdf_name, content)

    # Send email
    receiver = "francoismeiring0203@gmail.com"
    subject = "Test Email"
    body = "This is a test email sent from Python."
    attachment_path = os.path.join(file_path, pdf_name + '.pdf')

    send_email(receiver, subject, body, attachment_path)

if __name__ == '__main__':
    __main__()