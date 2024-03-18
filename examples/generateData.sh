#!/bin/bash

# rx_node_list=( 50 )
# rx_node_list=(     3  4  6  7  8  9 13 14 16 17 18 23 24 25 27 28 32 33 34 35 37 38 10 11 30 31 )
rx_node_list=(     3  4  6  7  8  9 13 14 16 17 18 23 24 25 27 28 32 33 34 35 37 38 )
# rx_node_list=(     12 )
#rx_node_list=(     3  4  6  7   )
# node indeces     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
# tx_node_list=(    03 04 06 07 08 09 50 16 50 50 23 24 50 50 50 50 33 50 50 37 38 )
# tx_node_list=(    03 04 06 07 08 09 13 14 16 17 18 23 24 25 27 28 33 34 35 37 38 )
# tx_node_list=(     3  4  6  7  8  9 13 14 16 17 18 23 24 25 27 28 32 33 34 35 37 38 10 11 30 31 )
tx_node_list=(     3  4  6  7  8  9 13 14 16 17 18 23 24 25 27 28 32 33 34 35 37 38 )
#tx_node_list=( 4 6 )
tx_power_list=(    8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8 )
sched_node=39
duration=30
varying=True
variation_freq=3

freq=865000000
samp_rate=5000000
#docker_image="notou/gr-txid-cxlb:0.5" # On dockerhub
docker_image="ghcr.io/inria-maracas/gr-txid-cxlb:0.5" # On github

# Création des strings de listes de noeuds séparés par ,
tx_list_string=""
for i in ${tx_node_list[@]}; do 
  tx_list_string="${tx_list_string}${tx_list_string:+,}$i"
done

tx_power_string=""
for i in ${tx_power_list[@]}; do 
  tx_power_string="${tx_power_string}${tx_power_string:+,}$i"
done

tx_power_string=""
for i in ${tx_power_list[@]}; do 
  tx_power_string="${tx_power_string}${tx_power_string:+,}$i"
done


rx_list_string=""
for i in ${rx_node_list[@]}; do 
  rx_list_string="${rx_list_string}${rx_list_string:+,}$i"
done


var_option=""
if [ $varying = "True" ]
then var_option="-v"
fi

# Création des fichiers et dossiers
echo "Files and folders creation"
python3 createFolderAndFiles_usrp.py -s ${sched_node} -p 3580 -d ${duration} -r ${rx_list_string} -t ${tx_list_string} -g ${tx_power_string} -G 20 --tx_freq 0.001 -a ${samp_rate} -b 0 -f ${freq} ${var_option} --var_freq ${variation_freq} -i ${docker_image}

# Création des tâches
echo "Tasks creation and submission"
i=0
echo  node${rx_node_list[$i]}
minus task create -f node${rx_node_list[$i]}
NUM_FIRST_TASK=$(minus task submit node${rx_node_list[$i]}.task | tr -dc '0-9')
NUM_LAST_TASK=$((${NUM_FIRST_TASK}+${#rx_node_list[@]}))
i=1
while [ $i -lt ${#rx_node_list[@]} ]; do
	echo  node${rx_node_list[$i]}
	minus task create -f node${rx_node_list[$i]}
	minus task submit node${rx_node_list[$i]}.task
	i=$(($i+1))
done


# Delete node folders and tasks
rm -rf node[1-9]*

# Attente que les tâches soient terminées
echo "Wait for tasks to finish"
result=$(date +"%Y%m%d_%Hh%M")
loop=True
while [ $loop = 'True' ]
do
	waiting=$(minus testbed status | grep "waiting: 0" | wc -l)
	value=$(minus testbed status | grep "(none)" | wc -l)
	id=$(minus testbed status | grep "<Task.*$" | sed 's/^.*id=\([0-9]*\),.*$/\1/')

	if [ $value = '1' ] && [ $waiting = '1' ]
	then loop=False
	else sleep 10 && echo "."
	fi
	if [ "$id" -ge "$NUM_LAST_TASK" ]
	then loop=False
	fi
done
echo "Tasks finished"

# Récupération des résultats
echo "Gathering result files in 10s"
sleep 10
cd ~/results
echo "Create folder: "$result
mkdir $result


echo Frequency:    ${freq} > $result/readme.txt
echo Sample rate:  ${samp_rate} >> $result/readme.txt
echo Image: ${docker_image} >> $result/readme.txt
echo Duration:     ${duration} >> $result/readme.txt
echo TX:     ${tx_list_string} >> $result/readme.txt
echo RX:     ${rx_list_string} >> $result/readme.txt
echo Sched:     ${sched_node} >> $result/readme.txt
if [ $varying = "True" ]
then echo Varying:     True     @ ${variation_freq}Hz >> $result/readme.txt
else echo Varying:     False >> $result/readme.txt
fi

i=0
while [ $i -lt ${#rx_node_list[@]} ]; do
	echo "File "$(($NUM_FIRST_TASK+i))
	
	mv task_$(($NUM_FIRST_TASK+i))/node${rx_node_list[$i]}/task_$(($NUM_FIRST_TASK+i))_container_0/root/*.bin ~/results/$result
	i=$(($i+1))
done
