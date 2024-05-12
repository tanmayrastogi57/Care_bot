import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import sklearn as ak
from joblib import dump, load
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os

#importing pretrained model
model_file = 'random_forest_model.joblib'
rf=load(model_file)

def predict(input_data):
    #preprocessed_input = preprocess_input(input_data)
    prediction = rf.predict(input_data)
    return prediction
#after clicking submit button
def submit_action():
    # Remove all widgets from the frame except the background image
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label) and widget["bg"] != "white":  # Keep the background image label
            continue
        widget.destroy()

    # Display and store patient details them in a list
    values = []
    for i, (label_text, value) in enumerate(zip(labels, [sex_var.get(), age_var.get(), smoker_var.get(), cigarettes_var.get(), bp_medication_var.get(), preva_var.get(), pb_var.get(), diabetic_var.get(), cholesterol_var.get(), systolic_bp_var.get(), diastolic_bp_var.get(), bmi_var.get(), heart_rate_var.get(), glucose_var.get()] + [var.get() for var in float_vars]), start=1):
        values.append(value)


    # Print the list of values
    print("Values:", values)
    #creating list of user entered details
    input_data=[]
    if values[0] == 'Male':
        input_data = [1] + [1 if var == 'Yes' else 0 if var == 'No' else var for var in values[1:]]
        print(input_data)
    else:
        input_data = [0] + [1 if var == 'Yes' else 0 if var == 'No' else var for var in values[1:]]
        print(input_data)


    print(input_data)
    #changing datatype of inputed data
    input_data = np.array([input_data],dtype=object)
    print(input_data)

    #sending user data to ml model

    prediction = predict(input_data)
    print("Prediction:", prediction)

    #showing result to display
    if(prediction[0]== 1):
        result_label = tk.Label(frame, text="Based on our health analysis, there is a high probability that you may develop a cardiac disease within the next decade.", font=("Arial", 18), bg="white", fg="#333")
        result_label.pack()
    else:
        result_label = tk.Label(frame,text="Based on our health analysis, it appears unlikely that you will develop any diseases in the next decade.", font=("Arial", 18), bg="white", fg="#333")
        result_label.pack()

    #Showing Tips to enhnance health

    re_label = tk.Label(frame,
                            text="Tips to improve your health.",
                            font=("Arial", 22), bg="white", fg="#333")
    re_label.pack()
    if(values[8]>180):
        chol_label=tk.Label(frame,text="Your cholesterol is high than usuasl. you can practice following to normalize it.",font=("Arial", 18), bg="white", fg="#333")
        chol_label.pack()
        cholt_label=tk.Label(frame,text="1. Healthy Diet: Focus on eating a diet rich in fruits, vegetables, whole grains, lean proteins, and healthy fats. \n2. Regular Exercise: Aim for at least 150 minutes of moderate-intensity aerobic exercise or 75 minutes of \nvigorous-intensity exercise per week.\nMedication: In some cases, lifestyle changes alone may not be enough to control cholesterol levels, and medication may\n be necessary.",font=("Arial", 18), bg="white", fg="#333")
        cholt_label.pack()
    if(values[9]>120 or values[10]>80):
        BP_label=tk.Label(frame,text="Your Blood Pressure is not in the recommanded range. you can practice the following to normalize it.",font=("Arial", 18), bg="white", fg="#333")
        BP_label.pack()
        BPt_label=tk.Label(frame,text="1.Eat a healthy diet, low in sodium.\n2.Maintain a healthy weight.\n3.Attend regular check-ups with your healthcare provider.",font=("Arial", 18), bg="white", fg="#333")
        BPt_label.pack()
    if(values[12]>100 or values[12]<60):
        HR_label = tk.Label(frame,
            text="Your Heart Rate is not in the recommanded range. you can practice the following to normalize it.",font=("Arial", 18), bg="white", fg="#333")
        HR_label.pack()
        HRt_label=tk.Label(frame,text="1.Limit Caffeine and Alcohol: Reduce consumption of caffeine and alcohol, as they can temporarily elevate heart rate.\n2.Manage Stress: Practice stress-reduction techniques such as deep breathing, meditation, yoga, or\nengaging in hobbies and activities you enjoy to help lower heart rate.\n3.Stay Hydrated: Dehydration can lead to an increased heart rate. Drink plenty of water throughout the day to stay hydrated.",font=("Arial", 18), bg="white", fg="#333")
        HRt_label.pack()
    if(values[13]>100 or values[13]<70):
        glu_label=tk.Label(frame,text="yor Glucose level in not in recommanded limit. You can practice following to normalize it.",font=("Arial", 18), bg="white", fg="#333")
        glu_label.pack()
        glut_label=tk.Label(frame,text="1.Medication Adherence: Take prescribed diabetes medications as directed by your healthcare provider.\n2.Monitor Blood Glucose: Check blood sugar levels regularly using a glucose meter or continuous glucose monitoring system.",font=("Arial", 18), bg="white", fg="#333")
        glut_label.pack()


# Create the main window
root = tk.Tk()
root.title("Cardiac Disease Prediction")



# Maximize the window
root.state("zoomed")  # For Windows
# root.attributes("-fullscreen", True)  # For macOS

