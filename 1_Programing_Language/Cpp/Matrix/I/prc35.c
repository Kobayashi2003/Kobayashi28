#include <stdlib.h>

int max(int a, int b) {
    return a > b ? a : b;
}

int min(int a, int b) {
    return a < b ? a : b;
}

int trap(int *height, int heightSize) {
    int *leftMax = (int*)malloc(sizeof(int)*heightSize);
    int *rightMax = (int*)malloc(sizeof(int)*heightSize);

    leftMax[0] = height[0];
    for (int i = 1; i < heightSize; ++i) {
        leftMax[i] = max(leftMax[i-1], height[i]);
    }

    rightMax[heightSize-1] = height[heightSize-1];
    for (int i = heightSize-2; i >= 0; --i) {
        rightMax[i] = max(rightMax[i+1], height[i]);
    }

    int ans = 0;
    for (int i = 0; i < heightSize; ++i) {
        ans += min(leftMax[i], rightMax[i]) - height[i];
    }

    free(leftMax);
    free(rightMax);

    return ans;
}
