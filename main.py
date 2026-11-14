import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from nj_halozat import NJHalozat


class NJAlkalmazas:
    def __init__(self, root):
        self.root = root
        self.halozat = NJHalozat()
        root.title('NJ Hálózati címelemző')
        root.geometry('850x640')
        root.minsize(720, 570)
        root.configure(bg='#edf2f7')
        stilus = ttk.Style(root)
        stilus.theme_use('clam')
        stilus.configure('TFrame', background='#edf2f7')
        stilus.configure('TLabel', background='#edf2f7', font=('Segoe UI', 10))
        stilus.configure('Title.TLabel', font=('Segoe UI', 22, 'bold'), foreground='#153454')
        stilus.configure('TButton', font=('Segoe UI', 10), padding=8)
        stilus.configure('Treeview', font=('Segoe UI', 10), rowheight=28)
        stilus.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        keret = ttk.Frame(root, padding=24)
        keret.pack(fill='both', expand=True)
        ttk.Label(keret, text='Hálózati címelemző', style='Title.TLabel').pack(anchor='w')
        ttk.Label(keret, text='IPv4 és IPv6 címek, hálózatok és címtartományok vizsgálata').pack(anchor='w', pady=(4, 18))
        ttk.Label(keret, text='IP-cím / prefix vagy IPv4 hálózati maszk:').pack(anchor='w')
        sor = ttk.Frame(keret)
        sor.pack(fill='x', pady=(6, 8))
        self.cim = tk.StringVar(value='192.168.1.10/24')
        self.be = ttk.Entry(sor, textvariable=self.cim, font=('Consolas', 13))
        self.be.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ttk.Button(sor, text='Elemzés', command=self.nj_futtat).pack(side='right')
        ttk.Label(keret, text='Példák: 192.168.1.10/24   •   10.0.0.5/255.255.255.0   •   2001:db8::1/64').pack(anchor='w', pady=(0, 14))
        tabla = ttk.Frame(keret)
        tabla.pack(fill='both', expand=True)
        self.lista = ttk.Treeview(tabla, columns=('adat', 'ertek'), show='headings', selectmode='browse')
        self.lista.heading('adat', text='Tulajdonság')
        self.lista.heading('ertek', text='Érték')
        self.lista.column('adat', width=225, minwidth=200)
        self.lista.column('ertek', width=500, minwidth=260)
        gorgeto = ttk.Scrollbar(tabla, orient='vertical', command=self.lista.yview)
        self.lista.configure(yscrollcommand=gorgeto.set)
        gorgeto.pack(side='right', fill='y')
        self.lista.pack(fill='both', expand=True)
        also = ttk.Frame(keret)
        also.pack(fill='x', pady=(14, 0))
        ttk.Button(also, text='JSON mentése', command=self.nj_ment).pack(side='left')
        ttk.Button(also, text='Törlés', command=self.nj_torol).pack(side='left', padx=8)
        self.allapot = tk.StringVar(value='Adj meg egy címet, majd kattints az Elemzés gombra.')
        ttk.Label(keret, textvariable=self.allapot, wraplength=740).pack(anchor='w', pady=(12, 0))
        root.bind('<Return>', self.nj_futtat)
        self.be.focus_set()

    def nj_futtat(self, event=None):
        try:
            eredmeny = self.halozat.nj_vizsgal(self.cim.get())
        except ValueError:
            self.halozat.nj_torol()
            self.lista.delete(*self.lista.get_children())
            self.allapot.set('Hibás cím. Példa a helyes formátumra: 192.168.1.10/24')
            messagebox.showerror('Érvénytelen cím', 'Adj meg érvényes IPv4 vagy IPv6 címet és prefixet!', parent=self.root)
            return
        self.lista.delete(*self.lista.get_children())
        for nev, ertek in eredmeny.items():
            self.lista.insert('', 'end', values=(nev, ertek))
        self.allapot.set('Az elemzés elkészült. Az eredmény JSON-fájlba menthető.')

    def nj_torol(self):
        self.halozat.nj_torol()
        self.lista.delete(*self.lista.get_children())
        self.cim.set('')
        self.allapot.set('Az adatok törölve.')
        self.be.focus_set()

    def nj_ment(self):
        if not self.halozat.eredmeny:
            messagebox.showinfo('Nincs eredmény', 'Előbb végezz el egy sikeres elemzést!', parent=self.root)
            return
        fajl = filedialog.asksaveasfilename(parent=self.root, title='Eredmény mentése', defaultextension='.json', filetypes=[('JSON-fájl', '*.json')], initialfile='halozati_elemzes.json')
        if not fajl:
            return
        try:
            with open(fajl, 'w', encoding='utf-8') as cel:
                json.dump(self.halozat.eredmeny, cel, ensure_ascii=False, indent=4)
        except OSError as hiba:
            messagebox.showerror('Mentési hiba', str(hiba), parent=self.root)
            return
        self.allapot.set('Az eredmény mentése sikerült.')


if __name__ == '__main__':
    root = tk.Tk()
    app = NJAlkalmazas(root)
    root.mainloop()
