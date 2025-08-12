## How to Run the Project

1. **Install Tesseract OCR Engine**  
   Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).

2. **Update Path in `app.py`**  
   In the file **`app.py`**, replace the existing path to `tesseract.exe` with the actual path where Tesseract is installed on your system.  
   Example:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
3. **Install Required Libraries**
   Run the following command:
   ```python
   pip install pyautogui pyperclip webbrowser flask pytesseract opencv-python numpy werkzeug
4. **Execute**
   Run the following command:
   ```python
   python app.py
