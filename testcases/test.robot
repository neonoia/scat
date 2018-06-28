*** Test Cases ***

Check Status
    Get Upload Time

*** Keywords ***

Get Upload Time
    @{temp} =	                    Get Time	                    year month day
    ${hour} =	                    Get Time	                    hour
    ${min} =	                    Get Time	                    min
    ${sec} =                        Get Time                        sec
    ${sec} =                        Convert To Integer              ${sec}
    ${sec} =                        Set Variable                    ${sec+1}
    ${date} =                       Catenate                        SEPARATOR=-     @{temp}
    ${day}                          Catenate                        SEPARATOR=:     ${hour}  ${min}  ${sec}
    ${time}                         Catenate                        ${date}     ${day}
    Set Global Variable             ${time}
    Log To Console                  ${time}