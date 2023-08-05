virtual void bfs(int v, int reach[], int lable) {
    arrayQueue<int> q(10);
    reach[v] = lable;
    q.push(v);
    while (!q.isEmpty()) {
        int w = q.front();
        q.pop();
        vertexIterator<int> *iw = iterator(w);
        int u;
        while ((u = iw->next()) != 0) {
            if (reach[u] == 0) {
                reach[u] = lable;
                q.push(u);
            }
            delete iw;
        }
    }
}