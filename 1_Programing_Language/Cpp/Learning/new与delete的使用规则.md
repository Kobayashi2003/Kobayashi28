# new 与 delete 的使用规则

1. 不要使用 delete 来释放不是 new 分配的内存
2. 不要使用 delete 释放同一个内存块两次
3. 如果使用 new [] 来为数组分配内存，则应使用 delete [] 来释放
4. 如果使用 new 来为一个实体分配内存，则应使用 delete（没有方括号）来释放
5. 对空指针应用 delete 是安全的