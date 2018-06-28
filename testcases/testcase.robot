*** Settings ***
Library     Selenium2Library
Library     DateTime
Library     ../lib/fileParser.py
Library     ../lib/kafkaMessage.py
Library     ../lib/couchbaseCheck.py

*** Variables ***
${filename}        /home/budiman/Documents/automation-supply-chain/files/SKU.xlsx

*** Test Cases ***
# Initialize Browser To Upload
SPLY-01
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
    Choose File To Be Uploaded
    Upload File

Choose File To Be Uploaded
    Page Should Contain Button      xpath://*[@id="file"]
    Choose File                     xpath://*[@id="file"]           ${filename}

Upload File
    Page Should Contain Button      xpath://*[@id="myButton"]
    Click Element                   xpath://*[@id="myButton"]

Get Upload Time
    ${day} =	                    Get Time	                    day
    ${month} =	                    Get Time	                    month
    ${year} =	                    Get Time	                    year
    ${hour} =	                    Get Time	                    hour
    ${min} =	                    Get Time	                    min
    ${date} =                       Catenate                        SEPARATOR=-     ${day}  ${month}  ${year}
    ${day}                          Catenate                        SEPARATOR=:     ${hour}  ${min}
    ${time}                         Catenate                        ${date}     ${day}
    Set Global Variable             ${time}

Wait Until File Processed
    Sleep                           10s
    Wait Until Element Is Enabled   xpath:/html/body/div[2]/div/div/div[1]/div/ul/li[3]/a
    Click Element                   xpath:/html/body/div[2]/div/div/div[1]/div/ul/li[3]/a
    Page Should Contain             ${time}

Get Columns Data
    ${col}                          Get Number of Columns           ${filename}
    ${row}                          Get Number of Rows              ${filename}
    ${columns}                      Get Column Names                ${filename}
    ${items}                        Get List of Items               ${filename}
    Set Global Variable             ${col}
    Set Global Variable             ${row}
    Set Global Variable             ${columns}
    Set Global Variable             ${items}

Match Details With Kafka
    ${messages}                     Get Topic Messages                  SkuCreateRequested      10.99.143.96:9092
    Set Global Variable             ${messages}
    ${kafka_status}                 Match Kafka Item Details            ${row}      ${col}      ${items}        ${messages}
        Run Keyword If              '${kafka_status}' == 'False'        Log                     Some item details do not exist in Kafka Topic.                  ERROR
    ...                             ELSE                                Log                     All Item and its details are present in Kafka Topic.

Match Details With Couchbase
    ${couchbase_status}             Match Couchbase Item Details        ${row}      ${col}      ${items}        ${columns}
    Run Keyword If                  '${couchbase_status}' == 'False'    Log                     Some item details do not exist in Couchbase Server.             ERROR
    ...                             ELSE                                Log                     All Item and its details are present in Couchbase Server.