import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
import pandas as pd
import json

# Datenbank und Zähler
gutscheine = {'Getränke': {}, 'Essen': {}, 'Essen / Getränke': {}}
zaehler = {'Getränke': 1, 'Essen': 1, 'Essen / Getränke': 1}
ADMIN_PASSWORT = "admin123"

# Funktionen


def logout_admin():
    admin_interface.pack_forget()
    login_button.pack(pady=10)


def speichern_gutscheine():
    with open("gutscheine.json", "w") as file:
        json.dump(gutscheine, file)

def login_admin():
    pw = simpledialog.askstring("Passwort", "Bitte Admin-Passwort eingeben:", show='*')
    if pw == ADMIN_PASSWORT:
        admin_interface.pack(pady=10)
        login_button.pack_forget()
        update_gutschein_liste()
    else:
        messagebox.showerror("Fehler", "Falsches Passwort!")


def erstelle_gutschein():
    kategorie = kategorie_combobox.get()
    try:
        anzahl = int(anzahl_entry.get())  # Anzahl der zu erstellenden Gutscheine
    except ValueError:
        messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben!")
        return

    for _ in range(anzahl):
        nummer = zaehler[kategorie]
        zaehler[kategorie] += 1
        gutscheine[kategorie][nummer] = True
    speichern_gutscheine()  # Daten speichern
    update_gutschein_liste()

def laden_gutscheine():
    global gutscheine, zaehler
    try:
        with open("gutscheine.json", "r") as file:
            daten = json.load(file)
            if "gutscheine" in daten and "zaehler" in daten:
                gutscheine = daten["gutscheine"]
                zaehler = daten["zaehler"]
            else:
                gutscheine = {"Essen": {}, "Getränke": {}, "Essen / Getränke": {}}
                zaehler = {'Getränke': 1, 'Essen': 1, 'Essen / Getränke': 1}
    except FileNotFoundError:
        gutscheine = {"Essen": {}, "Getränke": {}, "Essen / Getränke": {}}
        zaehler = {'Getränke': 1, 'Essen': 1, 'Essen / Getränke': 1}

def pruefe_gutschein():
    kategorie = kategorie_pruef_combobox.get()
    nummer = int(pruef_entry.get())
    
    
    if nummer in gutscheine[kategorie]:
        if gutscheine[kategorie][nummer]:
            gutscheine[kategorie][nummer] = False
            speichern_gutscheine()  # Daten speichern
            update_gutschein_liste()
            messagebox.showinfo("Gutschein", "Der Gutschein wurde erfolgreich eingelöst!")
        else:
            messagebox.showwarning("Gutschein", "Der Gutschein wurde bereits eingelöst!")
    else:
        messagebox.showerror("Fehler", "Gutschein nicht gefunden!")

def update_gutschein_liste(sort_kategorie=None):
    gutschein_liste.delete(*gutschein_liste.get_children())
    
    if sort_kategorie is None:
        sortierte_gutscheine = sorted(gutscheine.items(), key=lambda x: x[0], reverse=True)
    else:
        sortierte_gutscheine = sorted(gutscheine.items(), key=lambda x: sum([1 for num, status in x[1].items() if status and x[0] == sort_kategorie]), reverse=True)
    
    for kategorie, data in sortierte_gutscheine:
        for nummer, status in data.items():
            gutschein_liste.insert("", "end", values=(kategorie, nummer, "Ja" if status else "Nein"))



def deactivate_gutschein(event):
    item = gutschein_liste.selection()[0]
    kategorie, nummer, status = gutschein_liste.item(item, "values")
    if status == "Ja":
        gutscheine[kategorie][int(nummer)] = False
        speichern_gutscheine()  # Daten speichern
        update_gutschein_liste()

def export_to_excel():
    data = []
    for kategorie, gutscheindaten in gutscheine.items():
        for nummer, status in gutscheindaten.items():
            data.append([kategorie, nummer, "Ja" if status else "Nein"])

    df = pd.DataFrame(data, columns=["Kategorie", "Nummer", "Gültig"])
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    
    if save_path:
        df.to_excel(save_path, index=False)
        messagebox.showinfo("Erfolg", "Daten erfolgreich nach Excel exportiert!")



