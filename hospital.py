import re
import tkinter as tk
from tkinter import messagebox, ttk


class HospitalManagementSystem(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Hospital Management System - HCI Prototype")
        self.geometry("950x700")
        self.configure(bg="#f0f4f8")

        # In-Memory Data Stores
        self.patients = {}  # {patient_id: {name, age, gender, phone, address}}
        self.appointments = []  # [{patient_id, doctor, date, time}]
        self.doctors = ["Dr. Smith (Cardiology)", "Dr. Adams (Pediatrics)", "Dr. Taylor (General Medicine)"]
        self.time_slots = ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "03:30 PM"]

        # Apply Consistent Visual Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background="#f0f4f8")
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[10, 5])
        self.style.configure("TFrame", background="#ffffff")
        self.style.configure("Header.TLabel", font=("Helvetica", 13, "bold"), background="#ffffff", foreground="#1a365d")
        self.style.configure("TLabel", font=("Helvetica", 10), background="#ffffff")
        self.style.configure("TButton", font=("Helvetica", 10, "bold"), background="#2b6cb0", foreground="#ffffff")
        self.style.map("TButton", background=[("active", "#2c5282")])

        # Main Navigation Tabs (Initially Hidden Until Login)
        self.notebook = ttk.Notebook(self)

        self.create_login_tab()
        self.create_patient_registration_tab()
        self.create_appointment_booking_tab()
        self.create_doctor_dashboard_tab()
        self.create_billing_tab()

        # Display Login Screen First
        self.show_login_screen()

    # ==========================================
    # SCREEN 1: LOGIN PAGE
    # ==========================================
    def create_login_tab(self):
        self.tab_login = ttk.Frame(self.notebook, padding=40)
        self.notebook.add(self.tab_login, text="Login")

        ttk.Label(self.tab_login, text="Hospital Management System - Login", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self.tab_login, text="Username:").grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.login_user = ttk.Entry(self.tab_login, width=25)
        self.login_user.grid(row=1, column=1, sticky="w", pady=8)
        self.login_user.insert(0, "admin")

        ttk.Label(self.tab_login, text="Password:").grid(row=2, column=0, sticky="e", pady=8, padx=5)
        self.login_pass = ttk.Entry(self.tab_login, show="*", width=25)
        self.login_pass.grid(row=2, column=1, sticky="w", pady=8)
        self.login_pass.insert(0, "password")

        ttk.Label(self.tab_login, text="Role:").grid(row=3, column=0, sticky="e", pady=8, padx=5)
        self.login_role = ttk.Combobox(self.tab_login, values=["Receptionist", "Doctor", "Admin"], state="readonly", width=23)
        self.login_role.grid(row=3, column=1, sticky="w", pady=8)
        self.login_role.current(0)

        ttk.Button(self.tab_login, text="Login to System", command=self.handle_login).grid(row=4, column=0, columnspan=2, pady=20)

    def show_login_screen(self):
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

    def handle_login(self):
        user = self.login_user.get().strip()
        pwd = self.login_pass.get().strip()

        if user and pwd:
            messagebox.showinfo("Login Success", f"Welcome, {user}! Authenticated as {self.login_role.get()}.")
            # Select Patient Registration tab after successful login
            self.notebook.select(1)
        else:
            messagebox.showerror("Login Error", "Please provide a valid username and password.")

    # ==========================================
    # PART 1 / SCREEN 2: PATIENT REGISTRATION
    # ==========================================
    def create_patient_registration_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Patient Registration")

        ttk.Label(tab, text="Register New Patient", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        fields = [
            ("Patient ID:", "entry_id"),
            ("Full Name:", "entry_name"),
            ("Age:", "entry_age"),
            ("Gender:", "combo_gender"),
            ("Phone Number:", "entry_phone"),
            ("Address:", "entry_address")
        ]

        self.reg_widgets = {}

        for i, (label_text, var_name) in enumerate(fields, start=1):
            ttk.Label(tab, text=label_text).grid(row=i, column=0, sticky="w", pady=6, padx=5)

            if var_name == "combo_gender":
                widget = ttk.Combobox(tab, values=["Male", "Female", "Other"], state="readonly", width=28)
            else:
                widget = ttk.Entry(tab, width=30)

            widget.grid(row=i, column=1, sticky="w", pady=6, padx=5)
            self.reg_widgets[var_name] = widget

        btn_frame = ttk.Frame(tab)
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=15, sticky="w")

        ttk.Button(btn_frame, text="Register Patient", command=self.register_patient).pack(side="left", padx=(0, 10))
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_registration_form).pack(side="left")

    def register_patient(self):
        p_id = self.reg_widgets["entry_id"].get().strip()
        name = self.reg_widgets["entry_name"].get().strip()
        age = self.reg_widgets["entry_age"].get().strip()
        gender = self.reg_widgets["combo_gender"].get()
        phone = self.reg_widgets["entry_phone"].get().strip()
        address = self.reg_widgets["entry_address"].get().strip()

        if not all([p_id, name, age, gender, phone, address]):
            messagebox.showerror("Validation Error", "All fields are required. Please fill in all details.")
            return

        if p_id in self.patients:
            messagebox.showerror("Validation Error", f"Patient ID '{p_id}' already exists.")
            return

        if not age.isdigit() or int(age) <= 0 or int(age) > 120:
            messagebox.showerror("Validation Error", "Please enter a valid age (1-120).")
            return

        if not re.match(r"^\+?\d{8,15}$", phone):
            messagebox.showerror("Validation Error", "Please enter a valid phone number (8-15 digits).")
            return

        self.patients[p_id] = {
            "name": name,
            "age": age,
            "gender": gender,
            "phone": phone,
            "address": address
        }

        messagebox.showinfo("Success", f"Patient '{name}' (ID: {p_id}) registered successfully!")
        self.clear_registration_form()
        self.update_patient_dropdowns()

    def clear_registration_form(self):
        for widget in self.reg_widgets.values():
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(0, tk.END)

    # ==========================================
    # PART 2 / SCREEN 3: APPOINTMENT BOOKING
    # ==========================================
    def create_appointment_booking_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Appointment Booking")

        ttk.Label(tab, text="Book Doctor Appointment", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        ttk.Label(tab, text="Select Patient:").grid(row=1, column=0, sticky="w", pady=6)
        self.combo_booking_patient = ttk.Combobox(tab, state="readonly", width=38)
        self.combo_booking_patient.grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(tab, text="Select Doctor:").grid(row=2, column=0, sticky="w", pady=6)
        self.combo_doctor = ttk.Combobox(tab, values=self.doctors, state="readonly", width=38)
        self.combo_doctor.grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(tab, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", pady=6)
        self.entry_date = ttk.Entry(tab, width=40)
        self.entry_date.grid(row=3, column=1, sticky="w", pady=6)
        self.entry_date.insert(0, "2026-10-05")

        ttk.Label(tab, text="Available Time Slots:").grid(row=4, column=0, sticky="w", pady=6)
        self.combo_slot = ttk.Combobox(tab, values=self.time_slots, state="readonly", width=38)
        self.combo_slot.grid(row=4, column=1, sticky="w", pady=6)

        ttk.Button(tab, text="Book Appointment", command=self.confirm_booking).grid(row=5, column=0, columnspan=2, pady=20, sticky="w")

    def update_patient_dropdowns(self):
        patient_options = [f"{p_id} - {data['name']}" for p_id, data in self.patients.items()]
        self.combo_booking_patient["values"] = patient_options
        self.combo_billing_patient["values"] = patient_options

    def confirm_booking(self):
        patient_str = self.combo_booking_patient.get()
        doctor = self.combo_doctor.get()
        date = self.entry_date.get().strip()
        slot = self.combo_slot.get()

        if not all([patient_str, doctor, date, slot]):
            messagebox.showerror("Error", "Please complete all fields to book an appointment.")
            return

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")
            return

        patient_id = patient_str.split(" - ")[0]

        confirm = messagebox.askyesno(
            "Confirm Appointment",
            f"Please review booking details:\n\n"
            f"Patient: {patient_str}\n"
            f"Doctor: {doctor}\n"
            f"Date: {date}\n"
            f"Time Slot: {slot}\n\n"
            f"Confirm this booking?"
        )

        if confirm:
            self.appointments.append({
                "patient_id": patient_id,
                "doctor": doctor,
                "date": date,
                "time": slot
            })
            messagebox.showinfo("Confirmed", "Appointment successfully booked!")
            self.refresh_doctor_dashboard()

    # ==========================================
    # PART 3 / SCREEN 4: DOCTOR DASHBOARD
    # ==========================================
    def create_doctor_dashboard_tab(self):
        tab = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(tab, text="Doctor Dashboard")

        top_frame = ttk.Frame(tab)
        top_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(top_frame, text="Active Doctor Dashboard: ", font=("Helvetica", 11, "bold")).pack(side="left")
        self.dash_doc_select = ttk.Combobox(top_frame, values=self.doctors, state="readonly", width=35)
        self.dash_doc_select.pack(side="left", padx=5)
        if self.doctors:
            self.dash_doc_select.current(0)
        self.dash_doc_select.bind("<<ComboboxSelected>>", lambda e: self.refresh_doctor_dashboard())

        main_dash = ttk.Frame(tab)
        main_dash.pack(fill="both", expand=True)

        left_frame = ttk.LabelFrame(main_dash, text=" Today's Appointments ", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.tree_appointments = ttk.Treeview(left_frame, columns=("ID", "Name", "Time"), show="headings", height=8)
        self.tree_appointments.heading("ID", text="Patient ID")
        self.tree_appointments.heading("Name", text="Name")
        self.tree_appointments.heading("Time", text="Time Slot")
        self.tree_appointments.column("ID", width=70)
        self.tree_appointments.column("Name", width=120)
        self.tree_appointments.column("Time", width=80)
        self.tree_appointments.pack(fill="both", expand=True)
        self.tree_appointments.bind("<<TreeviewSelect>>", self.on_select_patient_appointment)

        right_frame = ttk.LabelFrame(main_dash, text=" Patient Records & Diagnosis ", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.lbl_patient_info = ttk.Label(right_frame, text="Select a patient from the list to view records.", font=("Helvetica", 9, "italic"))
        self.lbl_patient_info.pack(anchor="w", pady=(0, 10))

        ttk.Label(right_frame, text="Diagnosis:").pack(anchor="w")
        self.txt_diagnosis = tk.Text(right_frame, height=3, width=40, font=("Helvetica", 9))
        self.txt_diagnosis.pack(fill="x", pady=(0, 10))

        ttk.Label(right_frame, text="Prescription:").pack(anchor="w")
        self.txt_prescription = tk.Text(right_frame, height=3, width=40, font=("Helvetica", 9))
        self.txt_prescription.pack(fill="x", pady=(0, 10))

        quick_action_frame = ttk.Frame(right_frame)
        quick_action_frame.pack(fill="x")

        ttk.Button(quick_action_frame, text="View Lab Results", command=self.view_lab_results).pack(side="left", padx=(0, 5))
        ttk.Button(quick_action_frame, text="Save Clinical Entry", command=self.save_clinical_entry).pack(side="left")

    def refresh_doctor_dashboard(self):
        for item in self.tree_appointments.get_children():
            self.tree_appointments.delete(item)

        selected_doc = self.dash_doc_select.get()

        for app in self.appointments:
            if app["doctor"] == selected_doc:
                p_id = app["patient_id"]
                p_name = self.patients.get(p_id, {}).get("name", "Unknown")
                self.tree_appointments.insert("", "end", values=(p_id, p_name, app["time"]))

    def on_select_patient_appointment(self, event):
        selected_item = self.tree_appointments.selection()
        if not selected_item:
            return

        values = self.tree_appointments.item(selected_item[0], "values")
        p_id = values[0]

        if p_id in self.patients:
            p = self.patients[p_id]
            info_text = f"ID: {p_id} | Name: {p['name']} | Age: {p['age']} | Gender: {p['gender']}\nPhone: {p['phone']} | Address: {p['address']}"
            self.lbl_patient_info.config(text=info_text, font=("Helvetica", 9, "bold"))

    def view_lab_results(self):
        selected_item = self.tree_appointments.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a patient from the appointments list.")
            return

        p_id = self.tree_appointments.item(selected_item[0], "values")[0]
        lab_data = f"Lab Results for Patient ID {p_id}:\n\n- Blood Count (CBC): Normal\n- Blood Sugar (Fasting): 95 mg/dL\n- Cholesterol: 180 mg/dL"
        messagebox.showinfo("Lab Results", lab_data)

    def save_clinical_entry(self):
        selected_item = self.tree_appointments.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a patient to record diagnosis.")
            return

        p_id = self.tree_appointments.item(selected_item[0], "values")[0]
        diag = self.txt_diagnosis.get("1.0", tk.END).strip()
        presc = self.txt_prescription.get("1.0", tk.END).strip()

        if not diag or not presc:
            messagebox.showerror("Error", "Please fill in both Diagnosis and Prescription fields.")
            return

        messagebox.showinfo("Saved", f"Clinical entry recorded successfully for Patient ID {p_id}.")
        self.txt_diagnosis.delete("1.0", tk.END)
        self.txt_prescription.delete("1.0", tk.END)

    # ==========================================
    # SCREEN 5: BILLING SECTION
    # ==========================================
    def create_billing_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Billing & Invoicing")

        ttk.Label(tab, text="Patient Billing Management", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        ttk.Label(tab, text="Select Patient:").grid(row=1, column=0, sticky="w", pady=6)
        self.combo_billing_patient = ttk.Combobox(tab, state="readonly", width=38)
        self.combo_billing_patient.grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(tab, text="Consultation Fee ($):").grid(row=2, column=0, sticky="w", pady=6)
        self.entry_consult_fee = ttk.Entry(tab, width=25)
        self.entry_consult_fee.grid(row=2, column=1, sticky="w", pady=6)
        self.entry_consult_fee.insert(0, "50.00")

        ttk.Label(tab, text="Lab/Medication Fee ($):").grid(row=3, column=0, sticky="w", pady=6)
        self.entry_lab_fee = ttk.Entry(tab, width=25)
        self.entry_lab_fee.grid(row=3, column=1, sticky="w", pady=6)
        self.entry_lab_fee.insert(0, "30.00")

        ttk.Label(tab, text="Payment Method:").grid(row=4, column=0, sticky="w", pady=6)
        self.combo_payment_method = ttk.Combobox(tab, values=["Cash", "Credit/Debit Card", "Health Insurance"], state="readonly", width=23)
        self.combo_payment_method.grid(row=4, column=1, sticky="w", pady=6)
        self.combo_payment_method.current(0)

        ttk.Button(tab, text="Generate Invoice", command=self.generate_invoice).grid(row=5, column=0, columnspan=2, pady=20, sticky="w")

    def generate_invoice(self):
        patient_str = self.combo_billing_patient.get()
        consult_fee = self.entry_consult_fee.get().strip()
        lab_fee = self.entry_lab_fee.get().strip()
        pay_method = self.combo_payment_method.get()

        if not patient_str:
            messagebox.showerror("Error", "Please select a registered patient.")
            return

        try:
            c_fee = float(consult_fee)
            l_fee = float(lab_fee)
            total = c_fee + l_fee
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid numeric fee amounts.")
            return

        p_id, p_name = patient_str.split(" - ", 1)

        invoice_details = (
            f"=== OFFICIAL HOSPITAL INVOICE ===\n\n"
            f"Patient ID: {p_id}\n"
            f"Patient Name: {p_name}\n"
            f"-----------------------------------\n"
            f"Consultation Fee: ${c_fee:.2f}\n"
            f"Lab/Medicine Fee: ${l_fee:.2f}\n"
            f"-----------------------------------\n"
            f"TOTAL AMOUNT DUE: ${total:.2f}\n"
            f"Payment Method:   {pay_method}\n\n"
            f"Status: PAID / PROCESSED"
        )

        messagebox.showinfo("Invoice Generated", invoice_details)


if __name__ == "__main__":
    app = HospitalManagementSystem()
    app.mainloop()