from pickle import dumps ,loads
from sys import getsizeof
global b #Nombre c2imal d'enregistrement dans le buffer ou le bloc
global tnom #La taille du champ Nom
global tprénom #La taille du champ Prénom
global tmat #La taille du champ Matricule
global tniveau #La taille du champ Niveau
global tsupprimer #La taille du champ indiquant l'effacement logique de l'enregistrement
global bufsize #La taille dubfuffer ou du bloc
b = 2
tmat = 20
tnom = 20
tprenom = 20
tniveau = 10
tsupprimer = 1
etud1 = '#' * (tmat + tnom + tprenom + tniveau + tsupprimer)
buf = [0, [etud1] * b] #Utilisé pour le calcul de la taille du buffer
bufsize = getsizeof(dumps(buf)) + (len(etud1) + 1) *  (b - 1) #Formule de calcul de la taille du buffer
print(bufsize)
def resize_chaine(chaine, c2taille):
    """Fonction de redémentionnement des champs de l'enregistrement afin de ne pas avoir des problèmes de taille"""
    for i in range(len(chaine),c2taille):
          chaine = chaine + '#' 
    return chaine


"""chargrmnet initial"""
def Creer_fichier(): 
    """ Procédure de création d'un fichier binaire"""
    fn = input("Donner le nom du fichier : ")
    j = 0 #Parcours des enregistrement
    i = 0 #Parcours des blocs
    n = 0 #Nombre des enregistrements
    #initialisation du buffer : 
    buf_tab = [etud1]*b
    buf_nb = 0 #buf_nb représente le nombre d'enregistrements dans le bloc
    try:
        f = open(fn, "wb")
    except:
        print("Creation du fichier est impossible ")
    rep = 'O'
    while (rep.upper() == 'O'):
        #Lecture des information :
        Nom = input('Donner le nom : \n')
        Prenom = input('Donner le prenom : \n')
        Matricule = input('Donner le matricule : \n')
        Niveau = input('Donner le niveau : \n')
        #Redémentionnement des informations : 
        Matricule = resize_chaine(Matricule, tmat)
        Nom = resize_chaine(Nom, tnom)
        Prenom = resize_chaine(Prenom, tprenom)
        Niveau = resize_chaine(Niveau, tniveau)
        #Enregistrement sous-forme d'une chaine de caractères
        Etud = Matricule + Nom + Prenom + Niveau + '0' #'0' pour non-supprimé
        n += 1 #Augmenter le nombre d'enregistrement
        if(j < b): #bloc non-plain
            buf_tab[j] = Etud
            buf_nb += 1 #Augmenter le nombre d'enregistrement
            j += 1
        else: #bloc plain
            buf=[buf_nb, buf_tab]
            ecrireBloc(f, i, buf) #Ecrire le bloc dans le fichier
            buf_tab=[etud1] * b #Créer un nouveau bloc
            #Mettre dans le bloc le nouveau enregistrement
            buf_nb = 1 
            buf_tab[0] = Etud
            j = 1
            i += 1 #Augmenter le nombre de blocs
        rep = input("Un autre étudiant à ajouter O/N ? ")
    buf=[j,buf_tab]
    ecrireBloc(f, i, buf) #Ecrire le dernier bloc
    affecter_entete(f, 0, n) #Ecrire la première caractéristique
    affecter_entete(f, 1, i+1) #Ecrire la deuxième caractéristique
    f.close()

def affecter_entete(f, offset, val):
    """Fonction pour écrire les caractéristiques dans le fichier selon 'offset'"""
    Adr = offset * getsizeof(dumps(0))
    f.seek(Adr, 0)
    f.write(dumps(val))
    return

def ecrireBloc(f, ind, buff):
    """Procédure pour écrire le bloc dans le fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    f.write(dumps(buff))
    return

def lirebloc(f, ind) :
    """Fonction pour lire le bloc du fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    buf = f.read(bufsize)
    return (loads(buf))

def entete(f, ind):
    """fonction de récupération des caractéristiques selon 'ind'"""
    Adr = ind * getsizeof(dumps(0))
    f.seek(Adr, 0)
    tete = f.read(getsizeof(dumps(0)))
    return loads(tete)

def afficher_fichier():
    """Procédure d'affichage du fichier"""
    fn = input('Entrer le nom du fichier à afficher: ')
    f = open(fn,'rb')
    secondcar = entete(f,1) #Récupération de nombre des blocs
    print(f'votre fichier contient {secondcar} block \n')
    for i in range (0,secondcar):
        buf = lirebloc(f,i)
        buf_nb = buf[0]       
        buf_tab = buf[1]
        print(f'Le contenu du block {i+1} est:\n' )
        for j in range(buf_nb):
            if (buf_tab[j][-1] != '1'): #Ne pas affichier les enregistrements supprimés logiquement changer i a j
                
                print(afficher_enreg(buf_tab[j]))
        print('\n')        
    f.close()
    return
    

"""
the structure bloc [       NB=3  ----0
                    BUF_tab   [ {      mat      |     nom      | prenom      |niveau       |      supprimer}--1       

                                {      mat      |     nom      | prenom      |niveau       |      supprimer}--2

                                {      mat      |     nom      | prenom      |niveau       |      supprimer}--3]

              ]

buf=[0,[]]

buf_nb=buf[0]
buftab=buf[1]


"""
def afficher_enreg(e):
    """Fonction de mise en forme des enregistrements
    Retourne une chaine de caractères sans le '#'"""
    Matricule = e[0:20].replace('#',' ')
    Nom = e[20:40].replace('#',' ')
    Prenom = e[40:60].replace('#',' ')
    Niveau = e[60:70].replace('#',' ')
    Supprimer = e[-1]
    return Matricule + ' ' + Nom + ' ' + Prenom + ' ' + Niveau + Supprimer


