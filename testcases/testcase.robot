*** Settings ***
Library     Selenium2Library
Library     DateTime
Library     ../lib/fileParser.py
Library     ../lib/kafkaMessage.py
Library     ../lib/couchbaseCheck.py

*** Variables ***
${filename}        /home/budiman/Documents/automation-supply-chain/files/SKU.xlsx

*** Test Cases ***
Initialize Browser To Upload
    Open Browser To Upload File
Check Status
    Get Upload Time
    Wait Until File Processed
Check And Match Columns
    Match Columns

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

Match Columns
    ${no_of_columns}                Get Number of Columns           ${filename}
    ${no_of_rows}                   Get Number of Rows              ${filename}
    ${columns}                      Get Column Names                ${filename}
    ${items}                        Get List of Items               ${filename}
    Set Global Variable             ${no_of_columns}
    Set Global Variable             ${no_of_rows}
    Set Global Variable             ${columns}
    Set Global Variable             ${items}
    Match Details With Kafka
    Match Details With Couchbase

Match Details With Kafka
    ${messages}                     Get Topic Messages                  SkuCreateRequested              10.99.143.96:9092
    Set Global Variable             ${messages}
    :FOR    ${row}                  IN RANGE        ${no_of_rows}
    \    Handle Item Kafka          ${row}

Handle Item Kafka
    [Arguments]    ${row}
    :FOR    ${col}                  IN RANGE        ${no_of_columns}
    \   ${status}                   Match Item Details                  ${items[${row}][${col}]}        ${messages}
    \   Run Keyword If              '${status}' == 'False'              Log                             ${items[${row}][0]} does not exist in Kafka, details: ${items[${row}][${col}]}      ERROR
    \   ...                         ELSE                                Log                             ${items[${row}][0]} : ${items[${row}][${col}]} exists in Kafka

Match Details With Couchbase
    :FOR    ${row}                  IN RANGE        ${no_of_rows}
    \    Handle Item Couchbase      ${row}

Handle Item Couchbase
    [Arguments]    ${row}
    :FOR    ${col}                  IN RANGE        ${no_of_columns}
    \   ${status}=                  Check In Couchbase                  ${items[${row}][0]}             ${columns[${col}]}          ${items[${row}][${col}]}
    \   Run Keyword If              '${status}' == 'False'              Log                             ${items[${row}][0]} does not exist in Couchbase ${items[${row}][0]} ${columns[${col}]} ${items[${row}][${col}]}     ERROR
    \   ...                         ELSE                                Log                             ${items[${row}][0]} : ${items[${row}][${col}]} exists in Couchbase \n