
from pickle import dumps,loads
from sys import getsizeof

global b
global tnom
global tprénom
global tmat 
global tniveau

b=2

tnum=10  

tnom=20

tprénom=20 

tniveau=20 

Tetud=tnum+tnom+tprénom+tniveau

Tnreg='#'*(Tetud+1)  
global buf
Tbloc=[0,[Tnreg]*b,-1] #blocks have new zone is lien to zone debordemt if its equal -1 that means theirs none
global blocsize
blocsize=getsizeof(dumps(Tbloc))+len(Tnreg)*(b-1)+(b-1)

N=10 #nmbr index maximale
nbI=0 
tcouple=[0,[0,0],nbI]#cle=0 adr[0,0] numberindex=0
index= [tcouple]*N # la table d index 
# le nombre des enrg dans la table d index



def resize_chaine(chaine, maxtaille):
    for i in range(len(chaine),maxtaille):
          chaine=chaine+'#' 
    return chaine

def lireBloc(file,i):
    dp=2*getsizeof(dumps(0))+i*blocsize#dumbs make a binary represnetion
    file.seek(dp,0)
    buf=file.read(blocsize)
    return (loads(buf))#loads transform the binary form to the orignal form 

def ecrireBloc(file,i,bf):
    dp=2*getsizeof(dumps(0))+i*blocsize
    file.seek(dp,0)
    file.write(dumps(bf))
    return


def affecter_entete(file,of,c):
    dp=of*getsizeof(dumps(0))
    file.seek(dp,0)
    file.write(dumps(c))
    return

def entete(file,offset):
    dp=offset*getsizeof(dumps(0))
    file.seek(dp,0)
    c=file.read(getsizeof(dumps(0)))
    return loads(c)


def créer_fichier():
    fn=input('Entrer le nom du fichier à créer: ')
    j=0
    i=0
    n=0
    buf = [0, [Tnreg]*b , -1] # ---> bloc_nb=0   bloc_tab = (inisialiser ###)  next_block=-1

    try:
      f = open(fn,'wb')
    except:
        print("impossible d'ouvrir le fichier en mode d'écriture ")
    
        return
    

    f_index = open('fileindex','w')

    f_debordement = open('filedebordement',"wb")
    rep='o'


    while(rep=='o'):
        print("Entrer les information de l'étudiant: ")
        num=input("Enter le mat : ")
        nom=input('Entrer le nom: ')
        prénom=input('Entrer le prénom: ')
        niveau=input("Entrer niveau: ")
        num=resize_chaine(num,tnum)
        nom=resize_chaine(nom,tnom)
        prénom=resize_chaine(prénom,tprénom)
        niveau=resize_chaine( niveau,tniveau)
        etud=num+nom+prénom+niveau+'0'

        n=n+1

        if (j<b):#block non plein
           buf[1][j]=etud #mettre l'enregitrement dans le tableau  
           buf[0] += 1 #augmenter le buf.NB
           j += 1
           lastnum = num # pour returner le mat de deriner eng dans le bloc
        else: #block plien
            ecrireBloc(f,i,buf)
            f_index.write(lastnum.replace('#',"") + "\n")#ecrire cle dans index table
            
            buf = [1, [Tnreg]*b , -1]#vider buffer
            buf[1][0] = etud
            j = 1
            i += 1 #counter of blocs
        rep=input('Avez vous un autre élement à entrer O/N: ').lower() 


    ecrireBloc(f,i,buf) 

    f_index.write(num.replace('#',"") + "\n")
    affecter_entete(f,0,n)#nbr eng
    affecter_entete(f,1,i+1)#nbr block

    affecter_entete(f_debordement,0,0)
    affecter_entete(f_debordement,1,0)
    f.close()
    f_index.close()
    f_debordement.close()
    return

def afficher_index():
    
    try:
        with open('fileindex', 'r') as f:
            indexes = f.readlines()
            for index in indexes:
                print(index.strip())  
    except :
        print("File 'fileindex' not found.")
    return



    

