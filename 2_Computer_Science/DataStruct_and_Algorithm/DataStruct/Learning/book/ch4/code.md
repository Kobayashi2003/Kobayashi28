```cpp
template <typename Object>
struct TreeNode {
    Object element;
    TreeNode *firstChild;
    TreeNode *nextSibling;
};
```

```cpp
void FileSystem::listAll(int depth = 0) const {
    printName(depth);
    if (isDirectory()) 
        for each file c in this directory (for each child)
            c.listAll(depth + 1);
}
```

```cpp
int FileSystem::size() const {
    int totalSize = sizeOfThisFile();
    if (isDirectory())
        for each file c in this directory (for each child)
            totalSize += c.size();
    return totalSize;
}
```

```cpp
template <typename Object>
struct BinaryTree {
    Object element;
    BinaryTree *left;
    BinaryTree *right;
};
```