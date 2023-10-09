void SelectedSortInt(int *nums, int n) {
    for (int i=0; i<=n-2; i++) {
        //find minimum idx
        int idx = i;
        for (int j=i+1; j<=n-1; j++) {
            if (nums[j] < nums[idx]) {
                idx = j;
            }
        }

        //swap
        if (i!=idx) {
            int temp = nums[i];
            nums[i] = nums[idx];
            nums[idx] = temp;
        }
    }
}