def afficher_fichier():
      fn=input('Entrer le nom du fichier à afficher: ')


      try :
        f = open(fn,'rb')
      except:
        print("erreur lors de l'ouverture du fichier")
        return 
      file_debordement = open('filedebordement',"rb")



      
      nbr_blocks=entete(f,1)#nombre des bloc 
      print(f'votre fichier contient {nbr_blocks} block \n')
      for i in range (nbr_blocks):
            buf=lireBloc(f,i)
            print(f'Le contenu du block {i+1} est: ' )

            for j in range(buf[0]):
                if buf[1][j][-1:] != '1':#check for effac logique last zone in buf table
                    print(buf[1][j][:-1].replace('#'," "))
                
            while buf[2] != -1:#check for debordement in loop for all cases
                print(f"le contenu du bloc {buf[2]} dans le fichier de débordement est : ")
                buf = lireBloc(file_debordement,buf[2])#buf[2] is equal to block numbr in debodemnt 
                for j in range(buf[0]):
                    if buf[1][j][-1:] != '1':
                        print(buf[1][j][:-1].replace('#'," "))# afficher l'enregistrement
                  
      return

def rech(fn, cle):
    f = open(fn, "rb+")
    with open('fileindex', 'r') as file_index:
        indexes = file_index.readlines()
        trouv = False

        for i, index in enumerate(indexes):  # Using enumerate to get both index and value
            if index.strip() != 'vide' and index.strip() >= cle:
                trouv = True
                break
        print(type(i))
        if not trouv:
            return -1, -1, False

        buf = lireBloc(f,i)

    for j in range(buf[0]):
        if buf[1][j][:10].replace("#", "") == cle and buf[1][j][-1:] == '0':
            return i, j, True  # Key found
        elif buf[1][j][:10].replace("#", "") > cle and buf[1][j][-1:] == '0':
            return i, j, False  # Insert address

    while buf[2] != -1:
        i1 = buf[2]
        j1 = buf[0]
        with open('filedebordement', 'rb') as f_debordement:
            buf = lireBloc(f_debordement, buf[2])

        for j in range(buf[0]):
            if buf[1][j][:10].replace("#", "") == cle and buf[1][j][-1:] == '0':
                return i1, j, True, True

    return i1, j1, False, False

