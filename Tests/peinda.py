
requete = input("> ")
database = {} 
table = {} 
select = {} 
insert = {}
value = tabRequet = champ = []
requete=requete.lower()
mot= ""
j= k =0

longueur = len(requete)

for i in range (0,longueur):
    if(requete[i] != " "):
        mot = mot + requete[i]
    else:
        tabRequet.append(mot)
        mot = ""
        j=j + 1

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
    print(select)
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
    print(insert)