# Load the background image
background_image = tk.PhotoImage(file="image.png")  # Replace "image.png" with the path to your image
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create a frame to contain the other elements
frame = tk.Frame(root, bg="white", bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.8, anchor="n")

# Create and place the heading label
heading_label = tk.Label(frame, text="CARE BOT", font=("Arial", 34), bg="white", fg="#333")
heading_label.grid(row=0, column=0, columnspan=2, pady=20)  # Add some padding at the top and bottom

# Create and place the entry widgets for health data
labels = ["Sex", "Age", "Current smoker", "Cigarettes per day", "Are you on BP Medication",
          "Prevalent Stroke", "Prevalent hypertension", "Are you Diabetic", "Cholesterol", "Systolic BP", "Diastolic BP",
          "BMI", "Heart Rate", "Glucose"]

#setting default values of variables
entries = []
float_vars = []
sex_var = tk.StringVar(value="")  # Default value is ""
age_var = tk.DoubleVar(value=0)  # Default value is 0
smoker_var = tk.StringVar(value="")  # Default value is ""
cigarettes_var = tk.DoubleVar(value=0)  # Variable for cigarettes per day
bp_medication_var = tk.StringVar(value="")  # Default value is ""
preva_var = tk.StringVar(value="")  # Default value is ""
pb_var = tk.StringVar(value="")  # Default value is ""
diabetic_var = tk.StringVar(value="")  # Default value is ""
cholesterol_var = tk.DoubleVar(value=0)  # Variable for cholesterol
systolic_bp_var = tk.DoubleVar(value=0)  # Variable for systolic blood pressure
diastolic_bp_var = tk.DoubleVar(value=0)  # Variable for diastolic blood pressure
bmi_var = tk.DoubleVar(value=0)  # Variable for BMI
heart_rate_var = tk.DoubleVar(value=0)  # Default value is 0
glucose_var = tk.DoubleVar(value=0)  # Variable for glucose

#displaying dropdown menu and textbox
#taking values from user
for i, label_text in enumerate(labels, start=1):
    if i == 1:  # For "Sex"
        label = tk.Label(frame, text=f"{i}. {label_text}:", font=("Arial", 14), bg="white", fg="#333", anchor="w")
        label.grid(row=i, column=0, sticky="w", padx=(10, 5), pady=5)
        sex_dropdown = ttk.Combobox(frame, textvariable=sex_var, values=["Male", "Female"], font=("Arial", 14))
        sex_dropdown.grid(row=i, column=1, sticky="ew", padx=(0, 10), pady=5)
    elif i == 3 or i == 5 or i == 6 or i == 7 or i == 8:  # For "Current smoker", "BP Medication", "Preva", "PB", and "Diabetic"
        label = tk.Label(frame, text=f"{i}. {label_text}:", font=("Arial", 14), bg="white", fg="#333", anchor="w")
        label.grid(row=i, column=0, sticky="w", padx=(10, 5), pady=5)
        option_values = ["Yes", "No"]
        option_var = diabetic_var if i == 8 else (pb_var if i == 7 else (preva_var if i == 6 else (bp_medication_var if i == 5 else smoker_var)))
        dropdown = ttk.Combobox(frame, textvariable=option_var, values=option_values, font=("Arial", 14))
        dropdown.grid(row=i, column=1, sticky="ew", padx=(0, 10), pady=5)
    else:
        label = tk.Label(frame, text=f"{i}. {label_text}:", font=("Arial", 14), bg="white", fg="#333", anchor="w")
        label.grid(row=i, column=0, sticky="w", padx=(10, 5), pady=5)
        entry_bg = tk.Label(frame, bg="white", bd=0)  # Background label
        entry_bg.grid(row=i, column=1, sticky="ew", padx=(0, 10), pady=5)
        if i == 2:  # For "Age"
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=age_var)
        elif i == 4:  # For "Cigarettes per day"
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=cigarettes_var)
        elif i == 9:  # For "Cigarettes per day"
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=cholesterol_var)
        elif i == 10:  # For "Cigarettes per day"
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=systolic_bp_var)
        elif i == 11:  # For "Cigarettes per day"
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=diastolic_bp_var)
        elif i == 12:  # For "Cigarettes per day"
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=bmi_var)
        elif i == 13:  # For "Heart Rate"
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=heart_rate_var)
        elif i == 14:  # For "Cigarettes per day"
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=glucose_var)
        else:
            float_var = tk.DoubleVar()  # Float variable
            float_vars.append(float_var)
            entry = ttk.Entry(entry_bg, font=("Arial", 14), style="Custom.TEntry", textvariable=float_var)
            entries.append(entry)
        entry.pack(fill="both", expand=True)

# Create and place the "SUBMIT" button
submit_button = tk.Button(root, text="SUBMIT", command=submit_action, bg="#4CAF50", fg="white", font=("Arial", 14),
                          relief="flat", pady=10)
submit_button.place(relx=0.5, rely=0.9, anchor="s")

# Create custom style for entry widgets
style = ttk.Style()
style.configure("Custom.TEntry", foreground="#333", borderwidth=0, focuscolor="#4CAF50")

# Start the main event loop
root.mainloop()