def insertion():
    file = input('Entrez le nom du fichier : ')

    try:
        f = open(file, "rb+")
    except FileNotFoundError:
        print("Erreur lors de l'ouverture du fichier.")
        return
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return

    file_index = open('fileindex', 'r')
    file_debordement = open("filedebordement", 'rb+')

    print("Entrer les informations de l'étudiant : ")
    num = input("Entrez le numéro d'inscription : ")
    rech_re = rech(file, num)

    if rech_re[2]:
        print("La clé existe déjà.")
        f.close()
        file_debordement.close()
        file_index.close()
        return

    nom = input('Entrez le nom : ')
    prénom = input('Entrez le prénom : ')
    niveau = input("Entrez le niveau : ")

    num = resize_chaine(num, tnum)
    nom = resize_chaine(nom, tnom)
    prénom = resize_chaine(prénom, tprénom)
    niveau = resize_chaine(niveau, tniveau)
    etud = num + nom + prénom + niveau + '0'

    if rech_re[0] == -1:  # Insertion à la fin
        buf = lireBloc(f, entete(f, 1) - 1)

        if buf[0] == b:  # Nouveau bloc à la fin
            buf = [1, [Tnreg] * b, -1]
            buf[1][0] = etud
            ecrireBloc(f, entete(f, 1), buf)
            affecter_entete(f, 1, entete(f, 1) + 1)

            file_index.close()
            file_index = open('fileindex', 'a')
            file_index.write(num.replace("#", "") + '\n')
            affecter_entete(f, 0, entete(f, 0) + 1)
        else:  # On insère à la fin du bloc
            buf[1][buf[0]] = etud
            buf[0] += 1
            ecrireBloc(f, entete(f, 1) - 1, buf)
            affecter_entete(f, 0, entete(f, 0) + 1)

            indexes = file_index.readlines()
            indexes[entete(f, 1) - 1] = num.replace('#', "") + "\n"
            file_index.close()
            file_index = open('fileindex', "w")
            file_index.writelines(indexes)
    elif len(rech_re) == 3:  # Décalages
        if rech_re[2] == 0:  # On peut insérer l'élément dans le bloc précédent
            buf = lireBloc(f, rech_re[0] - 1)  # On va dans le bloc précédent
            indexes = file_index.readlines()
            indexes[rech_re[0] - 1] = num.replace('#', "") + "\n"  # On remplace dans l'index
            file_index.close()
            file_index = open('fileindex', "w")
            file_index.writelines(indexes)

            if buf[2] == -1:  # Aucun bloc dans le débordement, on en crée un nouveau
                buf[2] = entete(file_debordement, 1)
                ecrireBloc(f, rech_re[0] - 1, buf)  # On met le pointeur à jour
                buf = [1, [Tnreg] * b, -1]
                buf[1][0] = etud
                ecrireBloc(file_debordement, entete(file_debordement, 1), buf)
                affecter_entete(file_debordement, 1, entete(file_debordement, 1) + 1)
                affecter_entete(file_debordement, 0, entete(file_debordement, 0) + 1)
            else:
                while buf[2] != -1:  # On cherche le dernier bloc de débordement
                    i = buf[2]
                    buf = lireBloc(file_debordement, buf[2])

                if buf[0] != b:  # Si le dernier bloc n'est pas plein, on rajoute à la fin
                    buf[1][buf[0]] = etud
                    buf[0] += 1
                    ecrireBloc(file_debordement, i, buf)
                    affecter_entete(file_debordement, 0, entete(f, 0) + 1)  # On augmente le nombre d'enregistrements
                else:  # Si le dernier bloc est plein, on en crée un nouveau
                    buf[2] = entete(file_debordement, 1)
                    ecrireBloc(file_debordement, i, buf)  # Le pointeur
                    buf = [1, [Tnreg] * b, -1]
                    buf[1][0] = etud
                    ecrireBloc(file_debordement, entete(file_debordement, 1), buf)
                    affecter_entete(file_debordement, 1, entete(file_debordement, 1) + 1)
                    affecter_entete(file_debordement, 0, entete(file_debordement, 0) + 1)
        else:  # Décalages
            buf = lireBloc(f, rech_re[0])
            if buf[0] != b:  # Il y a de la place dans le bloc
                for j in range(buf[0] - 1, rech_re[1], -1):
                    buf[1][j] = buf[1][j - 1]
                buf[1][rech_re[1]] = etud
                ecrireBloc(f, buf[0], buf)
            else:
                a_decaler = buf[1][buf[0] - 1]
                for j in range(buf[0] - 1, rech_re[1], -1):
                    buf[1][j] = buf[1][j - 1]
                buf[1][rech_re[1]] = etud
                ecrireBloc(f, rech_re[0], buf)

                if buf[2] == -1:  # Aucun bloc dans le débordement, on en crée un nouveau
                    buf[2] = entete(file_debordement, 1)  # Le pointeur
                    ecrireBloc(f, rech_re[0], buf)
                    buf = [1, [Tnreg] * b, -1]
                    buf[1][0] = a_decaler
                    ecrireBloc(file_debordement, entete(file_debordement, 1), buf)
                    affecter_entete(file_debordement, 1, entete(file_debordement, 1) + 1)
                    affecter_entete(file_debordement, 0, entete(file_debordement, 0) + 1)
                else:
                    while buf[2] != -1:  # On cherche le dernier bloc de débordement
                        i = buf[2]
                        buf = lireBloc(file_debordement, buf[2])

                    if buf[0] != b:  # Si le dernier bloc n'est pas plein, on rajoute à la fin
                        buf[1][buf[0]] = a_decaler
                        buf[0] += 1
                        ecrireBloc(file_debordement, i, buf)
                        affecter_entete(file_debordement, 0, entete(file_debordement, 0) + 1)  # On augmente le nombre d'enregistrements
                    else:  # Si le dernier bloc est plein, on en crée un nouveau
                        buf[2] = entete(file_debordement, 1)
                        ecrireBloc(file_debordement, i, buf)  # Le pointeur...
                        buf = [1, [Tnreg] * b, -1]
                        buf[1][0] = a_decaler
                        ecrireBloc(file_debordement, entete(file_debordement, 1), buf)
                        affecter_entete(file_debordement, 1, entete(file_debordement, 1) + 1)
                        affecter_entete(file_debordement, 0, entete(file_debordement, 0) + 1)

    elif len(rech_re) == 4:  # Insertion dans la zone de débordement
        buf = lireBloc(file_debordement, rech_re[0])
        if buf[0] == b:  # On crée un nouveau bloc
            buf[2] = entete(file_debordement, 1)  # Le pointeur
            ecrireBloc(file_debordement, rech_re[0], buf)
            buf = [1, [Tnreg] * b, -1]
            buf[1][0] = etud
            ecrireBloc(file_debordement, entete(file_debordement, 1), buf)
            affecter_entete(file_debordement, 1, entete(file_debordement, 1) + 1)
            affecter_entete(file_debordement, 0, entete(file_debordement, 0) + 1)
        else:
            buf[1][buf[0]] = etud
            buf[0] += 1
            ecrireBloc(file_debordement, rech_re[0], buf)
            affecter_entete(file_debordement,0,entete(file_debordement,0)+1)
        
            
    f.close()
    file_debordement.close()
    file_index.close()


