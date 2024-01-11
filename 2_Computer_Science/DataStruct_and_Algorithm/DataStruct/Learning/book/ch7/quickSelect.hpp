#include <vector>

using namespace std;

template <typename Comparable>
void quickSelect( vector<Comparable> & a, int left, int right, int k ) {
    if (left + 10 <= right) {
        const Comparable & pivot = median3( a, left, right );

        // Begin partitioning
        int i = left, j = right - 1;
        for ( ; ; ) {
            while ( a[++i ] < pivot ) { }
            while ( pivot < a[--j] ) { }
            if ( i < j )
                std::swap( a[ i ], a[ j ] );
            else
                break;
        }
        std::swap( a[ i ], a[ right - 1 ] ); // Restore pivot

        if ( k <= i )
            quickSelect( a, left, i - 1, k );
        else if ( k > i + 1 )
            quickSelect( a, i + 1, right, k );
        else
            return; // Found kth smallest
    }
    else
        insertionSort( a, left, right );
}