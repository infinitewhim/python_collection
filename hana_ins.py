#!/usr/bin/python2.7
#Date: 18/09/2017
#Version 0.0.1, adapted from perl script
#Author: Henry

import re
import os
import time

arch = os.popen("uname -m").read()
print('architecture: '+arch)


auto = 0
dbsid = ''
multidb = 0
unpack_target_root = '/tmp/install/hdb'

#try to mount if mount is missing
if(not os.path.exists('/usr/supportpackages/HANA')):
	os.system('service autofs restart')
	if(not os.path.exists('/usr/supportpackages/HANA')):
		os.system('mkdir /usr/supportpackages')
		os.system('mount lsi033:/data/supportpackages /usr/supportpackages')

#install some prereqs of SLES
if(os.path.exists('/usr/bin/zypper')):
	print('Checking some prerequisites are installed...\n')
	os.system('zypper install -y libgcc_s1 libstdc++6')

# install some prereqs of RHEL
if(os.path.exists('/usr/bin/yum')):
	print('Checking some prerequisites are installed...\n')
	os.system('/net/sts.linux/Scripts/install-compat-sap.sh')

#choose the right version of SAPCAR to use
SAPCAR = '/sapmnt/fatools/tools/SAPCAR_721.LIN_X86_64'
if (arch == 'ppc64'):
	SAPCAR = '/sapmnt/fatools/tools/SAPCAR_721.LIN_PPC64'
elif (arch == 'ppc64le'):
	SAPCAR = '/sapmnt/fatools/tools/SAPCAR_721.LIN_PPC64LE'

print('\nSAPCAR used is: '+SAPCAR+'\n')

hanaversion = raw_input('Please enter the HANA version you want to install(100 or 200) , leave empty for default which is 200:\n')
if ( not hanaversion):
	hanaversion = '200'
while((hanaversion  != '100') and (hanaversion != '200') and (hanaversion != '')):
	hanaversion = raw_input('HANA version has to be 100 or 200 , leave empty for default which is 200:\n')
if ( not hanaversion):
	hanaversion = '200'


maxrev_param = raw_input('Please enter the maximum revision you want to install(numeric), leave empty for default which is the highest:\n')
if(maxrev_param==''):
	print('Searching for the highest HANA revision for you...')
else:
	print('Searching for the highest PATCH level of the maximum revision '+maxrev_param+'...')
time.sleep(1)

if ((arch == 'ppc64') or (arch =='ppc64le')):
	HANA_DB_ARCHDIR = '/usr/supportpackages/HANA/profiles_power'
else:
	HANA_DB_ARCHDIR = '/usr/supportpackages/HANA/profiles_intel'

ARCHIVES = os.listdir(HANA_DB_ARCHDIR)




maxrev_db = -1
maxpatch_db = 0
profile_db = ''
if maxrev_param != '':
	maxrev_param = int(maxrev_param)

for arcv in ARCHIVES:
	pattern = re.compile(hanaversion+'_(\d+)_(\d+).*')
	rel = pattern.match(arcv)

	if rel:
		if ((maxrev_param=='') or (int(rel.group(1))<=maxrev_param)):
			print('------candidate-------\n'+ 'Revision '+rel.group(1))
			print('Patch    '+rel.group(2)+'\n----------------------\n')
			
			if ( (int(rel.group(1))>maxrev_db) or ((int(rel.group(1))==maxrev_db) and (int(rel.group(2))>=maxpatch_db)) ):
				
				maxrev_db = int(rel.group(1))
				maxpatch_db = int(rel.group(2))
				profile_db = rel.group(0)
				
if(maxrev_db == -1):
	print('no version found to meet the requirement, exiting now')
	time.sleep(2)
	exit(1)
print('Available highest HANA DB revision: '+str(maxrev_db)+', patch: '+str(maxpatch_db)+ ' for version '+hanaversion+'\n')
print('The profile name is: '+profile_db+'\n')

time.sleep(2)


os.system('rm -rf '+unpack_target_root)
os.system('mkdir -p '+unpack_target_root)
print('\nGathering packages now...\n\n')
time.sleep(1)

