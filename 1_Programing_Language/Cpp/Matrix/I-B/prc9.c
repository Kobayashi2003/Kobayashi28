#include <stdio.h>

extern float weight;

int change_mood(int mood, int val) {
    mood += val;
    if (mood > 0) {
        printf("Little Qin is happy! XD\n");
    } else if (mood == 0) {
        printf("Little Qin wants to play with you~ : )\n");
    } else {
        printf("Little Qin is sad... : (\n");
    }
    return mood;
}

void change_weight(float factor) {
    weight *= factor;
    if (weight < 50.0) {
        printf("Cute!\n");
    } else if (weight <= 200.0) {
        printf("So cute!\n");
    } else {
        printf("Extremely CUTE!\n");
    }
}

int rua(int mood) {
    return change_mood(mood, 1);
}

int feed(int mood) {
    mood = change_mood(mood, 2);
    change_weight(2.0);
    return mood;
}

int do_nothing(int mood) {
    mood = change_mood(mood, -1);
    change_weight(0.75);
    return mood;
}