def loesche_alle_gutscheine():
    response = messagebox.askyesno("Bestätigung", "Möchten Sie wirklich alle Gutscheine löschen?")
    if response:
        global gutscheine
        print("Vor dem Löschen:", gutscheine)  # Debug-Ausgabe
        gutscheine = {'Getränke': {}, 'Essen': {}, 'Essen / Getränke': {}}
        
        # Zähler zurücksetzen
        zaehler['Getränke'] = 1
        zaehler['Essen'] = 1
        zaehler['Essen / Getränke'] = 1
        
        print("Nach dem Löschen:", gutscheine)  # Debug-Ausgabe
        speichern_gutscheine()
        update_gutschein_liste()


def speichern_gutscheine():
    daten = {
        "gutscheine": gutscheine,
        "zaehler": zaehler
    }
    try:
        with open("gutscheine.json", "w") as file:
            json.dump(daten, file)
    except Exception as e:
        messagebox.showerror("Fehler", f"Es gab einen Fehler beim Speichern: {e}")

# GUI
root = tk.Tk()
root.title("Gutschein-System")
laden_gutscheine()

login_button = tk.Button(root, text="Admin Login", command=login_admin)
login_button.pack(pady=10)

admin_interface = tk.Frame(root)

kategorie_label = tk.Label(admin_interface, text="Kategorie auswählen:")
kategorie_label.pack()

kategorie_combobox = ttk.Combobox(admin_interface, values=["Getränke", "Essen", "Essen / Getränke"])
kategorie_combobox.pack()
kategorie_combobox.set("Getränke")

anzahl_label = tk.Label(admin_interface, text="Anzahl der Gutscheine:")
anzahl_label.pack()

anzahl_entry = tk.Entry(admin_interface)
anzahl_entry.pack()

erstelle_button = tk.Button(admin_interface, text="Gutschein erstellen", command=erstelle_gutschein)
erstelle_button.pack(pady=10)

# Restlicher Code bleibt unverändert ...




def erstelle_gutschein():
    kategorie = kategorie_combobox.get()
    try:
        anzahl = int(anzahl_entry.get())  # Anzahl der zu erstellenden Gutscheine
    except ValueError:
        messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben!")
        return

    for _ in range(anzahl):
        nummer = zaehler[kategorie]
        zaehler[kategorie] += 1
        gutscheine[kategorie][nummer] = True

    speichern_gutscheine()  # Daten speichern
    update_gutschein_liste()


#erstelle_button = tk.Button(admin_interface, text="Gutschein erstellen", command=erstelle_gutschein)
#erstelle_button.pack(pady=10)

sortieren_button = ttk.Combobox(admin_interface, values=["Getränke", "Essen", "Essen / Getränke"])
sortieren_button.pack(pady=10)
sortieren_button.set("Sortieren nach...")
sortieren_button.bind("<<ComboboxSelected>>", lambda e: update_gutschein_liste(sort_kategorie=sortieren_button.get()))

gutschein_liste = ttk.Treeview(admin_interface, columns=("Kategorie", "Nummer", "Gültig"))
gutschein_liste.heading("Kategorie", text="Kategorie")
gutschein_liste.heading("Nummer", text="Nummer")
gutschein_liste.heading("Gültig", text="Gültig")
gutschein_liste.bind("<Double-1>", deactivate_gutschein)
gutschein_liste.pack(pady=10)

export_button = tk.Button(admin_interface, text="Exportieren nach Excel", command=export_to_excel)
export_button.pack(pady=10)

logout_button = tk.Button(admin_interface, text="Logout", command=logout_admin)
logout_button.pack(pady=10)

loeschen_button = tk.Button(admin_interface, text="Alle Gutscheine löschen", command=loesche_alle_gutscheine)
loeschen_button.pack(pady=10)

benutzer_label = tk.Label(root, text="Benutzer-Bereich")
benutzer_label.pack(pady=10)

kategorie_pruef_label = tk.Label(root, text="Kategorie auswählen:")
kategorie_pruef_label.pack()

kategorie_pruef_combobox = ttk.Combobox(root, values=["Getränke", "Essen", "Essen / Getränke"])
kategorie_pruef_combobox.pack()
kategorie_pruef_combobox.set("Getränke")

pruef_label = tk.Label(root, text="Gutscheinnummer eingeben:")
pruef_label.pack()

pruef_entry = tk.Entry(root)
pruef_entry.pack()

pruef_button = tk.Button(root, text="Gutschein prüfen", command=pruefe_gutschein)
pruef_button.pack(pady=10)

root.mainloop()
