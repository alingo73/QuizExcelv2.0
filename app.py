from flask import Flask, render_template, request, redirect, url_for, flash, Response, session

app = Flask(__name__)
app.secret_key = 'Giorgiolone1!'

# Funzione di autenticazione base
def check_auth(username, password):
    return username == 'admin' and password == 'password'

# Decoratore per proteggere le rotte con autenticazione
def authenticate():
    return Response(
        'Autenticazione richiesta', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

# Middleware di protezione
@app.before_request
def before_request():
    session.clear()  # Cancella i cookie di sessione
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

# Definizione delle domande del quiz
quiz = [
    {
        'id': 1,
        'type': 'multiple_choice',
        'question': 'La formula = $B$6 + C20 contiene:',
        'options': ['due riferimenti misti', 'un riferimento assoluto e un riferimento relativo', 'due riferimenti assoluti', 'due riferimenti relativi ed un riferimento assoluto'],
        'correct': 'un riferimento assoluto e un riferimento relativo'
    },
    {
	'id': 2,
        "type": "multiple_choice",
        "question": "Come si inserisce una colonna prima della colonna G.",
        "options": ["Vai su gruppo celle scheda home e seleziona colonna G e poi clicca 'Inserisci Colonna'", "Vai nel gruppo formato e seleziona colonna G e clicca 'Aggiungi Colonna'", "Seleziona colonna F e clicca 'Inserisci Colonna'", "Seleziona colonna D e clicca 'Aggiungi Colonna'"],
        "correct": "Vai su gruppo celle scheda home e seleziona colonna G e poi clicca 'Inserisci Colonna'",
        
    },
    {
        'id': 3,
        'type': 'open',
        'question': 'Senza l\'uso della barra multifunzione, scrivi la formula che effettua la differenza tra il contenuto della cella A4 e quello della cella B6:',
        'correct_variants': ['=A4-B6', '=(A4-B6)', '=(a4-b6)', '=a4-b6']
    },
        {
	'id': 4,
        "type": "multiple_choice",
        "question": "Come si crea una copia del foglio di lavoro chiamato ad esempio 'distribuzione' e si mette come ultimo foglio della cartella attiva?",
        "options": ["Click su copia il foglio e incolla come ultimo", "Clic col tasto sinistro sul foglio e poi nel menu si sceglie sposta o copia e metti come ultimo foglio", "Duplica il foglio e sposta come ultimo", "Aggiungi un nuovo foglio e incolla il contenuto"],
        "correct": "Clic col tasto sinistro sul foglio e poi nel menu si sceglie sposta o copia e metti come ultimo foglio",
    },
    {
        'id': 5,
        'type': 'open',
        'question': "Inserisci la funzione che scrive il testo 'OK' se il contenuto nella cella C17 è uguale a '11' e 'da completare' altrimenti.",
        'correct_variants': ["=SE(C17=11;\"OK\";\"da completare\")"]
    },
        {
	'id':6,
        "type": "multiple_choice",
        "question": "Come si mette in ordine crescente sulla base dei valori della colonna 'Fatturato' i dati di una tabella selezionata.",
        "options": ["Scheda Visualizza - gruppo celle Ordina dalla A alla Z", "Scheda Home - gruppo Modifica poi ordinamento personalizzato - dalla A alla Z", "Scheda Ordina dal minore al maggiore", "Ordina dalla Z alla A"],
        "correct": "Scheda Home - gruppo Modifica poi ordinamento personalizzato - dalla A alla Z",
        
    },
    {
	'id':7,
        "type": "multiple_choice",
        "question": "Parlando di fogli di lavoro, quali delle seguenti affermazioni sono corrette?",
        "options": ["in una cella conviene inserire sia il nome che il cognome di una persona", "in una cella conviene inserire solo il nome o solo il cognome di una persona", "ogni cella può contenere più dati omogenei", "ogni cella dovrebbe sempre contenere un solo dato"],
        "correct": "ogni cella dovrebbe sempre contenere un solo dato"
    },
    {
	'id':8,
        "type": "multiple_choice",
        "question": "Allinea al centro, orizzontalmente, il contenuto della cella selezionata.",
        "options": ["Seleziona cella e clicca 'Centro' nel gruppo allineamento della scheda Home", "Seleziona cella e clicca 'Centro' nel gruppo Zoom della scheda Visualizza", "Seleziona cella e clicca 'Centro' nella scheda Inserisci", "Seleziona cella e clicca 'Centro' nella scheda Layout di pagina."],
        "correct": "Seleziona cella e clicca 'Centro' nel gruppo allineamento della scheda Home",
        
        
    },
    {
	'id':9,
        "type": "open",
        "question": "Inserisci la funzione che scrive il testo 'critico' se il contenuto della cella C15 è minore di '1000' e 'buono' altrimenti.",
        "correct_variants": ["=SE(C15<1000;\"critico\";\"buono\")"]
    },
    {
	'id':10,
        "type": "multiple_choice",
        "question": "Come si sposta un contenuto già selezionato da un foglio di lavoro ad un altro? a partire dalla cella D6.",
        "options": ["Taglia e incolla su Foglio 1 in D6", "Copia e incolla su Foglio 1 in D6", "Sposta e incolla su Foglio 1 in D6", "Duplica e incolla su Foglio 1 in D6"],
        "correct": "Taglia e incolla su Foglio 1 in D6",
        
        
    },
    {
	'id':11,
        "type": "multiple_choice",
        "question": "Inserisci nell'intestazione il testo 'aggiornamento' posizionandolo al centro. Al termine premere invio.",
        "options": ["Vai su 'Formato', poi 'Intestazione', poi 'Centro'", "Vai su Visualizza - Imposta Pagina - 'Intestazione', personalizza intestazione  poi 'aggiornamento'", "Vai su scheda inserisci poi Intestazione e piè di pagina ed al centro inserisci il testo aggiornamento'", "Vai su 'Home', poi 'Intestazione', poi 'Centro'"],
        "correct": "Vai su scheda inserisci poi Intestazione e piè di pagina ed al centro inserisci il testo aggiornamento'",
        
    },
    {
	'id':12,
        "type": "multiple_choice",
        "question": "Formatta il contenuto delle celle selezionate in modo da visualizzare il separatore delle migliaia e una cifra decimale.",
        "options": ["Vai su 'Formato Celle', poi 'Numero'", "Vai su 'Home', poi 'Numero'", "Vai su 'Gruppo numeri' Metti il separatore delle migliaia e poi togli un decimale con gli appositi pulsanti'", "Vai su 'Visualizza', poi 'Numero'"],
        "correct": "Vai su 'Gruppo numeri' Metti il separatore delle migliaia e poi togli un decimale con gli appositi pulsanti'",
        
    },
    {
	'id':13,
        "type": "open",
        "question": "Senza utilizzare la barra multifunzione, inserisci la formula che calcola la differenza tra il contenuto delle celle E2 ed E11.",
        "correct_variants": ["=E2-E11" , "=(E2-E11)"]
    },
    {
	'id':14,
        "type": "multiple_choice",
        "question": "Quale regola occorre seguire nell'attribuzione dei nomi ai fogli di lavoro?",
        "options": ["assegnare nomi composti da una sola parola senza spazi bianchi", "assegnare nomi composti da codici numerici per poterli utilizzare nelle formule", "lasciare sempre i nomi predefiniti per sicurezza", "assegnare nomi significativi invece di accettare il nome predefinito"],
        "correct": "assegnare nomi significativi invece di accettare il nome predefinito"
    },
    {
	'id':15,
        "type": "open",
        "question": "Inserisci la funzione che scrive il testo 'dividendo ok' se il contenuto della cella B33 è maggiore di '300' e 'non pagabili' altrimenti.",
        "correct_variants": ["=SE(B33>300;\"dividendo ok\";\"non pagabili\")"]
    },
    {
	'id':16,
        "type": "open",
        "question": "Utilizza la funzione MEDIA per inserire la formula che calcola il valore medio contenuto nell'intervallo B5:D13.",
        "correct_variants": ["=MEDIA(B5:D13)"]
    },
    {
	'id':17,
        "type": "open",
        "question": "Inserisci la formula che calcola, senza l'uso delle funzioni, la somma del contenuto della cella C8 e quello della cella D8.",
        "correct_variants": ["=C8+D8" , "=(C8+D8)"]
    },
    {
	'id':18,
        "type": "open",
        "question": "Senza l'uso della barra multifunzione e utilizzando esclusivamente gli operatori aritmetici, inserisci la formula che calcola la somma dei contenuti delle celle C3 e C4.",
        "correct_variants": ["=C3+C4" , "=(C3+C4)"]
    },
    {
	'id':19,
        "type": "open",
        "question": "Usando la funzione CONTA.NUMERI inserisci una formula che conta quanti numeri sono presenti nell'intervallo C3:P10",
        "correct_variants": ["=CONTA.NUMERI(C3:P10)"]
    },
    {
	'id':20,
        "type": "multiple_choice",
        "question": "Se la struttura della tabella non è corretta ed è necessario inserire una riga vuota in un punto preciso, dove dovresti inserire la riga?",
        "options": ["Inserisci riga prima dei totali", "Inserisci riga dopo i totali", "Inserisci riga al centro della tabella", "Inserisci riga all'inizio della tabella"],
        "correct": "Inserisci riga prima dei totali",
        
        
    },
    {
	'id':21,
        "type": "open",
        "question": "Senza l'uso della barra multifunzione e utilizzando esclusivamente gli operatori aritmetici inserisci una formula che calcola la somma dei contenuti delle celle B2 e C5 meno il valore contenuto nella cella B7",
        "correct_variants": ["=B2+C5-B7" , "=C5+B2-B7" , "=(B2+C5)-B7"]
    },
    {
	'id':22,
        "type": "multiple_choice",
        "question": "come si stampano sei copie di sole celle selezionate.",
        "options": ["File - Stampa - scelgo 6 copie e stampo", "Stampo sei copie dell'intero foglio", "File - Stampa - Stampa selezione e poi metto 6 copie", "Stampa sei copie della prima pagina"],
        "correct": "File - Stampa - Stampa selezione e poi metto 6 copie",
        
    },
    {
	'id':23,
        "type": "multiple_choice",
        "question": "Se devi salvare il file Excel visualizzato nella cartella C:\\lavoro cambiando il type di formato dati in 'dati XML' e lasciando lo stesso nome.",
        "options": ["File - Salva con nome - salvo come dati XML in C:\\lavoro", "File - Salve e salvo come dati XML in C:\\lavoro", "Salvo con barra di accesso rapido dati XML in C:\\lavoro", "Salva come dati PDF in C:\\lavoro"],
        "correct": "File - Salva con nome - salvo come dati XML in C:\\lavoro",
        
    },
    {
	'id':24,
        "type": "multiple_choice",
        "question": "Salva il file Excel visualizzato nella cartella C:\\lavoro assegnandogli il nome 'nuovoReport'.",
        "options": ["Salva con nome 'nuovoReport' in C:\\lavoro", "Salva con nome 'nuovoFile' in C:\\lavoro", "Salva con nome 'nuovaCartella' in C:\\lavoro", "Salva con nome 'nuovoDocumento' in C:\\lavoro"],
        "correct": "Salva con nome 'nuovoReport' in C:\\lavoro",
        
        
    },
    {
	'id':25,
        "type": "multiple_choice",
        "question": "Fai in modo che i titoli presenti nella riga 2 siano sempre riportati su ogni pagina stampata.",
        "options": ["Inserisci riga - imposta riga 2 come intestazione di stampa", "Scheda Layout di pagina - gruppo imposta pagina - comando stampa titoli e poi si seleziona la riga 2", "Imposta riga 2 come intestazione a piè di pagina", "Imposta riga 2 come intestazione laterale"],
        "correct": "Scheda Layout di pagina - gruppo imposta pagina - comando stampa titoli e poi si seleziona la riga 2",
        
    },
    {
	'id':26,
        "type": "open",
        "question": "Usando la funzione ARROTONDA inserisci una formula che arrotonda il contenuto della cella B4 a zero cifre decimali",
        "correct_variants": ["=ARROTONDA(B4;0)"]
    },
    {
	'id':27,
        "type": "multiple_choice",
        "question": "Come si elimina la visualizzazione della griglia e delle intersezioni di riga e di colonna impostate per quando si stamperà il foglio di lavoro.",
        "options": ["Disattiva la visualizzazione della griglia in 'Imposta Pagina'", "Disattiva la visualizzazione della griglia in 'Visualizza'", "Disattiva la visualizzazione della griglia in 'Home'", "Disattiva la visualizzazione della griglia in 'Inserisci'"],
        "correct": "Disattiva la visualizzazione della griglia in 'Imposta Pagina'",
        
    },
    {
	'id':28,
        "type": "multiple_choice",
        "question": "Cosa succede quando la formula che contiene il riferimento $C$7 viene copiata in un'altra cella?",
        "options": ["Il riferimento di cella cambia solo per la colonna, adattandosi alla nuova posizione della formula", "Il riferimento di cella cambia completamente, adattandosi alla nuova posizione della formula", "Il riferimento di cella non cambia", "Il riferimento di cella cambia solo per la riga, adattandosi alla nuova posizione della formula"],
        "correct": "Il riferimento di cella non cambia"
    },
    {
	'id':29,
        "type": "multiple_choice",
        "question": "Inserisci il bordo inferiore alle celle selezionate.",
        "options": ["Vai su 'Inserisci', poi 'Bordo inferiore'", "Vai su 'Home', poi 'Bordo inferiore'", "Vai su 'Formato', poi 'Bordo inferiore'", "Vai su 'Visualizza', poi 'Bordo inferiore'"],
        "correct": "Vai su 'Home', poi 'Bordo inferiore'",
        
    },
    {
	'id':30,
        "type": "open",
        "question": "Utilizza la funzione MIN per inserire la formula che calcola il valore minimo contenuto nelle celle E5:E9.",
        "correct_variants": ["=MIN(E5:E9)"]
    },
    {
	'id':31,
        "type": "multiple_choice",
        "question": "Che type di errore produce =C5/0?",
        "options": ["#DIV/0!", "#RIF!", "#NOME?", "#VALORE!"],
        "correct": "#DIV/0!"
    },
    {
	'id':32,
        "type": "open",
        "question": "Senza usare la barra multifunzione e utilizzando esclusivamente gli operatori aritmetici, inserisci la formula che calcola la divisione delle celle B5 ed A7.",
        "correct_variants": ["=B5/A7"]
    },
    {
	'id':33,
        "type": "multiple_choice",
        "question": "Quale comando usi per fare in modo che il testo di una cella sia compreso su più righe nella stessa cella?",
        "options": ["Uso il comando di allineamento al centro", "Uso il comando di UNISCI ED ALLINEA AL CENTRO", "Uso il comando di TESTO A CAPO", "Non è possibile porre su più righe il testo in una cella"],
        "correct": "Uso il comando di TESTO A CAPO",
        
    },
    {
	'id':34,
        "type": "open",
        "question": "Usando la funzione CONTA.VALORI inserisci una formula che conta le celle non vuote nell'intervallo A1:F12",
        "correct_variants": ["=CONTA.VALORI(A1:F12)"]
    },
    {
	'id':35,
        "type": "multiple_choice",
        "question": "Utilizza l’apposito pulsante per fa apparire a sinistra nell’intestazione, il nome del file.",
        "options": ["Vai su 'Inserisci', poi 'Nome File'", "Vai su 'Home', poi 'Nome File'", "Vai su Inserisci - Intestazione e piè di pagina e si sceglie l'icona Excel nettendolo alla sinistra del foglio", "Vai su 'Visualizza', poi 'Nome File'"],
        "correct": "Vai su Inserisci - Intestazione e piè di pagina e si sceglie l'icona Excel nettendolo alla sinistra del foglio",
        
    },
    {
	'id':36,
        "type": "multiple_choice",
        "question": "Formatta il contenuto della cella selezionata in modo da avere il formato gg-mm-aaaa.",
        "options": ["Vai in impostazione avanzate gruppo numeri e nella finestra Formato Celle scegli 'Data'", "Vai su 'Home', poi 'Data'", "Vai su 'Inserisci', poi 'Data'", "Vai su impostazioni avanzate gruppo Stili e poi scegli il formato 'data'"],
        "correct": "Vai in impostazione avanzate gruppo numeri e nella finestra Formato Celle scegli 'Data'",
        
    }
]

# Dizionario per salvare le risposte dell'utente
user_answers = {}

@app.route('/')
def home():
    return redirect(url_for('inizia_quiz'))  # Reindirizza alla pagina di inizio quiz


# Inizializza il quiz e resetta user_answers
@app.route('/inizia_quiz', methods=['GET', 'POST'])
def inizia_quiz():
    global user_answers
    user_answers = {}  # Reset delle risposte memorizzate
    return redirect(url_for('domanda', q_id=1))

@app.route('/domanda/<int:q_id>', methods=['GET', 'POST'])
def domanda(q_id):
    global user_answers
    total_questions = len(quiz)  # Calcola il numero totale di domande
    domanda_attuale = next((q for q in quiz if q['id'] == q_id), None)
    
    if domanda_attuale is None:
        return redirect(url_for('risultati'))
    
    if request.method == 'POST':
        # Verifica il tipo di domanda
        if domanda_attuale['type'] == 'multiple_choice':
            answer = request.form.get('risposta')
            if not answer:  # Se non è selezionata alcuna risposta
                flash('Per favore, seleziona una risposta.')
                return redirect(url_for('domanda', q_id=q_id))  # Rimanda alla stessa domanda
        elif domanda_attuale['type'] == 'open':
            answer = request.form.get('risposta', '').strip()
            if not answer:  # Se la risposta è vuota
                flash('Per favore, scrivi una risposta.')
                return redirect(url_for('domanda', q_id=q_id))  # Rimanda alla stessa domanda
        else:
            answer = ''
        
        # Salva la risposta dell'utente nel dizionario
        user_answers[q_id] = {
            'answer': answer,
            'freezed': True  # "Freeza" la domanda quando è confermata
        }
        
        # Vai alla domanda successiva o ai risultati se è l'ultima domanda
        if q_id < total_questions:
            return redirect(url_for('domanda', q_id=q_id + 1))
        else:
            return redirect(url_for('risultati'))

    # Passa 'user_answers' al template
    return render_template('domanda.html', domanda=domanda_attuale, q_id=q_id, total_questions=total_questions, user_answers=user_answers)

@app.route('/termina', methods=['POST'])
def termina_quiz():
    global user_answers
    unanswered_count = 0
    # Conta le domande non risposte
    for q in quiz:
        risposta_utente = user_answers.get(q['id'], {}).get('answer', '').strip().lower()
        if not risposta_utente:
            unanswered_count += 1
    
    # Se ci sono domande non risposte, mostra il messaggio di avviso
    if unanswered_count > 0:
        return render_template('conferma_termina.html', unanswered_count=unanswered_count)
    
    # Se tutte le domande sono state risposte, vai ai risultati
    return redirect(url_for('risultati'))


@app.route('/conferma_termina', methods=['POST'])
def conferma_termina_quiz():
    global user_answers
    # Aggiungi "nessuna risposta" alle domande non risposte
    for q in quiz:
        if not user_answers.get(q['id'], {}).get('answer'):
            user_answers[q['id']] = {'answer': 'nessuna risposta'}
    
    return redirect(url_for('risultati'))


@app.route('/risultati')
def risultati():
    global user_answers
    risultati_quiz = []
    correct_count = 0
    unanswered_count = 0

    for q in quiz:
        risposta_utente = user_answers.get(q['id'], {}).get('answer', '').strip().lower()
        corretta = False

        if q['type'] == 'multiple_choice':
            corretta = risposta_utente == q['correct'].lower()
            correct_answer = q['correct']
        elif q['type'] == 'open':
            corretta = any(risposta_utente == var.lower() for var in q['correct_variants'])
            correct_answer = ', '.join(q['correct_variants'])
            
        if not risposta_utente:  # Conta le domande senza risposta
            unanswered_count += 1

        if corretta:
            correct_count += 1

        risultati_quiz.append({
            'question': q['question'],
            'user_answer': user_answers.get(q['id'], {}).get('answer', ''),
            'correct_answer': correct_answer,
            'is_correct': corretta
        })

    total_questions = len(quiz)
    
    return render_template('risultati.html', risultati=risultati_quiz, correct_count=correct_count, total_questions=total_questions, unanswered_count=unanswered_count)


if __name__ == '__main__':
    app.run(debug=True)
