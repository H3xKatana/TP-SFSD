from pickle import dumps, loads
from sys import getsizeof

global b1
global b2
global b3
b1=3   #la taille max du bloc1
b2=3   # la taille max du bloc2
b3=3   # la taille max du bloc3

global tcle
tcle=10  # taille mac du champ tcle
cle= tcle * '#'
e=[cle,False]

Tbloc1= [0,-1,[e]*b1] # 0 c est le nombre des enrg dans le bloc1 , -1 c est le numero du bloc suivant en debordement 

Tbloc2= [0,-1,[e]*b2]
Tbloc3= [0,-1,[e]*b3]


Tcouple= [cle,0]  # 0 c est la adr de la cle cle

global N 
N=4

index= [Tcouple]*N # la table d index 
nbI=0  # le nombre des enrg dans la table d index

M=4
T= [e]*M

global blocsize

# la taille qui sera ocuper par un bloc 

blocsize = getsizeof(dumps(Tbloc1)) + len(e) * (b1 - 1) + (b1 - 1)
print(blocsize)


def resize_chaine(chaine, maxtaille):
    for i in range(len(chaine), maxtaille):
        chaine = chaine + '#'
    return chaine


def lireBloc(file, i):
    dp = 2 * getsizeof(dumps(0)) + i * blocsize
    file.seek(dp, 0);
    buf = file.read(blocsize)
    return (loads(buf))



def ecrireBloc(file, i, bf):
    dp = 2 * getsizeof(dumps(0)) + i * blocsize
    file.seek(dp, 0)
    file.write(dumps(bf));

    return




def affecter_entete(file, of, c):
    dp = of * getsizeof(dumps(0))
    file.seek(dp, 0)
    file.write(dumps(c))
    return


def entete(file, offset):
    dp = offset * getsizeof(dumps(0))
    file.seek(dp, 0)
    c = file.read(getsizeof(dumps(0)))
    return loads(c)


def afficher_fichier():
    fn = input('Entrer le nom du fichier à afficher: ')
    f = open(fn, 'rb')
    secondcar = entete(f, 1)
    print(f'votre fichier contient {secondcar} block \n')
    for i in range(0, secondcar):
        buf = lireBloc(f, i)
        buf_nb = buf[0]  # recupérer le nb
        buf_tab = buf[1]  # recupérer le tableau d'enregitrement
        print(f'Le contenu du block {i + 1} est:\n')
        # pour chaque enregitrement dans le tableau
        for j in range(buf_nb):
            print(afficher_enreg(buf_tab[j]))  # afficher l'enregitrement
        print('\n')

    f.close()
    return


def afficher_enreg(a):
    # recupérer les champs à partir de chaque enregistrement et remplacer les '#' par un espace
    cle = a[0]
    eff= a[1]
    return cle + '' + eff





def chargement_initial (n,u):
    fn=input('Entre le nom du fichier à créer: ')
    with open (fn , 'rb+') as f:
        i1=0
        j1=0
        nbI=0
        k=0
        for k in range (n):
            e[0]=input(f'Entre la cle de l elm num {k+1}: ')
            if (j1<= b1*(u/100)):
                Tbloc1[2][j1]=e
                j1+=1
            else:
                index[nbI][0]=e
                index[nbI][1]=i1
                nbI+=1
                Tbloc1[0]= j1-1
                buf1=[Tbloc1[0],-1,Tbloc1[2]]
                ecrireBloc(f,i1,buf1)
                i1+=1
                Tbloc1[0]=0
                Tbloc1[2][0]=e
                j1=1
        index[nbI][0]=e
        index[nbI][1]=i1
        Tbloc1[0]=j1-1  
        buf1=[Tbloc1[0],-1,Tbloc1[2]] 
        affecter_entete(f,1,i1)


def Reorganisation(fn1, fn2, fn, u):
    M=4
    T= [e]*M
    with open(fn, 'rb+') as f , open(fn1, 'rb+') as f1, open(fn2, 'rb+') as f2:
        i,j,nbI=0
        for i1 in range(entete(f1,1)):
            buf1=lireBloc(f1,i1)
            for j1 in range(buf1[0]):
                if buf1[2][j1][1] == 'false':
                    if j<= b1 * (u/100):
                        Tbloc1[2][j][0]=buf1[2][j1][0]
                        j+=1
                    else:
                        index[nbI][0]=Tbloc1[2][j-1][0]
                        index[nbI][1]=i
                        nbI+=1
                        Tbloc1[0]=j-1
                        Tbloc1[1]=-1
                        buf=[Tbloc1[0],Tbloc1[1],Tbloc1[2]]
                        ecrireBloc(f,i,buf)
                        i+=1
                        Tbloc1[0]=0
                        Tbloc1[2][0][0]=buf1[2][j1][0]
                        j=1
            if buf1[1] != -1:
                k=0
                i2=buf1[1]
                while i2 != -1:
                    buf2= lireBloc(f2,i2)
                    for j2 in range(buf2[0]):
                        if buf2[2][j2][1] == 'false':
                            T[k][0]=buf2[2][j2][0]
                            k+=1
                    i2=buf2[1]
                for j2 in range(k):
                    if j<= b1 * (u/100):
                        Tbloc1[2][j][0]=T[j2][0]
                        j+=1
                    else:
                        index[nbI][0]= Tbloc1[2][j-1][0]
                        index[nbI][1]=i
                        nbI+=1
                        Tbloc1[0]=j-1
                        Tbloc1[1]=-1
                        buf=[Tbloc1[0],Tbloc1[1],Tbloc1[2]]
                        ecrireBloc(f,i,buf)
                        i+=1
                        Tbloc1[0]=0
                        Tbloc1[2][0][0]= T[j2][0]
                        j=1
        index[nbI][0]=Tbloc1[2][j-1][0]
        index[nbI][1]=i
        nbI+=1
        Tbloc1[0]=j-1
        Tbloc1[1]=-1
        buf=[Tbloc1[0],Tbloc1[1],Tbloc1[2]]
        ecrireBloc(f,i,buf)
        affecter_entete(f,i,1)




