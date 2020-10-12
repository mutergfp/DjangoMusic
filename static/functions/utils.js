function totalDuree(){
    let minutes = 0
    let tmpMinutes = 0
    let tmpSecondes = 0
    let secondes = 0
    let elements = document.getElementsByClassName('.duree')
    for(let i = 0; i < elements.length; i++){
        let str = element.text.split(':')
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
}