with open(HANA_DB_ARCHDIR+'/'+profile_db,'r') as f:
    packages = f.readlines()
print('--------------------------------------------------------------------')
for cont in packages:
	print(cont)
print('---------------------------------------------------------------------\n\n')


real_archives = []
for line in packages:
	if (os.path.exists(os.path.join(unpack_target_root,'source.sar'))):
		os.system('rm '+os.path.join(unpack_target_root,'source.sar'))

	list = line.split('->')
	package = list[0].strip()
	archive = list[1].strip()
	print('\nExtracting package '+package+'...\n')

	os.system('mkdir '+unpack_target_root+'/'+package)

	print('archive: '+archive+'\n')
	time.sleep(2)

	source = '/net/sapmnt.kernelpatches/'+archive
	

	if(os.path.exists(source)):
		print('trying the source: '+source+'\n')
		linkcommand = 'ln -s '+'\"'+source+'\"'+' '+unpack_target_root+'/source.sar'
		if(re.match(r'.*TGZ',source)):
			linkcommand = 'ln -s '+'\"'+source+'\"'+' '+unpack_target_root+'/source.tgz'
		print(linkcommand+'\n')
		os.system(linkcommand)

	if(not os.path.exists(source)):
		source = '/net/sapmnt.patch_inbox_external/'+archive
		print('trying the source: '+source+'\n')
		linkcommand = 'ln -s '+'\"'+source+'\"'+' '+unpack_target_root+'/source.sar'
		if(re.match(r'.*TGZ',source)):
			linkcommand = 'ln -s '+'\"'+source+'\"'+' '+unpack_target_root+'/source.tgz'
		print(linkcommand+'\n')
		os.system(linkcommand)



	if(os.path.isfile(os.path.join(unpack_target_root,'source.sar'))):
		os.system(SAPCAR+' -xvf '+unpack_target_root+'/source.sar '+'-R '+unpack_target_root+'/'+package+' -manifest SIGNATURE.SMF')
		os.system('rm '+unpack_target_root+'/source.sar')
		real_archives.append(source)


	if(os.path.isfile(os.path.join(unpack_target_root,'source.tgz'))):
		ori = os.popen("pwd").read().strip()
		os.chdir(unpack_target_root+'/'+package)
		os.system('tar -xvzf '+unpack_target_root+'/source.tgz')
		os.chdir(unpack_target_root)
		os.system('rm source.tgz')
		os.chdir(ori)
		real_archives.append(source)


	# should be single directory extracted. move signature.mf there

	if(os.path.isfile(os.path.join(unpack_target_root,package,'SIGNATURE.SMF'))):
		targets = os.listdir(unpack_target_root+'/'+package)

		for element in targets:
			print('checking if '+element+ ' is subfolder '+element+'\n')
			if (os.path.exists(os.path.join(unpack_target_root,package,element))):
				print('this is a subfolder\n')
				mvcommand = 'mv ' + unpack_target_root+'/'+package+'/SIGNATURE.SMF '+unpack_target_root+'/'+package+'/'+element
				print(mvcommand)
				os.system(mvcommand)

unpack_target_db = unpack_target_root+'/db'

print('\n\nremoving hardware check...\n')
os.system('truncate '+unpack_target_db+'/SAP_HANA_DATABASE/server/HanaHwCheck.py --size=0')

print('\n\nSUMMARY\n\n')
print('The following archives were extracted:\n"')
for real_arc in real_archives:
	print(real_arc+'\n')


components = 'server,afl'
command = './hdblcm --action=install --sapmnt=/hana/shared --install_hostagent --component_root='+unpack_target_root+' --components='+components +' --autostart=y --timezone=Europe/Berlin'

answer = ''
while((answer!='y') and (answer!='n')):
	print('Do you want to install HANA DATABASE now?\n')
	print('command would be: '+command+'\n')
	print('[y/n]?')
	answer = raw_input().lower()

if(answer=='y'):
	os.chdir(unpack_target_db+'/SAP_HANA_DATABASE/')
	os.system(command)

