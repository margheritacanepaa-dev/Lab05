import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore)

    input_tipo = ft.TextField( label="Tipo", width = 300)
    input_marca =  ft.TextField( label="Marca", width=300)       # il value = deposito.strumenti.marca
    input_anno = ft.TextField( label="Anno acquisto", width=300)

    # Contatore: necessita di 1 textfiled per il valore, e 2 pulsanti per incrementare/diminuire
    txt_contatore = ft.TextField( value="0", width= 50, text_align=ft.TextAlign.CENTER)
           # uso value e non label perchè voglio che si aggiorni,     text_align per avere il numero al centro



    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))


    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # HANDLERS per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # Creo funzione per gestione aggiorna strumenti
    def aggiorna_strumenti(e):
        # controllo validità dei campi
        if not input_anno.value or not input_anno.value.isdigit():
            alert.show_alert("❌ Errore: inserisci dati numerici validi per l'anno.")  # apre una finestra che mostra l'errore
            return
        if not txt_contatore.value or not txt_contatore.value.isdigit():
            alert.show_alert("❌ Errore: inserisci dati numerici validi per il valore.")   # apre una finestra che mostra l'errore
            return

        # aggiungo lo strumento al deposito (trasformo i campi numerici)
        anno = int(input_anno.value)
        valore = float(txt_contatore.value)      # è quello inserito nel contatore
        deposito.aggiungi_strumento(input_tipo.value, input_marca.value, anno, valore)   # prende i valori inseriti nei campi

        # svuoto i campi e azzero contatore
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        txt_contatore.value = "0"

        # aggiorno la lista degli strumenti mostrata a schermo
        aggiorna_lista_strumenti()
        page.update()


    # Creo funzione per incrementare il prezzo (bottone +)
    def aumenta_valore(e):
        if not txt_contatore.value or not txt_contatore.value.isdigit():   # se è vuoto o non è un numero, inizializzo a 0
            txt_contatore.value = "0"
        val_corrente = int(txt_contatore.value)        # trasformo in intero il valore del TextField per sommare
        txt_contatore.value = str(val_corrente + 1)       # rimetto come stringa per il testo
        txt_contatore.update()

    # Creo funzione per diminuire il prezzo (bottone -)
    def decrementa_valore(e):
        if not txt_contatore.value or not txt_contatore.value.isdigit():   # se è vuoto o non è un numero, inizializzo a 0
            txt_contatore.value = "0"
        val_corrente = int(txt_contatore.value)          # trasformo in intero per sommare
        if val_corrente >0:                                # faccio un controllo per non andare in negativo
            txt_contatore.value = str(val_corrente - 1)
            txt_contatore.update()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiorna_strumenti)

    # Pulsanti per il contatore, usano la fz IconButton
    pulsante_piu = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", icon_size=20, on_click= aumenta_valore)
    pulsante_meno = ft.IconButton(icon=ft.Icons.REMOVE, icon_color = "red", icon_size = 20, on_click=decrementa_valore)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),                                  # linea divisoria per separare due parti
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        # creo nuova riga per i fields
        ft.Row(spacing=30,
               # inserisco tutti i campi per questa riga
               controls=[input_tipo, input_marca, input_anno,pulsante_meno, txt_contatore, pulsante_piu],
               alignment=ft.MainAxisAlignment.CENTER),                # allineo al centro

        # aggiungo una riga per mettere il bottone aggiungi strumento
        ft.Row(spacing=200,
               controls=[pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),               # allineo al centro

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
