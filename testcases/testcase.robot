*** Settings ***
Library     Selenium2Library
Library     DateTime
Library     ../lib/fileParser.py
Library     ../lib/kafkaMessage.py
Library     ../lib/couchbaseCheck.py
Resource    preparation.robot

*** Variables ***
${filename}        /home/budiman/Documents/automation-supply-chain/files/SKU.xlsx

*** Test Cases ***
SPLY-01
# Initialize Browser To Upload
    Open Browser To Upload File
# Check File Upload Status
SPLY-02
    Get Upload Time
    Wait Until File Processed
# Check And Match Excel Columns Details
SPLY-03
    Get Columns Data
    Match Details With Kafka
    Match Details With Couchbase

*** Keywords ***
Open Browser to Upload File
    Open Browser                    http://10.99.143.80:8080/       browser=chrome
    Page Should Contain Button      xpath://*[@id="file"]
    Choose File                     xpath://*[@id="file"]           ${filename}
    Page Should Contain Button      xpath://*[@id="myButton"]
    Click Element                   xpath://*[@id="myButton"]

Get Upload Time
    ${day}= 	                    Get Time	                    day
    ${month}=  	                    Get Time	                    month
    ${year}=	                    Get Time	                    year
    ${hour}=	                    Get Time	                    hour
    ${min}= 	                    Get Time	                    min
    ${date}=                        Catenate                        SEPARATOR=-     ${day}   ${month}   ${year}
    ${day}=                         Catenate                        SEPARATOR=:     ${hour}  ${min}
    ${time}=                        Catenate                        ${date}         ${day}
    Set Global Variable             ${time}

Wait Until File Processed
    Wait For Condition              return document.getElementById("upload-loader").style.display == "none"        timeout=30s
    Click Element                   xpath:/html/body/div[2]/div/div/div[1]/div/ul/li[3]/a
    Page Should Contain             ${time}

Get Columns Data
    ${columns}                      Get Column Names                ${filename}
    ${items}                        Get List of Items               ${filename}
    Set Global Variable             ${columns}
    Set Global Variable             ${items}

Match Details With Kafka
    ${kafka_status}                 Match Kafka Item Details            ${items}        SkuCreateRequested      10.99.143.96:9092
    Run Keyword If                  '${kafka_status}' == 'False'        Log                     Some item details do not exist in Kafka Topic.                  ERROR
    ...                             ELSE                                Log To Console          All Item and its details are present in Kafka Topic.

Match Details With Couchbase
    ${couchbase_status}             Match Couchbase Item Details        ${items}        ${columns}        10.99.143.96:8091         Administrator       password        item
    Run Keyword If                  '${couchbase_status}' == 'False'    Log                     Some item details do not exist in Couchbase Server.             ERROR
    ...                             ELSE                                Log To Console          All Item and its details are present in Couchbase Server.