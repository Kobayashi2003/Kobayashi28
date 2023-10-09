#include <stdio.h>
#include <math.h>

const int M = 0x0003C000;

int main() {

    unsigned V[64] = {0}; scanf("%u", &V[0]);

    for (int T = 0; T < 6; ++T) {
        for (int i = pow(2,T)-1; i >= 0; --i) {
            if ((1<<31)&V[i]) 
                V[2*i+1] = V[i] << T;
            else 
                V[2*i+1] = V[i] << 1;
            
            if (1&V[i]) 
                V[2*i] = V[i] >> T;
            else 
                V[2*i] = V[i] >> 1;
        }
    }

    short flg = 0;
    for (int i = 0; i < 64; ++i) {
        if (!((V[i]&M)^M)) {
            flg = 1; break;
        }
    }

    if (flg)
        printf("yes");
    else
        printf("no");

    return 0;
}