def suppression():
    file = input('Entrez le nom du fichier : ')
    try:
        f = open(file, 'rb+')
    except FileNotFoundError:
        print('Erreur lors de l\'ouverture du fichier.')
        return
    except Exception as e:
        print(f'Erreur inattendue : {e}')
        return

    f_debordement = open("filedebordement", "rb+")
    f_index = open('fileindex', 'r')

    cle = input('Entrez la clé à supprimer : ')
    rech_result = rech(file, cle)

    if not rech_result[2]:
        print("La clé n'existe pas.")
        return

    buf = lireBloc(f, rech_result[0])  # rech_result[0]=i rech_result[1]=j
    buf[1][rech_result[1]] = buf[1][rech_result[1]][:-1] + "1"
    ecrireBloc(f, rech_result[0], buf)

    if len(rech_result) == 4:  # Il y a un bloc de débordement
        i = rech_result[3]
    else:
        i = rech_result[0]

    indexes = f_index.readlines()
    max_key = 'vide'

    if indexes[i][:-1] == buf[1][rech_result[1]][:10].replace('#', ''):  # On doit chercher le max pour remplacer dans l'index
        buf = lireBloc(f, i)

        for j in range(buf[0]):
            if (max_key == "vide" and buf[1][j][-1:] == '1') or (max_key != 'vide' and buf[1][j][:10].replace('#', '') > max_key and buf[1][j][-1:] == '1'):
                max_key = buf[1][j][:10].replace('#', '')

        while buf[2] != -1:
            buf = lireBloc(f_debordement, buf[2])

            for j in range(buf[0]):
                if (max_key == 'vide' and buf[1][j][-1:] == '1') or (max_key != 'vide' and buf[1][j][:10].replace('#', '') > max_key and buf[1][j][-1:] == '1'):
                    max_key = buf[1][j][:10].replace('#', '')

        indexes[i] = max_key + "\n"
        f_index.close()
        f_index = open('fileindex', 'w')
        f_index.writelines(indexes)

    f_index.close()
    f.close()
    f_debordement.close()