def Recherche (c,trouv,i,j,debord,k):
    fn1=input('entre le nom du fichier de données: ')
    fn2=input('entrer le nom du fichier de debordement: ')
    with open(fn1, 'rb+') as f1 ,open(fn2, 'rb+') as f2:
        trouv= False 
        bi=0
        bs=nbI
        cont=True
        while not trouv and bi<=bs:
            k= (bi+bi)//2
            if c < index[k][0]:
                bs=k-1
            else:
                if c > index[k][0]:
                    bi=k+1
                else:
                    trouv = True
        if not trouv :
            if bi <= nbI:
                k=bi
            else:
                k=nbI
                cont=False
        
        trouv = False
        debord = False
        i= index[k][1]
        buf1= lireBloc(f1, i)
        if c < buf1[2][buf1[0]][0]:
            bi=0
            bs=buf1[0]
            while not trouv and bi<= bs:
                j=(bi+bs)/2
                if c < buf1[2][j][0]:
                    bs =j-1
                else:
                    if c > buf1[2][j][0]:
                        bi=j+1
                    else:
                        trouv= True
            if not trouv :
                j=bi
            else:
                if buf1[2][j][1] == False:
                    trouv = False
        else:
            j= buf1[0]+1
            if buf1[1]!= -1:
                debord=True
                i=buf1[1]
                i1=-1
                if cont :
                    while not trouv and i1 != -1:
                        buf2=lireBloc(f2,i)
                        j=0
                        while not trouv and j <= buf2[0]:
                            if c == buf2[2][j][0]:
                                trouv= True
                            else:
                                j+=1
                        if not trouv:
                            i1=i
                            i=buf2[1]
                    if trouv :
                        if buf2[2][j][1] == False:
                            trouv= False
                    else:
                        i=i1




def insertion(c,i,j,k,debord):
    fn1=input('entre le nom du fichier de données: ')
    fn2=input('entrer le nom du fichier de debordement: ')
    with open(fn1, 'rb+') as f1 ,open(fn2, 'rb+') as f2:
        if debord == False:
            buf1=lireBloc(f1,i)
            eng=buf1[2][buf1[0]]
            m=buf1[0]
            while m > j:
                buf1[2][m]=buf1[2][m-1]
                m-=1
            buf1[2][j]=c
            if buf1[0] < b1:
                buf1[0]+=1
                buf1[2][buf1[0]] =eng
                ecrireBloc(f1,i,buf1)
            else:
                if buf1[1] != -1:
                    buf2= lireBloc(f2,buf1[1])
                    if buf2[0] < b2:
                        buf2[0]+=1
                        buf2[2][buf2[0]]= eng
                        ecrireBloc(f2,buf1[1],buf2)
                    else:
                        n=allocBloc(f2)
                        buf2[1]=buf1[1]
                        buf2[2][0]= eng
                        buf2[0]=1
                        ecrireBloc(f2,n,buf2)
                        buf1[1]=n 
                        ecrireBloc(f1,i, buf1)
                else:
                    n=allocBloc(f2)
                    buf2[1]=-1 
                    buf2[2][0]=eng
                    buf2[0]=1
                    ecrireBloc(f2,n,buf2)
                    buf1[1]= n 
                    ecrireBloc(f1,i,buf1)
        else:
            buf1= lireBloc(f1,index[k][1])
            m=buf1[1]
            buf2=lireBloc(f2,m)
            if buf2[0] < b2:
                buf2[0]+=1
                buf2[2][buf2[0]] = eng
                ecrireBloc(f2,m,buf2)
            else:
                n=allocBloc(f2)
                buf2[1] =m 
                buf2[2][0]= eng
                buf2[0]=1
                ecrireBloc(f2,n,buf2)
                buf1[1]= n 
                ecrireBloc(f1,index[k][1],buf1)
        if c[0] > index[k][0] :
            index[k][0]= c[0]



def suppression_logique(i,j,debord):
    fn1=input('Donnez le fichier ou vous voulez supprimer: ')
    fn2=input('Donnez le fichier de deordement: ')
    with open(fn1, 'rb+')as f1 , open(fn2, 'rb+')as f2:
        if debord== False:
            buf1=lireBloc(f1,i)
            buf1[2][j][1]= True
            ecrireBloc(f1,i,buf1)
        else :
            buf2=lireBloc(f2,i)
            buf2[2][j][1]== True
            ecrireBloc(f2,i,buf2)








def allocBloc(fn):
    fn=input('')


def choix(ch):
    if ch == 1:
        chargement_initial(5,2)
    elif ch == 2:
        afficher_fichier()
    elif ch == 3:
        print("hello")
    elif ch == 4:
        insertion()
    elif ch == 5:
        suppression_logique()
    elif ch == 6:
        Reorganisation()
    elif ch == 7:
        print('no')
    else:
        print("la fonction n'existe pas")

def main():
    
    
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