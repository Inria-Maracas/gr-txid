#!/bin/bash

NB_NOEUDS=21
node_list=( 6 4 35 7 8 9 13 14 16 17 18 23 24 25 27 28 32 33 34 37 38 )
# Création des fichiers et dossiers
echo "Files and folders creation"
python createFolderAndFiles_usrp.py

# Ajouter les droits d'execution
echo "Adding execution rights"
chmod u+x node*/*.py

# Création des tâches
echo "Tasks creation and submission"
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
echo "Wait for tasks to finish"
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
echo "Tasks finished"

# Décompression des résultats et copie des fichiers
echo "Unzipping results and copying files"
cd ~/results
echo "Create folder: "$result
mkdir $result
i=0
while [ $i -lt $NB_NOEUDS ]; do
	echo "File "$(($NUM_FIRST_TASK+i))
	cd task_$(($NUM_FIRST_TASK+i))
	tar -zxf node${node_list[$i]}.tgz
	mv node${node_list[$i]}/*.bin ~/results/$result
	cd ..
	i=$(($i+1))
done
