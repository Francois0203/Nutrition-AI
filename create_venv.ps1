Set-Location ($pwd).path
python -m venv venv
venv\Scripts\activate.ps1

# GUI libraries
pip install tkinter
pip install customtkinter

# Data manipulation and analysis libraries
pip install pandas
pip install numpy

# Scientific computing libraries
pip install seaborn
pip install matplotlib.pyplot

deactivate
Exit