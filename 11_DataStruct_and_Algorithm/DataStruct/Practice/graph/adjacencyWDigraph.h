#include "graph.h"
#include <sstream>  

using namespace std;

template <typename T>
class adjacencyWDigraph : public graph<T> {
protected:
    int n;
    int e;
    T **a;
    T noEdge; // the value stands for no edge
publc:  
    adjacencyWDigraph(int numberOfVertices = 10, T theNoEdge = 0) {
        if (numberOfVertices < 0)
            throw illegalParameterValue("number of vertices must be >= 0");
        n = numberOfVertices;
        e = 0;
        noEdge = theNoEdge;
        make2dArray(a, n + 1, n + 1);
        for (int i = 1; i <= n; i++)
            fill(a[i], a[i] + n + 1, noEdge);
    }
    ~adjacencyWDigraph() { delete2dArray(a, n + 1); }
    int numberOfVertices() const { return n; }
    int numberOfEdges() const { return e; }
    bool directed() const { return true; }
    bool weighted() const { return true; }
    bool existsEdge(int i, int j) const {
        if (i < 1 || j < 1 || i > n || j > n || a[i][j] == noEdge)
            return false;
        else 
            return true;
    }
    void insertEdge(edge<T> *theEdge) {
        // insert theEdge into the graph, if the edge is already there, change the weight of the edge
        int v1 = theEdge->vertex1();
        int v2 = theEdge->vertex2();
        if (v1 < 1 || v2 < 1 || v1 > n || v2 > n || v1 == v2) {
            ostringstream s;
            s << "(" << v1 << "," << v2 << ") is not a permissible edge";
            throw illegalParameterValue(s.str());
        }
        if (a[v1][v2] == noEdge)
            e++;
        a[v1][v2] = theEdge->weight();
    }
    void eraseEdge(int i, int j) {
        if (i >= 1; && j >= 1 && i <= n && j <= n && a[i][j] != noEdge) {
            a[i][j] = noEdge;
            e--;
        }
    }
    void checkVertex(int theVertex) const {
        if (theVertex < 1 || theVertex > n) {
            ostringstream s;
            s << "no vertex " << theVertex;
            throw illegalParameterValue(s.str());
        }
    }
    int degree(int theVertex) const {
        throw undefinedMethod("degree() undefined");
    }
    int outDegree(int theVertex) const {
        checkVertex(theVertex);
        int sum = 0;
        for (int j = 1; j <= n; j++)
            if (a[theVertex][j] != noEdge)
                sum++;
        return sum;
    }
    int inDegree(int theVertex) const {
        checkVertex(theVertex);
        int sum = 0;
        for (int j = 1; j <= n; j++)
            if (a[j][theVertex] != noEdge)
                sum++;
        return sum;
    }

    class myIterator : public vertexIterator<T> {
    public:
        myIterator(T* theRow, T* theNoEdge, int numberOfVertices) {
            row = theRow;
            noEdge = theNoEdge;
            n = numberOfVertices;
            currentVertex = 1;
        }  
        ~myIterator() {}

        int next(T& theWeight) {
            for (int j = currentVertex; j <= n; j++) {
                if (row[j] != *noEdge) {
                    currentVertex = j + 1;
                    theWeight = row[j];
                    return j;
                }
            }
            currentVertex = n + 1;
            return 0;
        }

    protected:
        T* row;
        T* noEdge;
        int n;
        int currentVertex;
    };

    myIterator* iterator(int theVertex) {
        checkVertex(theVertex);
        return new myIterator(a[theVertex], &noEdge, n);
    }
};