def inser(filename):
    print("Entrer les information de l'étudiant: ")
    mat=input("Enter le mat : ")
    nom=input('Enter le nom: ')
    prénom=input('Entrer le prénom: ')
    niveau=input("Entrer l'niveau: ")
    mat=resize_chaine(mat,tmat)
    nom=resize_chaine(nom,tnom)
    prénom=resize_chaine(prénom,tprenom)
    niveau=resize_chaine( niveau,tniveau)
    etud=mat+nom+prénom+niveau+"0"
  

    f=open(filename,"rb+")
    nbr_blocks=entete(f,1)
    nbr_eng=entete(f,0)
    buff=lirebloc(f,nbr_blocks-1)
    buf_nb=buff[0]
    if buf_nb == b:
        buf_tab=[etud1]*b 
        buf_nb=1
        buf_tab[0]=etud  
        buf=[buf_nb,buf_tab]
        ecrireBloc(f,nbr_blocks,buf)  
        affecter_entete(f,1,nbr_blocks+1)



    else:#bloc is not full
        buf_tab = buff[1]
        buf_tab[buf_nb] = etud
        buf_nb += 1
        buf=[buf_nb,buf_tab]
        ecrireBloc(f,nbr_blocks-1,buf)

    affecter_entete(f, 0, nbr_eng+1)
    f.close()       


def chercher(filename,cle):
    f = open(filename, 'rb')
    nb_blocks = entete(f, 1)
    
    for i in range(nb_blocks):
        buf = lirebloc(f, i)
        buf_nb = buf[0]
        buf_tab = buf[1]
        cle= cle +(tmat - len (cle))*"#"
        for j in range(buf_nb):
            r = buf_tab[j]
            if r[0:20] == cle:
                trouv=True
                return [i,j]
    return False                   
    f.close()
    




def supprimer(filename, cle):

    result = chercher(filename, cle)
    if result:
        i, j = result
        f = open(filename, 'r+b')
        nbr_eng=entete(f,0)
        buf = lirebloc(f, i)
        eng=buf[1][j]
        
        #change  supprime = 1 pour logical supprimer
        eng=eng[:len(eng)-1]+'1'
        buf[1][j]=eng
        affecter_entete(f, 0, nbr_eng-1) #Ecrire la première caractéristique
        ecrireBloc(f, i, buf)
            
        print(f"eng ave mat {cle} est logical supp.")
        f.close()
    else:
        print(f"il ya aucun  {cle} .")




###########################################################################

def fragmentation():
    file = input('entrez le nom du fichier : ')
    a = input('entrez la valeur c1imale : ')
    c = input('entrez la valeur c2imale : ')
    
    f = open(file,'rb')
    fc1 = open('filec1','wb')
    fc2 = open('filec2','wb')
    fmoyen = open('filemoyen','wb') 
   
    ic1,jc1= 0,0
    ic2,jc2 =  0,0 
    imoyen = 0
    jmoyen = 0
    buf1 = [0,[etud1]*b]
    buf2 = [0,[etud1]*b]
    buf3 = [0,[etud1]*b]
    for i in range(entete(f,1)):#nbr blocs
        buf = lirebloc(f,i)
        for j in range(buf[0]): #nbr eng 
            if buf[1][j][:buf[1][j].index('#')] > c: #buf[i][j].index["#"] return the end of the mat first #
                if jc2 < b:
                    buf1[1][jc2] = buf[1][j]
                    buf1[0] += 1
                    jc2 += 1
                else:
                    ecrireBloc(fc2,ic2,buf1)
                    ic2 += 1
                    buf1 = [1,[etud1]*b]
                    buf1[1][0] = buf[1][j]
                    jc2 = 1
            elif buf[1][j][:buf[1][j].index('#')] < a:
                if jc1 < b:
                    buf2[1][jc1] = buf[1][j]
                    buf2[0] += 1
                    jc1 += 1
                else:
                    ecrireBloc(fc1,ic1,buf2)
                    ic1 += 1
                    buf2 = [1,[etud1]*b]
                    buf2[1][0] = buf[1][j]
                    jc1 = 1
            else:
                if jmoyen < b:
                    buf3[1][jmoyen] = buf[1][j]
                    buf3[0] += 1
                    jmoyen += 1
                else:
                    ecrireBloc(fmoyen,imoyen,buf3)
                    imoyen += 1
                    buf3 = [1,[etud1]*b]
                    buf3[1][0] = buf[1][j]
                    jmoyen = 1
   
   #f1
    ecrireBloc(fc1,ic1,buf2)
    affecter_entete(fc1,0,ic1*b+jc1)#noombre des eng=nbrebloc*b
    affecter_entete(fc1,1,ic1+1)
    #f2
    ecrireBloc(fc2,ic2,buf1)
    affecter_entete(fc2,0,ic2*b+jc2)
    affecter_entete(fc2,1,ic2+1)
    #f3
    ecrireBloc(fmoyen,imoyen,buf3)
    affecter_entete(fmoyen,0,imoyen*b+jmoyen)
    affecter_entete(fmoyen,1,imoyen+1)
    f.close()
    fc1.close()
    fc2.close()
    fmoyen.close()

filename="test"
cle="55g"
#Creer_fichier()
#afficher_fichier()
#print(chercher(filename,cle))
#supprimer(filename,cle)
#inser(filename)
#afficher_fichier()
#print(chercher(filename,cle))
#fragmentation()
i=0
for i in range(3):
    afficher_fichier()

