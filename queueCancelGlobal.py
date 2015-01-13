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
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from optparse import OptionParser

url = "http://jenkins.openet.com/queue/api/python?pretty=true"
jsonAST = ast.literal_eval(urllib.urlopen(url).read())
#jsonAST = ast.literal_eval(urllib.urlopen('http://10.0.21.218/pk/testQueuePython.out').read())
#pprint (jsonAST)
#print type(jsonAST["items"])

jobMap= {}

statsDirectory = "JobStats"

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
                #print dt.datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))
                write_stat(jobKey, dt.datetime.now().strftime(('%Y-%m-%d')), 1)
                cancelBuild(jobVal[i])

            # else add a 0 to the stats file indicating we didn't delete anything
            #print dt.datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))
            write_stat(jobKey, dt.datetime.now().strftime(('%Y-%m-%d')), 0)

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

#write to a file per job.
def write_stat(jobName, timestamp, deleted):
    print "write_stat"
    if not os.path.exists(statsDirectory):
        print "making stat dir"
        os.makedirs(statsDirectory)

    stats_file = open(statsDirectory + "/" + jobName + "_stats.stats", "a")
    file_path = os.path.abspath(stats_file.name)
    #print file_path
    file_modified = dt.datetime.fromtimestamp(os.path.getmtime(file_path))
    # Delete after a week's logging.
    if dt.datetime.now() - file_modified > dt.timedelta(hours=168):
        os.remove(file_path)

    csv_writer = csv.writer(stats_file)
    data = [timestamp, deleted]

    csv_writer.writerow(data)

    stats_file.close()
    return


def genGraphs(graphOutput):
    for statsFile in os.listdir(statsDirectory):
        print statsFile
        
        filePath = statsDirectory + "/" + statsFile
        print filePath

        #There are 14 bytes in a file with one line with our csv format with a carriage return + line feed.
        #Only graph files with atleast 2 lines of data. Numpy/pyplot doesn't like 1 line of input
        if os.stat(filePath).st_size > 14:
            #impressions are either 1 or 0, indicating whether a job was killed in that run
            days, impressions = np.loadtxt(filePath,unpack=True,delimiter=",", converters={0: mdates.strpdate2num('%Y-%m-%d')})
            
            #print days
            #print impressions
            #convert numbers to ints so we can sum them up, giving us our maximum on the y-axis
            totalList = [0]
            totalList = totalList + map(int, impressions)
            #print "totalList = ",totalList
            
            #Remove duplicate entries from days list
            daysFinal = list(set(days))
            #print daysFinal

            listOfTotalsPerDay = [0]*len(daysFinal)
            #print "listOftotalsPerDay = ", listOfTotalsPerDay
            daysInts = map(int, daysFinal)
            #print "daysInts = ", daysInts
            daysOldInts = map(int, days)
            #print "daysOldInts = ",daysOldInts

            
            daysOldMap = {}
            
            counter = 0
            for day in daysOldInts:
                daySum = 1
                #print totalList[counter]
                if day not in daysOldMap:
                    daysOldMap[day] = totalList[counter]
                else:
                    daysOldMap[day] = daysOldMap[day] + totalList[counter]
                counter+=1
            #print "daysOldMap = ", daysOldMap
            
            
            maxY = sum(totalList)
            #print maxY
            #print daysOldMap.keys()
            #print daysOldMap.values()

                   

            if maxY == 0:
                plt.axhline(y=0)
            else:
                axes = plt.gca()
                axes.set_ylim([0,maxY])


            #Format date of x-axis
            fmt = mdates.DateFormatter('%Y-%m-%d')
            loc = mdates.WeekdayLocator(byweekday=mdates.MONDAY)
            ax = plt.axes()
            ax.xaxis.set_major_formatter(fmt)
            ax.xaxis.set_major_locator(loc) 

            
            #Do the plot.
            plt.grid(True)
            plt.plot_date(x=daysOldMap.keys(), y=daysOldMap.values(), fmt='ro-')

            
            fig = plt.figure(1)
            fig.autofmt_xdate()


            #Give a title to the graph
            jobName = statsFile[:-6]
            graphTitle = "Frequency of killed queued jobs for " + jobName
            plt.title(graphTitle)
            plt.ylabel("No. of times job was killed")


            #N = 3
            #params = plt.gcf()
            #pltSize = params.get_size_inches()
            #params.set_size_inches( (pltSize[0]*N, pltSize[1]*N) )

            plt.show()
            
            #Save it. Adding the graphOutput for the jenkins job so we can write to the workspace directory
            pngName = graphOutput + "/" + jobName + ".png"
            plt.savefig(pngName)

                        
    return

def main(argv):

    job_to_monitor = ''
    parser = OptionParser()
    parser.add_option("-m", "--master", action="store_true", dest="master", default=False, help="Assume master control of the Jenkins job queue")
    parser.add_option("-j", "--job", action="store", type="string", dest="job_to_monitor", default='', help="The Job you wish to monitor for")
    parser.add_option("-o", "--output", action="store", type="string", dest="graphOutput", default='.', help="The output directory of graphs")

    (options, args) = parser.parse_args()

	#print options.filename
    #print options.master
    #print options.job_to_monitor
    
    #Check the output directory to see if it exists first.
    if not os.path.exists(options.graphOutput):
        print "Making graph output directory at: ", options.graphOutput
        os.makedirs(options.graphOutput)

	
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
        #Same for the stats dir. This seems only a problem when the job queue is empty on the very first run of this script
        if not os.path.exists(statsDirectory):
            print "Making stats directory"
            os.makedirs(statsDirectory)
        else:
            print "stats dir exists"

        doCancel('')
        genGraphs(options.graphOutput)
               
 
if __name__ == "__main__":
    main(sys.argv[1:])
