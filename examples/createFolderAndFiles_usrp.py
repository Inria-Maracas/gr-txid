#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from shutil import copyfile, copytree
import os
import time

fichier = open("src/scenario_src.yaml","r")
contenu_src = fichier.read()
fichier.close()

date = time.strftime("%Y%m%d_%Hh%M")
command = "reciever.py -R re_00 -I im_00"
# node_list = [6, 3, 4, 35, 7, 8, 9, 13, 14, 16, 17, 18, 23, 24, 25, 27, 28, 32, 33, 34, 37, 38]	#Mono Rx
node_list = [6, 4, 35, 7, 8, 9, 13, 14, 16, 17, 18, 23, 24, 25, 27, 28, 32, 33, 34, 37, 38] 		#Multi Rx

# Dans la boucle ...
# for i in [1]:						#Mono Rx
for i in range(len(node_list)): 	#Multi Rx

	print "Fichier ", str(node_list[i])
	index = str(i)
	if ( i < 10):
		curr_command = command.replace("00", "0"+str(i))
	else:
		curr_command = command.replace("00", str(i))

	contenu = contenu_src.replace("emitter.py -T " + index + " -P 3580 -G 8 -R 0 -f 2", curr_command)


	# Folder creation
	folder = "node" + str(node_list[i]) + "/"
	os.mkdir(folder)

	# Write new file
	new_file = folder + "scenario.yaml"
	fichier = open(new_file,"w")
	fichier.write(contenu)
	fichier.close()

	# Copy Tx and Rx files
	string_file_tx = folder + "emitter.py"
	string_file_rx = folder + "reciever.py"
	string_file_sch = folder + "scheduler.py"
	string_fold_lib = folder + "lib"
	string_fold_inc = folder + "include"
	string_fold_sha = folder + "share"
	copyfile("src/emitter.py", string_file_tx)
	copyfile("src/reciever.py", string_file_rx)
	copyfile("src/scheduler.py", string_file_sch)
	copytree("src/lib", string_fold_lib)
	copytree("src/include", string_fold_inc)
	copytree("src/share", string_fold_sha)

	# At loop's end
print "Fin."
