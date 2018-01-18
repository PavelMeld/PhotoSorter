import subprocess
import sys

def read_mts_date(filename):

	try:
		date = subprocess.check_output(["./mts/avchd2srt-core", filename]);
		return date
	except:
		return None;

	#try:
	#	process = subprocess.Popen(['./mts/avchd2srt-core', filename],
	#							   stdout=subprocess.PIPE,
	#							   stderr=subprocess.STDOUT)
	#	returncode = process.wait()

	#	if returncode != 0 :
	#		return None;

	#	date = process.stdout.read();
	#	return date
	#except:
	#	return None
	
	
if __name__ == "__main__":
	if len(sys.argv)<2:
		print "Syntax: mtsdate.py <MTS file>"
	else:
		res = read_mts_date(sys.argv[1])
		if res != None:
			print res
