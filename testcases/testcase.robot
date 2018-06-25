*** Settings ***
Library     Selenium2Library
Library     ../lib/fileParser.py
Library     ../lib/kafkaMessage.py
Library     ../lib/couchbaseCheck.py

*** Test Cases ***
Initialize Browser To Upload
    Open Browser To Upload File
Check And Match Columns
    Match Columns
Check Status
    Check Process Status

*** Keywords ***
Open Browser to Upload File
    Open Browser                    http://10.99.143.80:8080/       browser=chrome
    Choose File To Be Uploaded
    Upload File

Choose File To Be Uploaded
    Page Should Contain Button      xpath://*[@id="file"]
    Choose File                     xpath://*[@id="file"]           /home/budiman/Documents/automation-supply-chain/files/SKU.xlsx

Upload File
    Page Should Contain Button      xpath://*[@id="myButton"]
    # Click Element                   xpath://*[@id="myButton"]

Match Columns
    ${no_of_columns}                Get Number of Columns
    ${no_of_rows}                   Get Number of Rows
    ${columns}                      Get Column Names
    ${items}                        Get List of Items
    Set Global Variable             ${no_of_columns}
    Set Global Variable             ${no_of_rows}
    Set Global Variable             ${columns}
    Match Columns With Kafka
    Match Columns With Couchbase

Match Columns With Kafka
    ${messages}                     Get Topic Messages              SkuCreateRequested              10.99.143.96:9092
    :FOR    ${message}              IN      ${messages}
    
    ${result}                       Match File With Kafka           ${sku}                          ${messages}
    Run Keyword If                  '${result}' == 'False'          Log                             SKU Does not exist in Kafka                     ERROR
    ...                             ELSE    Log                     Passed

Match Columns With Couchbase
    ${cb}=                          Check In Couchbase              ${sku}
    Run Keyword If                  '${cb}' == 'False'              Log                             SKU Does not exist in Couchbase Server          ERROR
    ...                             ELSE    Log                     Passed

Check Process Status
