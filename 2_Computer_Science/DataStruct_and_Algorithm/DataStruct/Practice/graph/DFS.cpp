void dfs(int v, int reach[], int label) {
    graph<T>::reach = reach;
    graph<T>::label = label;
    rDfs(v);
}


void rDfs(int v) {
    reach[v] = lable;
    vertexIterator<T> *iw = iterator(v);
    int u;
    while ((u = iw->next()) != 0) {
        if (reach[u] == 0) {
            rDfs(u);
        }
    }
}