def reorganisation():
    file = input('entrez le nom du fichier que vous voulez réorganiser : ')
    try:
        f = open(file,'rb')
    except:
        print("erreur")
        return
    f_debordement = open('filedebordement','rb')
    nvfile = input('entrez le nom du nouveau fichier : ')
    nvfile = open(nvfile,'wb') # le nom du fichier dans lequel on a réorganisé
    i1 = 0
    j1 = 0
    n = 0
    buf1 = [0, [Tnreg]*b , -1]
    for i in range(entete(f,1)):
        buf = lireBloc(f,i)
        for j in range(buf[0]):
            if buf[1][j][-1:] == '0':
                if (j1<b):
                    buf1[1][j1] = buf[1][j]  
                    buf1[0] += 1 
                    j1 += 1
                    n += 1
                else:
                    ecrireBloc(nvfile,i1,buf1)
                    buf1 = [1, [Tnreg]*b , -1]
                    buf1[1][0] = buf[1][j]
                    j1 = 1
                    i1 += 1
                    n += 1
        lindex = []
        lbuf = []
        while buf[2] != -1:
            buf = lireBloc(f_debordement,buf[2])
            for j in range(buf[0]):
                if buf[1][j][-1:] == '1':
                    cle = float(buf[1][j][:10].replace("#",""))
                    lindex.append(cle)
                    lindex.sort()
                    emp = lindex.index(cle)
                    lbuf.insert(emp,buf[1][j])
        for el in lbuf:
            if (j1<b):
                buf1[1][j1] = el 
                buf1[0] += 1 
                j1 += 1
                n += 1
            else:
                ecrireBloc(nvfile,i1,buf1)
                buf1 = [1, [Tnreg]*b , -1]
                buf1[1][0] = el
                j1 = 1
                i1 += 1
                n += 1
    ecrireBloc(nvfile,i1,buf1)
    affecter_entete(nvfile,0,n)
    affecter_entete(nvfile,1,i1+1)
    nvfile.close()
    f.close()


def requete_a_intervalle():
    file = input('entrez le nom du fichier : ')
    try:
        f = open(file,'rb')
    except:
        print("erreur")
        return
    c1 = input('entrez la première valeur : ')
    c2 = input('entrez la deuxième valeur : ')
    c1 = min(c1,c2)
    c2 = max(c1,c2)
    file_index = open('fileindex',"r")
    l = file_index.readlines()
    if c1 > l[entete(f,1)-1][:-1] :
        print('borne min plus grand que le max')
        return
    k = 0    
    for el in l:
        if el[:-1] > c1:
            break
        k += 1
    file_debordement = open('filedebordement','rb')
    for i in range(k,entete(f,1)):
        buf = lireBloc(f,i)
        for j in range(buf[0]):
            if buf[1][j][:10].replace("#","") >= c1 and buf[1][j][:10].replace("#","") <= c2 and buf[1][j][-1:] == '1':
                print(buf[1][j].replace('#'," "))
            if buf[1][j][:10].replace("#","") > c2 :
                return
        while buf[2] != -1:
            buf = lireBloc(file_debordement,buf[2]) # on cherche dans le fichier de débordement
            for j in range(buf[0]):
                if buf[1][j][:10].replace("#","") >= c1 and buf[1][j][:10].replace("#","") <= c2 and buf[1][j][-1:] == '1':
                    print(buf[1][j].replace("#"," "))
        
    








                

    

    

def choix(ch):
    if ch == 1:
        créer_fichier()
    elif ch == 2:
        afficher_fichier()
    elif ch == 3:
        fn=input("enter file name ")
        cle=input("entrer cle :")
        print(cle)
        try:
            f = open(fn,'rb+')
        except:
            print('erreur')
            return
       
        print(rech(fn,cle))
    elif ch == 4:
        insertion()
    elif ch == 5:
        suppression()
    elif ch == 6:
        reorganisation()
    elif ch == 7:
        requete_a_intervalle()
    else:
        print("la fonction n'existe pas")

def main():
    
    afficher_index()
    rep = 'Y'
    while rep == 'Y':
        print("""Entrer votre choix 
                 1: créer_fichier
                 2: afficher_fichier
                 3: recherche
                 4: insertion
                 5: suppression
                 6: reorganisation
                 7: requete_a_intervalle""")
        ch = int(input())
        choix(ch)
        rep = input('Avez-vous une autre opération Y/N? ').upper()

main()
