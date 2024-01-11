let n = parseInt(window.prompt('Input')),i;
for(let number = 2; number <= n; number++){
    for(i = 2; i <= Math.sqrt(number); i++){
        if(number % i == 0){
            break;
        }
    }
    i > Math.sqrt(number) && document.write(number + " ");
}