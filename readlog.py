#!/usr/bin/python
import sys,os

#print len(sys.argv)
if len(sys.argv) < 2: 
	#raise StandardError, "Syntax: readlog.py [keyword: to start reading] [outputfilename]"
	print "\n This command is used to load log file from lammps production run to create figures."
	#print " after using this, do not forget using [\"showdata.bash\"] to see your data.\n"
	print " [syntax]: readlog.py logfilename [keyword: 1st KeyWord to dump] [outputfilename]\n"
	print " example: readlog.py example.log Step example.inputfornextcmd "
	print "\n keyword is set defaultly to \"Step\", which is normally the first col of your dump..."
	print " uh... again, for keyword, maybe you need2 have a look at your .log file...\n"
	print " if any problem, improvement made, or any Q, please contact me: [ leiw@ustc.edu.cn ]\n"
	exit(-1)

inpfile = sys.argv[1]

if len(sys.argv) >= 3:
	keyword = sys.argv[2]
else:
	keyword = "Step"

if len(sys.argv) >= 4: 
	outfile = sys.argv[3] 
else:
	outfile = inpfile[0:len(inpfile)-4]+".gnuplot.dat"

print ""
print " 1, loading [",inpfile,"],\n 2, started from: \"",keyword,"\"\n 3, output: [",outfile,"].";

inpfp = open(inpfile, 'r')
outfp = file(outfile,'w')

flagkeyword=0
runsteps=0
while True:
	line = inpfp.readline()
	elements = line.split()
	#print " ",elements," ... "
	if len(elements)!=0 and elements[0] == keyword :
		flagkeyword=1;
		tempstr="echo \""
		tempstr2=""
		flag=0
		for i in range(0,len(elements)):
			for j in range(0,len(elements[i])):
				if elements[i][j]== "_":
					tempstr2=elements[i][0:j]+elements[i][j+1:len(elements[i])]
					flag=1
					break
			if flag==0:
				tempstr2=elements[i]
			else:
				flag=0			
			tempstr=tempstr+tempstr2+" "
		tempstr=tempstr+"\" > itemlist.lst"
		print " 4,",tempstr;
		os.system(tempstr);
		print "   id",
		for i in range(0,len(elements)):
			tempnum=i+1
			print "%7d" % tempnum,
		print ""
		print "   nm",
		for i in range(0,len(elements)):
			print "%7s" % elements[i],
		print ""
	if len(elements)!=0 and elements[0] == "run" :
		runsteps=elements[1]
	if flagkeyword==1 and runsteps !=0 :
		break;
if flagkeyword==0 or runsteps==0:
	print " no records in [",inpfile,"]."
	exit -1
else :
	print "\n there are",runsteps,"(or divided by a numb) data, here we go~"

#numerator = 0
while True:
	line = inpfp.readline()
	elements = line.split()
	for i in range(0,len(elements)-1):
		print >> outfp, elements[i],
	print >> outfp, elements[-1]
	if elements[0]==str(runsteps):
		break;
	#numerator=numerator+1
	#print numerator
	#if numerator==runsteps:
	#	break;

print " all data loaded, now you can dwuw with 'em cheers. :-) "



