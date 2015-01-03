import string
import urllib2
from bs4 import BeautifulSoup

# Associo il nome dell'azione al suo url
nomeUrl = []

'''
==================================================
Per ogni lettera, leggo le pagine del listino per
recuperare il nome e l'indirizzo di ogni titolo
==================================================
'''

#for lettera in ['A']: 
for lettera in string.ascii_uppercase:
    pagina = 1
    while True:
        listino = urllib2.urlopen('http://www.borsaitaliana.it/borsa/azioni/listino-a-z.html?initial=%c&page=%d' % (lettera, pagina))    
        soup = BeautifulSoup(listino.read())
        
        # Esamino
        tabella = soup.body.table
        azioni=tabella.tbody.find_all('td', class_='name')

        conta = 0
        for azione in azioni:
            nome = str(azione.a.string)
            if 'Cv' in nome:
                continue
            elif 'Warr' in nome:
                continue
            else:
                conta += 1
                nomeUrl.append((nome, str(azione.a['href'])))                
        print 'In %c-%d ci sono %d azioni' % (lettera, pagina, conta)

        # Cerco il collegamento alla pagina successiva
        ancora = False
        succ = soup.body.find_all('a')
        for suc in succ:
            att = suc.attrs
            t = att.get('title')
            if t is None:
                pass
            elif 'Successiva' != att['title']:
                pass
            else:
                ancora = True

        if ancora:
            pagina += 1
        else:
            break

# Lista dei titoli: Codice,Isin,Settore,Nome,Indici
elenco = [
    ('FTSEMIB.MI','','prime 40 aziende per capitalizzazione','FTSE MIB',''), 
    ('ITLMS.MI','','Quasi tutto il listino','FTSE Italia All-Share',''),
    ('ITMC.MI','','seconde 60 aziende per capitalizzazione','FTSE Italia Mid Cap',''),
    ('ITSTAR.MI','','medie imprese: da 40M a 1G di capitale','FTSE Italia STAR','')
]

'''
==================================================
Per ogni ezione trovata, vado alla sua pagina e recupero
il resto delle informazioni
==================================================
'''

for elem in nomeUrl:
    isin = elem[1].find('isin')
    isin += 5
    isin = elem[1][isin:]
    isin = isin[:12]
    
    indirizzo = 'http://www.borsaitaliana.it%s' % elem[1]
    print indirizzo
    
    pagina = urllib2.urlopen(indirizzo)    
    soup = BeautifulSoup(pagina.read())
    righe = soup.find_all('td')
    ca = None
    ss = None
    indice = None
    conta = 0
    for riga in righe:
        conta += 1
        x = riga.string
        if None == x:
            continue
        elif 'Codice Alfanumerico' == x:
            ca = conta
        elif 'Super Sector' == x:
            ss = conta
        elif 'Indice' == x:
            indice = conta
        else:
            continue
            
    if ca == None:
        ca = ''
    else:
        ca = str(righe[ca].string) + '.MI'
    if ss == None:
        ss = ''
    else:
        ss = str(righe[ss].string).replace(',', ' +')
    if indice == None:
        indice = ''
    else:
        indici = righe[indice].find_all('a')
        indice = None
        for ind in indici:
            ftse = ind.string
            if None == indice:
                indice = ftse
            elif ftse in indice:
                pass
            else:
                indice = indice + ' + ' + ftse
        
    elenco.append((ca, isin, ss, elem[0], indice))

'''
==================================================
Salvo in formato csv
==================================================
'''
#print elenco
with open('listino.csv', 'wt') as uscita:            
    uscita.write('Codice,Isin,Settore,Nome,Indici\n')       
    for elem in elenco:
        uscita.write('%s,%s,%s,%s,%s\n' % elem)           
        
