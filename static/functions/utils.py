def totalDuree(strs):
    minutes = 0
    tmpMinutes = 0
    tmpSecondes = 0
    secondes = 0
    for strs as str{
        str = element.text.split(':')
        tmpMinutes += parseInt(str[0], 10)
        tmpSecondes += parseInt(str[1], 10)
        while(tmpSecondes!=0){
            if(tmpSecondes>=60){
                tmpSecondes -= 60
                tmpMinutes += 1
            }
            else{
                secondes = tmpSecondes
                minutes = tmpMinutes
            }
        }
    }
    console.log("".concat(minutes.toString(), ":", secondes.toString()))
    return "".concat(minutes.toString(), ":", secondes.toString())