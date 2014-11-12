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
from StringIO import StringIO
import sys, getopt
import datetime as dt
import os
import os.path
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from optparse import OptionParser

url = "http://jenkins.openet.com/queue/api/python?pretty=true"
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

    #restricted job deletion flow
    if job_to_monitor != '':
        for jobKey, jobVal in jobMap.iteritems():
            if jobKey == job_to_monitor:
                for i in xrange(0, len(jobVal)):
                    print jobVal[i]
                    print "Deleting job ", jobKey, " with id ", jobVal[i]
                    #jobVal.pop(i)
                    #cancelBuild(jobVal[i])
    #one job to rule them all flow
    else:

        for jobKey, jobVal in jobMap.iteritems():
            for i in xrange(0, len(jobVal) - 1):
                print jobVal[i]
                print "Deleting job ", jobKey, " with id ", jobVal[i]
                #print "Resizing map"
                #jobVal.pop(i)

                #print jobMap
                # TODO trying to add job deletion statistics in a graph. Must remember to truncate the
                # stats file so it doesn't get fricking huge over time.
                write_stat(dt.datetime.now(), 1)
                #cancelBuild(jobVal[i])

            # else add a 0 to the stats file indicating we didn't delete anything
            write_stat(dt.datetime.now(), 0)

    return

def cancelBuild(jobId):

    buf = cStringIO.StringIO()
    curl = pycurl.Curl()

    curl.setopt(curl.WRITEFUNCTION, buf.write)
    curl.setopt(curl.VERBOSE, True)
    curl.setopt(curl.FAILONERROR, True)

    values = {'id': `jobId`}
    #url = "http://jenkins.openet.com/queue/cancelItem?id=" + `jobId`
    #html = urllib.urlopen(url, urllib.urlencode(values)).read()
    #print html
    #print url
    values = urllib.urlencode(values)
    curl.setopt(curl.URL, "http://jenkins.openet.com/queue/cancelItem?")
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

def write_stat(timestamp, deleted):
    stats_file = open("stats.stats", "a")
    file_path = os.path.abspath(stats_file.name)
    file_modified = dt.datetime.fromtimestamp(os.path.getmtime(file_path))
    # Delete after a week's logging.
    if dt.datetime.now() - file_modified > dt.timedelta(hours=168):
        os.remove(file_path)

    csv_writer = csv.writer(stats_file)
    data = [deleted, timestamp]
    csv_writer.writerow(data)

    stats_file.close()
    return

def main(argv):

    job_to_monitor = ''
    parser = OptionParser()
    parser.add_option("-m", "--master", action="store_true", dest="master", default=False, help="Assume master control of the Jenkins job queue")
    parser.add_option("-j", "--job", action="store", type="string", dest="job_to_monitor", default='', help="The Job you wish to monitor for")

    (options, args) = parser.parse_args()

	#print options.filename
    #print options.master
    #print options.job_to_monitor

    if options.master == True and options.job_to_monitor != '':
        print "You must either use the -m flag or the -j flag. Not both."
        sys.exit(1)

    buildJobMap()
    if options.job_to_monitor != '':
        print "restrictive flow"
        job_to_monitor = options.job_to_monitor
        doCancel(job_to_monitor)        
    elif options.job_to_monitor == '':
        print "one job to rule them all flow"
        doCancel('')
        #plot our stats and save to png
        data = np.genfromtxt("stats.stats", delimiter=',', dtype=None)
        print data
        plt.plotfile("stats.stats",(0,))
        plt.savefig('test1.png')
    #print jobMap

 
if __name__ == "__main__":
    main(sys.argv[1:])
