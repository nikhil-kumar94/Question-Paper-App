import google.generativeai as genai
# Hardcode your API key here
API_KEY = "AIzaSyAN8udw5yLxdrsQHsEq08hG9jmcDUEEEqc"

# Configure the API with your hardcoded API key
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Path to the PDF file in the 'files' folder
file_path = "./files/Verity-By-Colleen-Hoover.pdf" 
sample_file = genai.upload_file(path=file_path, display_name="My File PDF")

# Confirm upload
print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

# Generate content using the uploaded document
response = model.generate_content([sample_file, "What are My name?"])

# Print the generated content
print(response.text)