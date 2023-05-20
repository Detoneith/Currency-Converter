from forex_python.converter import CurrencyRates, CurrencyCodes

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class CurrencyConverter(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        
        self.amount = ttk.DoubleVar(value='Amount')
        self.from_currency = ttk.StringVar(value='EUR')
        self.to_currency = ttk.StringVar(value='USD')
        self.converted_amount = ttk.DoubleVar(value='')        

        self.cr = CurrencyRates()
        
        # Création de la fenêtre
        self.create_form_entry("Montant à convertir", self.amount)
        self.create_option_menu("Devises de départ", self.from_currency)
        self.create_option_menu("Devises d'arrivée", self.to_currency)
        self.create_result_display("Montant converti", self.converted_amount)
        self.create_buttonbox()
        print("test")
        

    def create_form_entry(self,label, variable):
        """Create and add the widget elements"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        self.label = ttk.Label(master=container, text=label.title(), width=20)
        self.label.pack(side=LEFT, padx=5)

        self.entry = ttk.Entry(master=container, textvariable=variable)
        self.entry.pack(side=LEFT, padx=5, fill=X, expand=YES)
        #self.entry.configure(foreground="grey")

        self.entry.bind("<FocusIn>", self.on_entry_click)


    def on_entry_click(self, event):
        """Effacer le contenu de l'entrée si le texte par défaut est présent"""
        entry = event.widget
        if entry.get() == "Amount":
            entry.delete(0, "end")

    
    def create_option_menu(self, label, variable):
        """Create and add the Menubutton"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        self.label = ttk.Label(master=container, text=label.title(), width=20)
        self.label.pack(side=LEFT, padx=5)

        self.menu = ttk.OptionMenu(container, variable, self.from_currency.get(), *self.cr.get_rates(self.from_currency.get()))
        self.menu.pack(side=LEFT, padx=5)

        # options de devise dans l'OptionMenu
        for currency in self.cr.get_rates(self.from_currency.get()):
            self.menu["menu"].add_command(
                label=currency,
                command=lambda value=currency: variable.set(value)
            )
            
            
    def create_result_display(self,label, variable):
        """Create and add the widget elements"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        self.label = ttk.Label(master=container, text=label.title(), width=20)
        self.label.pack(side=LEFT, padx=5)

        self.result = ttk.Label(master=container, textvariable=variable, width=20)
        self.result.pack(side=LEFT, padx=5)

        self.currency_symbol = ttk.Label(master=container, text="", width=4)
        self.currency_symbol.pack(side=LEFT)


    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        cnv_btn = ttk.Button(
            master=container,
            text="Convertir",
            command=self.convert_currency,
            style="success.TButton",
            width=8,
        )
        cnv_btn.pack(side=LEFT, padx=5)

        cnl_btn = ttk.Button(
            master=container,
            text="Reset",
            command=self.on_reset,
            style="danger.TButton",
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

    def convert_currency(self):
        from_currency = self.from_currency.get()
        to_currency = self.to_currency.get()
        amount = self.amount.get()
        converted_amount = self.cr.convert(from_currency, to_currency, amount)
        self.converted_amount.set(round(converted_amount, 2))

        currency_codes = CurrencyCodes()
        currency_symbol = currency_codes.get_symbol(to_currency)
        self.currency_symbol.config(text=currency_symbol)

    def on_reset(self):
        """Callback for the cancel button"""
        self.amount.set('Amount')
        self.from_currency.set('EUR')
        self.to_currency.set('USD')
        self.converted_amount.set('')
        self.currency_symbol.config(text='')


if __name__ == "__main__":
    
    app = ttk.Window("CurrencyConverter", "cyborg")
    CurrencyConverter(app)
    app.mainloop()