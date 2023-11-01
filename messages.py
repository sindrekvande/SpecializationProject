timeStamp   = "time"
irrValue    = "irrValue"
ledPercent  = "ledPercent"

btConnect       = "btConnectFlag"
btDisconnect    = "btDisconnectFlag"
btPackets       = "btPackets"

adc1ch0 = "adc1ch0"
adc1ch1 = "adc1ch1"
adc1ch2 = "adc1ch2"
adc1ch3 = "adc1ch3"
adc1ch4 = "adc1ch4"
adc1ch5 = "adc1ch5"
adc1ch6 = "adc1ch6"
adc1ch7 = "adc1ch7"

adc2ch0 = "adc2ch0"
adc2ch1 = "adc2ch1"
adc2ch2 = "adc2ch2"
adc2ch3 = "adc2ch3"
adc2ch4 = "adc2ch4"
adc2ch5 = "adc2ch5"
adc2ch6 = "adc2ch6"
adc2ch7 = "adc2ch7"

adc_channels = [adc1ch0, adc1ch1, adc1ch2, adc1ch3, adc1ch4, adc1ch5, adc1ch6, adc1ch7, adc2ch0, adc2ch1, adc2ch2, adc2ch3, adc2ch4, adc2ch5, adc2ch6, adc2ch7]

messages = {timeStamp:      0,
            irrValue:       0,
            ledPercent:     0,
            btConnect:      0,
            btDisconnect:   0,
            btPackets:      0,

            adc1ch0: 0,
            adc1ch1: 0,
            adc1ch2: 0,
            adc1ch3: 0,
            adc1ch4: 0,
            adc1ch5: 0,
            adc1ch6: 0,
            adc1ch7: 0,

            adc2ch0: 0,
            adc2ch1: 0,
            adc2ch2: 0,
            adc2ch3: 0,
            adc2ch4: 0,
            adc2ch5: 0,
            adc2ch6: 0,
            adc2ch7: 0
            }

testActive = True

def resetBTmessages():
    messages[btConnect] = 0
    messages[btDisconnect] = 0
    messages[btPackets] = 0