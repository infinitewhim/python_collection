#Date: 13/04/2018
#python2

import re
import os
import time
import sys

#start
#print('checking localization properties: ')
#time.sleep(1)

#base directory for searching, script will be integrated with Jenkins.   python /var/jenkins_home/localization_check.py $WORKSPACE
base_dir = sys.argv[1]


#get all directories which contain localization properties file (excluding "test")
dirlist_all_contains_loc = []
dirlist_to_check = []
for dirpath, dirnames, filenames in os.walk(base_dir):
	if('localization.properties' in filenames ):
		dirlist_all_contains_loc.append(dirpath)
for dirpath in dirlist_all_contains_loc:
	if(not re.match(r'.*test.*',dirpath)):
		dirlist_to_check.append(dirpath)
		


#loop all the dirlist_to_check
for dir_to_check in dirlist_to_check:


	#read localization_properties file to get the reference KV pairs in that specific directory
	ref_kv = {}
	with open(dir_to_check + os.sep + 'localization.properties','r') as f:
	    lines = f.readlines()
	    for line in lines:
	    	#search for uncommented lines which contains "=" pair 
	    	if((re.match(r'.*=.*',line)) and  (not re.match(r'^#',line))  ):
	    		kv = line.split('=')
	    		ref_kv.update({kv[0].strip():kv[1].strip()})


	#get all language translation files in that specific directory and store them in a list
	properties_files_list = []
	for properties_file in os.listdir(dir_to_check):
		if(re.match(r'localization_.*properties',properties_file)):
			properties_files_list.append(properties_file)



	#loop the language file list to check the completeness of the localization_xx file(by comparing with reference). If the
	#key in localization_xx file is present in ref_kv_copy(create a new kv copy for each localization file in order to 
	#compare), then delete the entry. So in the end, the ref_kv_copy should be empty if nothing is missing in 
	#localization_xx file
	
	if(properties_files_list):
		for language_file in properties_files_list:
			ref_kv_copy = ref_kv.copy()
			with open(dir_to_check+ os.sep + language_file,'r') as f:
			    lines = f.readlines()
			    for line in lines:
			    	#search for uncommented lines which contains "=" pair 
			    	if((re.match(r'.*=.*',line)) and  (not re.match(r'^#',line))  ):
			    		kv = line.split('=')
			    		try:
			    			del ref_kv_copy[kv[0].strip()]
			    		except KeyError:
			    			pass
			    			#print('\''+kv[0]+'\'' + '  in ' +dir_to_check+ os.sep + language_file + ' does not exist in the reference')
			    			#print('----------------------------------------------------------------')
			if(ref_kv_copy):
				for missing_key in ref_kv_copy:
					print('\'' + missing_key + '\'' + ' is missing in '+dir_to_check.replace(base_dir,'')+ os.sep + language_file )
					print('----------------------------------------------------------------')
		
		
	#else:
		#print(dirlist_to_check[0]+' has no localization_xx.properties files')
		

    		
	



		




