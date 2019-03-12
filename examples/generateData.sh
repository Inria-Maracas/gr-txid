#!/bin/bash

NB_NOEUDS=1
# node_list=( 6 4 35 7 8 9 13 14 16 17 18 23 24 25 27 28 32 33 34 37 38 )
node_list=( 4 7 34 )
# Création des fichiers et dossiers
echo "Création des fichiers et dossiers"
python createFolderAndFiles_usrp.py

# Ajouter les droits d'execution
echo "Ajout des droits d'execution"
chmod u+x node*/*.py

# Création des tâches
echo "Création et soumission des tâches"
i=0
echo  node${node_list[$i]}
minus task create node${node_list[$i]}
NUM_FIRST_TASK=$(minus task submit node${node_list[$i]}.task | tr -dc '0-9')
i=1
while [ $i -lt $NB_NOEUDS ]; do
	echo  node${node_list[$i]}
	minus task create node${node_list[$i]}
	minus task submit node${node_list[$i]}.task
	i=$(($i+1))
done


# Delete node folders and tasks
rm -rf node[1-9]*

# Attente que les tâches soient terminées
echo "Attente que les tâches soient terminées"
result=$(date +"%Y%m%d_%Hh%M")
loop=True
value=$(minus testbed status | grep "(none)" | wc -l)
while [ $loop = 'True' ]
do
	if [ $value = '1' ]
	then loop=False
	else sleep 10 && echo "."
	fi
	value=$(minus testbed status | grep "(none)" | wc -l)
done
echo "Tâches terminées"

# Décompression des résultats et copie des fichiers
echo "Décompression des résultats et copie des fichiers"
cd ~/results
echo "Création du dossier "$result
mkdir $result
i=0
while [ $i -lt $NB_NOEUDS ]; do
	echo "Fichier "$(($NUM_FIRST_TASK+i))
	cd task_$(($NUM_FIRST_TASK+i))
	tar -zxf node${node_list[$i]}.tgz
	mv node${node_list[$i]}/*.bin ~/results/$result
	cd ..
	i=$(($i+1))
done

# Envoi des fichiers sur le serveur de Nokia
#echo "Envoi des fichiers sur le serveur de Nokia"
#ssh -p 2020 thibaud@159.217.142.68 "cd data/ && mkdir $result"
#scp -P 2020 -r $result/ thibaud@159.217.142.68:~/data/
