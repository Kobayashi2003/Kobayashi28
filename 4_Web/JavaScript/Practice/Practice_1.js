//输出100以内的质数
for(var number = 2; number < 100; number++){
    var i = 2;
    for(/*blank */; i < number; i++){
        if(number % i ==0)
            break;
    }
    if(i == number){
        document.write(number+"\n");
    }
}
