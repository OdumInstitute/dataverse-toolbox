#!/usr/bin/env python3

import argparse
import json
import requests

# arguments. persistentid and version are required, others optional.
parser = argparse.ArgumentParser(description='Download all files from a given dataset ID, in their original format.')
parser.add_argument('-d', '--dataverse', default='http://localhost:8080', help='Dataverse URL. Defaults to http://localhost:8080')
parser.add_argument('-i', '--iterations', default='5', help='calls per page. defaults to 5')

args = parser.parse_args()
if args.dataverse is None:  
  dv = 'http://localhost:8080'
else:
  dv = args.dataverse

if args.iterations is None:
  iter = 5
else:
  iter = int(args.iterations)

static = [
        '/',
        '/dataverse/root/?q=test'
        ]

def time_url(url):
  times = []
  for t in range(iter):
    response = requests.get(url)
    print(str(response.elapsed.total_seconds()) + "\t" + url)
    times.append(response.elapsed.total_seconds())

  avg = sum(times) / int(iter)
  print(url + "average:\t" + str(avg) + " seconds.")
  times.clear()
  
# time static calls  
for req in static:
  url = dv + req
  time_url(url)

# time root dv, process sub_dvs and datasets
url = dv + '/dataverses/root'
time_url(url)

# get root dv contents
url = dv + '/api/dataverses/root/contents'
r = requests.get(url)
j = r.json()

# time each sub_dv, get contents
for i in range(len(j["data"])):
  if (j["data"][i]["type"] == "dataverse"):

    sub_dv = str(j["data"][i]["id"])
    time_url(dv + '/dataverses/' + sub_dv)

    # get sub_dv contents
    url = dv + '/api/dataverses/' + sub_dv + '/contents'
    dvr = requests.get(url)
    dvj = dvr.json()

    # time each child dataset
    for i in range(len(dvj["data"])):
      if (dvj["data"][i]["type"] == "dataset"):
        doi = dvj["data"][i]["protocol"]
        authority = dvj["data"][i]["authority"]
        identifier = dvj["data"][i]["identifier"]
        dsurl = dv + '/dataset.xhtml?persistentId=' + doi + ':' + authority + '/' + identifier
        time_url(dsurl)
