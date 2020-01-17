#requete = "UPDATE etudiant SET (prenom='idy' nom='ndoye') WHERE id = 2 ;"
#requete="DELETE FROM etudiant WHERE id=1 ;"
requete = "UPDATE etudiant SET prenom='idy' nom='ndoye' WHERE id = 2 ;"

#declaration
database ={}
table = {}
select ={}
insert = {}
update = {}
delete = {}
value = []
requete=requete.lower()
tabRequet=[]
champ = []
mot= ""
j=0
k=0
long = len(requete)

#stockage de la requete dans un tableau
for i in range (0,long):
    if((requete[i] != " ") and (requete[i] != "=")):
        if(requete[i] != "("):
            if(requete[i] != ")"):
                if(requete[i] != "'" ):
                    if(requete[i] !="," ):
                        mot = mot + requete[i]
    else:
        tabRequet.append(mot)
        mot = ""
        j=j+1

#requete create
if(tabRequet[0]=="create"):
    if(tabRequet[1]=="database"):
        database = {
            'nature': "create",
            'database': tabRequet[2]
        }
    if(tabRequet[1]=="table"):
        for i in range (3,len(tabRequet)):
            champ.append(tabRequet[i])
        table = {
            'nature': "create",
            'table': tabRequet[2],
            'fields': champ
        }

#requete drop
if(tabRequet[0]=="drop"):
    if(tabRequet[1]=="database"):
        database = {
            'nature': "drop",
            'database': tabRequet[2]
        }
    if(tabRequet[1]=="table"):
        table = {
            'nature': "drop",
            'table': tabRequet[2]
        }

#requete select
if(tabRequet[0]=="select"):
    if(tabRequet[1]=="*"):
        select = {
            'nature': "select",
            'table':tabRequet[(len(tabRequet)-1)],
            'fields':'*'
        }
    else:
        for i in range (1,(len(tabRequet)-1)):
            if(tabRequet[i] != "from"):
                champ.append(tabRequet[i])
        select = {
            'nature': "select",
            'table': tabRequet[(len(tabRequet)-1)],
            'fields':champ
        }

#requete = "INSERT INTO etudiant prenom, nom VALUES idy ndoye ;"
#requete insert into
if(tabRequet[0]=="insert"):
    for i in range (3,(len(tabRequet)-1)):
        if(tabRequet[i] == "values"):
            break
        else:
            k=k+1
            champ.append(tabRequet[i])
    for i in range ((4+k),(len(tabRequet))):
        value.append(tabRequet[i])
    insert = {
        'nature': "insert",
        'table': tabRequet[2],
        'fields':champ,
        'values': value
    }
#requete update
#requete = "UPDATE etudiant SET prenom='idy' nom='ndoye' WHERE id = 2 ;"
if(tabRequet[0]=="update"):
    for i in range (3,(len(tabRequet)-1)):
        if(tabRequet[i] == "where"):
            break
        else:
            k=k+1
            champ.append(tabRequet[i])
        update = {
        'nature': "update",
        'table': tabRequet[1],
        'fields':champ,
        'values': tabRequet[(len(tabRequet)-1)]
    }
#requete="DELETE FROM `etudiant` WHERE id = 1 ;"
if(tabRequet[0]=="delete"):
        delete = {
        'nature': "delete",
        'table': tabRequet[2],
        'fields':tabRequet[4],
        'values': tabRequet[(len(tabRequet)-1)]
    }
for cle in update.values():
    print(cle)
