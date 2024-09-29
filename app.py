import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

quiz = [
    
      


    {
        "tipo": "multiple_choice",
        "domanda": "La formula = $B$6 + C20 contiene:",
        "opzioni": ["due riferimenti misti", "un riferimento assoluto e un riferimento relativo", "due riferimenti assoluti", "due riferimenti relativi ed un riferimento assoluto"],
        "risposta_corretta": "un riferimento assoluto e un riferimento relativo"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Come si crea una copia del foglio di lavoro 'distribuzione' e si mette come ultimo foglio della cartella attiva?",
        "opzioni": ["Click su copia il foglio e incolla come ultimo", "Clic sul foglio e poi sposta o copia e metti come ultimo foglio", "Duplica il foglio e sposta come ultimo", "Aggiungi un nuovo foglio e incolla il contenuto"],
        "risposta_corretta": "Clic sul foglio e poi sposta o copia e metti come ultimo foglio",
        "gif": "spostacopia.gif"
    },
  
    {
        "tipo": "multiple_choice",
        "domanda": "Come si inserisce una colonna prima della colonna G.",
        "opzioni": ["Vai su gruppo celle scheda home e seleziona colonna G e poi clicca 'Inserisci Colonna'", "Vai nel gruppo formato e seleziona colonna G e clicca 'Aggiungi Colonna'", "Seleziona colonna F e clicca 'Inserisci Colonna'", "Seleziona colonna D e clicca 'Aggiungi Colonna'"],
        "risposta_corretta": "Vai su gruppo celle scheda home e seleziona colonna G e poi clicca 'Inserisci Colonna'",
        "gif": "inseriscicolonna.gif"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Come si mette in ordine crescente sulla base dei valori della colonna 'Fatturato' i dati di una tabella selezionata.",
        "opzioni": ["Scheda Visualizza - gruppo celle Ordina dalla A alla Z", "Scheda Home - gruppo Modifica poi ordinamento personalizzato - dalla A alla Z", "Scheda Ordina dal minore al maggiore", "Ordina dalla Z alla A"],
        "risposta_corretta": "Scheda Home - gruppo Modifica poi ordinamento personalizzato - dalla A alla Z",
        "gif": "ordinamentopersonalizzato.gif"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Parlando di fogli di lavoro, quali delle seguenti affermazioni sono corrette?",
        "opzioni": ["in una cella conviene inserire sia il nome che il cognome di una persona", "in una cella conviene inserire solo il nome o solo il cognome di una persona", "ogni cella può contenere più dati omogenei", "ogni cella dovrebbe sempre contenere un solo dato"],
        "risposta_corretta": "ogni cella dovrebbe sempre contenere un solo dato"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Allinea al centro, orizzontalmente, il contenuto della cella selezionata.",
        "opzioni": ["Seleziona cella e clicca 'Centro' nel gruppo allineamento della scheda Home", "Seleziona cella e clicca 'Centro' nel gruppo Zoom della scheda Visualizza", "Seleziona cella e clicca 'Centro' nella scheda Inserisci", "Seleziona cella e clicca 'Centro' nella scheda Layout di pagina."],
        "risposta_corretta": "Seleziona cella e clicca 'Centro' nel gruppo allineamento della scheda Home",
        "gif": "centroeorizz.gif"
        
    },
    {
        "tipo": "excel",
        "domanda": "Inserisci la funzione che scrive il testo 'critico' se il contenuto della cella C15 è minore di '1000' e 'buono' altrimenti.",
        "risposte_possibili": ["=SE(C15<1000;\"critico\";\"buono\")"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Come si sposta un contenuto già selezionato da un foglio di lavoro ad un altro? a partire dalla cella D6.",
        "opzioni": ["Taglia e incolla su Foglio 1 in D6", "Copia e incolla su Foglio 1 in D6", "Sposta e incolla su Foglio 1 in D6", "Duplica e incolla su Foglio 1 in D6"],
        "risposta_corretta": "Taglia e incolla su Foglio 1 in D6",
        "gif": "SPOSTACELLE.gif"
        
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Inserisci nell'intestazione il testo 'aggiornamento' posizionandolo al centro. Al termine premere invio.",
        "opzioni": ["Vai su 'Formato', poi 'Intestazione', poi 'Centro'", "Vai su Visualizza - Imposta Pagina - 'Intestazione', personalizza intestazione  poi 'aggiornamento'", "Vai su scheda inserisci poi Intestazione e piè di pagina ed al centro inserisci il testo aggiornamento'", "Vai su 'Home', poi 'Intestazione', poi 'Centro'"],
        "risposta_corretta": "Vai su scheda inserisci poi Intestazione e piè di pagina ed al centro inserisci il testo aggiornamento'",
        "gif": "intestazione.gif"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Formatta il contenuto delle celle selezionate in modo da visualizzare il separatore delle migliaia e una cifra decimale.",
        "opzioni": ["Vai su 'Formato Celle', poi 'Numero'", "Vai su 'Home', poi 'Numero'", "Vai su 'Gruppo numeri' Metti il separatore delle migliaia e poi togli un decimale con gli appositi pulsanti'", "Vai su 'Visualizza', poi 'Numero'"],
        "risposta_corretta": "Vai su 'Gruppo numeri' Metti il separatore delle migliaia e poi togli un decimale con gli appositi pulsanti'",
        "gif": "migliaiadec.gif"
    },
    {
        "tipo": "excel",
        "domanda": "Senza utilizzare la barra multifunzione, inserisci la formula che calcola la differenza tra il contenuto delle celle E2 ed E11.",
        "risposte_possibili": ["=E2-E11" , "=(E2-E11)"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Quale regola occorre seguire nell'attribuzione dei nomi ai fogli di lavoro?",
        "opzioni": ["assegnare nomi composti da una sola parola senza spazi bianchi", "assegnare nomi composti da codici numerici per poterli utilizzare nelle formule", "lasciare sempre i nomi predefiniti per sicurezza", "assegnare nomi significativi invece di accettare il nome predefinito"],
        "risposta_corretta": "assegnare nomi significativi invece di accettare il nome predefinito"
    },
    {
        "tipo": "excel",
        "domanda": "Inserisci la funzione che scrive il testo 'dividendo ok' se il contenuto della cella B33 è maggiore di '300' e 'non pagabili' altrimenti.",
        "risposte_possibili": ["=SE(B33>300;\"dividendo ok\";\"non pagabili\")"]
    },
    {
        "tipo": "excel",
        "domanda": "Utilizza la funzione MEDIA per inserire la formula che calcola il valore medio contenuto nell'intervallo B5:D13.",
        "risposte_possibili": ["=MEDIA(B5:D13)"]
    },
    {
        "tipo": "excel",
        "domanda": "Inserisci la formula che calcola, senza l'uso delle funzioni, la somma del contenuto della cella C8 e quello della cella D8.",
        "risposte_possibili": ["=C8+D8" , "=(C8+D8)"]
    },
    {
        "tipo": "excel",
        "domanda": "Senza l'uso della barra multifunzione e utilizzando esclusivamente gli operatori aritmetici, inserisci la formula che calcola la somma dei contenuti delle celle C3 e C4.",
        "risposte_possibili": ["=C3+C4" , "=(C3+C4)"]
    },
    {
        "tipo": "excel",
        "domanda": "Usando la funzione CONTA.NUMERI inserisci una formula che conta quanti numeri sono presenti nell'intervallo C3:P10",
        "risposte_possibili": ["=CONTA.NUMERI(C3:P10)"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Se la struttura della tabella non è corretta ed è necessario inserire una riga vuota in un punto preciso, dove dovresti inserire la riga?",
        "opzioni": ["Inserisci riga prima dei totali", "Inserisci riga dopo i totali", "Inserisci riga al centro della tabella", "Inserisci riga all'inizio della tabella"],
        "risposta_corretta": "Inserisci riga prima dei totali",
        "gif": "inserisciriga.gif"
        
    },
    {
        "tipo": "excel",
        "domanda": "Senza l'uso della barra multifunzione e utilizzando esclusivamente gli operatori aritmetici inserisci una formula che calcola la somma dei contenuti delle celle B2 e C5 meno il valore contenuto nella cella B7",
        "risposte_possibili": ["=B2+C5-B7" , "=C5+B2-B7" , "=(B2+C5)-B7"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "come si stampano sei copie di sole celle selezionate.",
        "opzioni": ["File - Stampa - scelgo 6 copie e stampo", "Stampo sei copie dell'intero foglio", "File - Stampa - Stampa selezione e poi metto 6 copie", "Stampa sei copie della prima pagina"],
        "risposta_corretta": "File - Stampa - Stampa selezione e poi metto 6 copie",
        "gif": "stampaselezione.gif"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Se devi salvare il file Excel visualizzato nella cartella C:\\lavoro cambiando il tipo di formato dati in 'dati XML' e lasciando lo stesso nome.",
        "opzioni": ["File - Salva con nome - salvo come dati XML in C:\\lavoro", "File - Salve e salvo come dati XML in C:\\lavoro", "Salvo con barra di accesso rapido dati XML in C:\\lavoro", "Salva come dati PDF in C:\\lavoro"],
        "risposta_corretta": "File - Salva con nome - salvo come dati XML in C:\\lavoro",
        "gif": "SalvaXML.gif"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Salva il file Excel visualizzato nella cartella C:\\lavoro assegnandogli il nome 'nuovoReport'.",
        "opzioni": ["Salva con nome 'nuovoReport' in C:\\lavoro", "Salva con nome 'nuovoFile' in C:\\lavoro", "Salva con nome 'nuovaCartella' in C:\\lavoro", "Salva con nome 'nuovoDocumento' in C:\\lavoro"],
        "risposta_corretta": "Salva con nome 'nuovoReport' in C:\\lavoro",
        "gif": "Nuovoreport.gif"
        
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Fai in modo che i titoli presenti nella riga 2 siano sempre riportati su ogni pagina stampata.",
        "opzioni": ["Inserisci riga - imposta riga 2 come intestazione di stampa", "Scheda Layout di pagina - gruppo imposta pagina - comando stampa titoli e poi si seleziona la riga 2", "Imposta riga 2 come intestazione a piè di pagina", "Imposta riga 2 come intestazione laterale"],
        "risposta_corretta": "Scheda Layout di pagina - gruppo imposta pagina - comando stampa titoli e poi si seleziona la riga 2",
        "gif": "righe.gif"
    },
    {
        "tipo": "excel",
        "domanda": "Usando la funzione ARROTONDA inserisci una formula che arrotonda il contenuto della cella B4 a zero cifre decimali",
        "risposte_possibili": ["=ARROTONDA(B4;0)"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Come si elimina la visualizzazione della griglia e delle intersezioni di riga e di colonna impostate per quando si stamperà il foglio di lavoro.",
        "opzioni": ["Disattiva la visualizzazione della griglia in 'Imposta Pagina'", "Disattiva la visualizzazione della griglia in 'Visualizza'", "Disattiva la visualizzazione della griglia in 'Home'", "Disattiva la visualizzazione della griglia in 'Inserisci'"],
        "risposta_corretta": "Disattiva la visualizzazione della griglia in 'Imposta Pagina'",
        "gif": "griglia.gif"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Cosa succede quando la formula che contiene il riferimento $C$7 viene copiata in un'altra cella?",
        "opzioni": ["Il riferimento di cella cambia solo per la colonna, adattandosi alla nuova posizione della formula", "Il riferimento di cella cambia completamente, adattandosi alla nuova posizione della formula", "Il riferimento di cella non cambia", "Il riferimento di cella cambia solo per la riga, adattandosi alla nuova posizione della formula"],
        "risposta_corretta": "Il riferimento di cella non cambia"
    },
    {
        "tipo": "excel",
        "domanda": "Inserisci la funzione che scrive il testo 'OK' se il contenuto nella cella C17 è uguale a '11' e 'da completare' altrimenti.",
        "risposte_possibili": ["=SE(C17=11;\"OK\";\"da completare\")"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Inserisci il bordo inferiore alle celle selezionate.",
        "opzioni": ["Vai su 'Inserisci', poi 'Bordo inferiore'", "Vai su 'Home', poi 'Bordo inferiore'", "Vai su 'Formato', poi 'Bordo inferiore'", "Vai su 'Visualizza', poi 'Bordo inferiore'"],
        "risposta_corretta": "Vai su 'Home', poi 'Bordo inferiore'",
        "gif": "bordoinf.gif"
    },
    {
        "tipo": "excel",
        "domanda": "Utilizza la funzione MIN per inserire la formula che calcola il valore minimo contenuto nelle celle E5:E9.",
        "risposte_possibili": ["=MIN(E5:E9)"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Che tipo di errore produce =C5/0?",
        "opzioni": ["#DIV/0!", "#RIF!", "#NOME?", "#VALORE!"],
        "risposta_corretta": "#DIV/0!"
    },
    {
        "tipo": "excel",
        "domanda": "Senza usare la barra multifunzione e utilizzando esclusivamente gli operatori aritmetici, inserisci la formula che calcola la divisione delle celle B5 ed A7.",
        "risposte_possibili": ["=B5/A7"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Quale comando usi per fare in modo che il testo di una cella sia compreso su più righe nella stessa cella?",
        "opzioni": ["Uso il comando di allineamento al centro", "Uso il comando di UNISCI ED ALLINEA AL CENTRO", "Uso il comando di TESTO A CAPO", "Non è possibile porre su più righe il testo in una cella"],
        "risposta_corretta": "Uso il comando di TESTO A CAPO",
        "gif": "testoacapo.gif"
    },
    {
        "tipo": "excel",
        "domanda": "Usando la funzione CONTA.VALORI inserisci una formula che conta le celle non vuote nell'intervallo A1:F12",
        "risposte_possibili": ["=CONTA.VALORI(A1:F12)"]
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Utilizza l’apposito pulsante per fa apparire a sinistra nell’intestazione, il nome del file.",
        "opzioni": ["Vai su 'Inserisci', poi 'Nome File'", "Vai su 'Home', poi 'Nome File'", "'Vai su Inserisci - Intestazione e piè di pagina e si sceglie l'icona Excel nettendolo alla sinistra del foglio'", "Vai su 'Visualizza', poi 'Nome File'"],
        "risposta_corretta": "Vai su Inserisci - Intestazione e piè di pagina e si sceglie l'icona Excel nettendolo alla sinistra del foglio",
        "gif": "nomefile.gif"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Copia formato delle celle B2:B6 nella colonna immediatamente successiva a partire da C4.",
        "opzioni": ["Seleziona B2:B6, copia formato e applica a C4:C8", "Seleziona B2:B6, copia formato e applica a C4:C9", "Seleziona B2:B6, copia formato e applica a C4:C10", "Seleziona B2:B6, copia formato e applica a C4:C7"],
        "risposta_corretta": "Seleziona B2:B6, copia formato e applica a C4:C8"
    },
    {
        "tipo": "multiple_choice",
        "domanda": "Formatta il contenuto della cella selezionata in modo da avere il formato gg-mm-aaaa.",
        "opzioni": ["Vai su 'Formato Celle', poi 'Data'", "Vai su 'Home', poi 'Data'", "Vai su 'Inserisci', poi 'Data'", "Vai su impostazioni avanzate gruppo 'Numeri' e poi scegli il formato 'data'"],
        "risposta_corretta": "Vai su 'Formato Celle', poi 'Data'",
        "gif": "data.gif"
    }
]



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        risposte = request.form
        risultati = []
        
        for domanda in quiz:
            risposta_utente = risposte.get(domanda['domanda'])
            if risposta_utente == domanda['risposta_corretta'].lower():
                risultati.append({'domanda': domanda, 'risposta_corretta': True})
            else:
                risultati.append({'domanda': domanda, 'risposta_corretta': False})
        
        return render_template('risultati.html', risultati=risultati)

    return render_template('quiz.html', quiz=quiz)

if __name__ == '__main__':
    app.run(debug=True)
