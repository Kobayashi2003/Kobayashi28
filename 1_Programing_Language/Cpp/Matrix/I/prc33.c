const char* weekday(int year,int month, int day) {
    const char *weekdays[] = {"Sunday", 
        "Monday", "Tuesday", "Wednesday", 
        "Thursday", "Friday", "Saturday", };
    static int m[12] = {31,28,31,30,31,30,31,31,30,31,30,31};
    m[1] = leap(year)? 29 : 28;
    int sum_days = day;
    for (int i = 0; i < month - 1; i++) {
        sum_days += m[i];
    }
    for (int i = 1900; i < year; i++) {
        sum_days += leap(i)? 366 : 365;
    }
    return weekdays[sum_days % 7];
}

int leap(int year) {
    if ((year%4==0 && year%100!=0) || year%400==0)
        return 1;
    return 0;
}