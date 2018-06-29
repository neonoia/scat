# Automation Supply Chain

This automation supply chain tool is built with robot framework and python. Please give suggestions and inputs for new or other features needed that's not covered in this tool, or if you find some defects and bugs. Thank you

## Prerequisite

* Python 3.6
* Robot Framework
* Chromedriver
* [Couchbase](https://developer.couchbase.com/documentation/server/4.5/sdk/c/start-using-sdk.html)
* Install ```requirements.txt```

## How to Execute

* Before executing, change the location of the desired file to be uploaded and checked in its declaration right at line 10 inside testcase.robot.
* Also update the file first, make sure the ids are not present in the couchbase server.
* Run this command ```chmod +x run.sh``` and finally ```./run.sh```