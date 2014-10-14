
#!/usr/bin/env python

##################################
# This script checks for multiple jobs pending in the job queue and kills 
# the multiples off.
# This is needed for some downstream jobs that don't take very long.
# Eg: an increment build job fires, then does a CI build job. While the build job is running the increment job
# fires again (every 20 minutes in our case). This can build up an unneeded clog in the build queue.
# The script could be easily modified to become some master queued job killer of its dominion, but it's expected to be used in a downstream job for now.
#################################

import httplib, urllib, urllib2
import json
import ast
from pprint import pprint 
import pycurl
import cStringIO
import sys, getopt


url = "<jenkins_url>/queue/api/python?pretty=true"
jsonAST = ast.literal_eval(urllib.urlopen(url).read())
#jsonAST = ast.literal_eval(urllib.urlopen('http://10.0.21.218/pk/testQueuePython.out').read())
#pprint (jsonAST)
#print type(jsonAST["items"])

jobMap= {}

#If we run this job independently from a dependency flow. Eg: Not a downstream job, we'd want to keep the last item in the queue as that
#would be the most recent job queued, meaning it is more updated that the previously queued incarnations.
def buildJobMap():
	#What we need to kill queued jobs is the job id which is in the id field of the queued job.
	for item in jsonAST["items"]:
		#pprint (item["task":item["name"]])
		if item["task"].get("name") not in jobMap:
			print "adding ", item["task"].get("name")
			
			#key = value.
			value = [item["id"]]
			jobMap[item["task"].get("name")] = value
		else:
			jobMap[item["task"].get("name")].append(item["id"])
			
	print jobMap
	return



#job_to_monitor is a string of the jenkins job you wish to kill if there's duplicates.
def doCancel(job_to_monitor):

	#now iterate through jobMap and delete jobs. We need to do some checks on the value lists aswell...
    print "find duplicate jobs in the job queue..."
	#we only want to delete jobs up until the biggest id for that Job name.
   
    for jobKey, jobVal in jobMap.iteritems():
    #Change if statement if we aren't running as a downstream job. At that point we should check whether there is already a job in the queue.
    #only delete when we have more than one id in the list.
    #In this case, we are a downstream job so we want to delete every occurence of the job since our downstream job is going to kick off.
        if jobKey == job_to_monitor:
            for i in xrange(0, len(jobVal)):
                print jobVal[i]
		print "Deleting job ", jobKey, " with id ", jobVal[i]
                cancelBuild(jobVal[i])
		
    return

def cancelBuild(jobId):

	buf = cStringIO.StringIO()
	curl = pycurl.Curl()

	curl.setopt(curl.WRITEFUNCTION, buf.write)
	curl.setopt(curl.VERBOSE, True)
	curl.setopt(curl.FAILONERROR, True)

	values = {'id': `jobId`}
	
	#html = urllib.urlopen(url, urllib.urlencode(values)).read()
	#print html
	#print url
	values = urllib.urlencode(values)
	curl.setopt(curl.URL, "<jenkins_url>/queue/cancelItem?")
	curl.setopt(curl.POST, 1)
	curl.setopt(curl.POSTFIELDS, values)

	try:
	    curl.perform()

	    #print buf.getvalue()
	    
	except pycurl.error, error:
	    errno, errstr = error
	    print 'An error occurred: ', errstr
	    return

	buf.close()
	return

def main(argv):
    job_to_monitor = ''
    jPresent = False
    try:
        opts, args = getopt.getopt(argv, "hj:",["job="])
    except getopt.GetoptError:
        print 'queueCancel.py -j <JOB_NAME>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'queueCancel.py -j <JOB_NAME>'
            sys.exit()
        elif opt in ("-j", "--job"):
            job_to_monitor = arg
            jPresent = True

    if not jPresent:
        print 'queueCancel.py -j <JOB_NAME>'
        sys.exit(2)

        

    buildJobMap()
    doCancel(job_to_monitor)



if __name__ == "__main__":
    main(sys.argv[1:])
