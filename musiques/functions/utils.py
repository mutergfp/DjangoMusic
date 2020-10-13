def totalDuree(strs):
    minutes = 0
    tmpMinutes = 0
    tmpSecondes = 0
    secondes = 0
    for time in strs :
        elements = time.split(':')
        tmpMinutes += int(elements[0], 10)
        tmpSecondes += int(elements[1], 10)
        while tmpSecondes!=0 :
            if (tmpSecondes >= 60) :
                tmpSecondes -= 60
                tmpMinutes += 1
            else :
                secondes = tmpSecondes
                minutes = tmpMinutes
                break
    return "" + str(minutes) + ":" + str(secondes)