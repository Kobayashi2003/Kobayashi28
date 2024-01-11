#include "insertionSort.h"
#include <vector>

using namespace std;

/**
 * quickSort algorithm (driver). 
**/
template <typename Comparable>
void quickSort( vector<Comparable> & a ) {
    quickSort( a, 0, a.size( ) - 1 );
}


/**
 * return median of left, center, and right.
 * order these and hide the pivot.
**/
template <typename Comparable>
const Comparable & median3( vector<Comparable> & a, int left, int right) {
    int center = ( left + right ) / 2;

    if ( a[ center ] < a[ left ] )
        std::swap( a[ left ], a[ center ] );
    if ( a[ right ] < a[ left ] )
        std::swap( a[ left ], a[ right ] );
    if ( a[ right ] < a[ center ] )
        std::swap( a[ center ], a[ right ] );

    std::swap( a[ center ], a[ right - 1 ] );
    return a[ right - 1 ];
}


/**
 * Internal quicksort method that makes recursive calls.
 * Uses median-of-three partitioning and a cutoff of 10.
 * a is an array of Comparable items.
 * left is the left-most index of the subarray.
 * right is the right-most index of the subarray.
**/
template <typename Comparable>
void quickSort( vector<Comparable> & a, int left, int right ) {
    if ( left + 10 <= right ) {
        const Comparable & pivot = median3( a, left, right );

        int i = left, j = right - 1;
        for ( ; ; ) {
            while ( a[ ++i ] < pivot ) { }
            while ( pivot < a[ --j ] ) { }
            if ( i < j )
                std::swap( a[ i ], a[ j ] );
            else
                break;
        }

        std::swap( a[ i ], a[ right - 1 ] ); // Restore pivot

        quickSort( a, left, i - 1 ); // Sort small elements
        quickSort( a, i + 1, right ); // Sort large elements
    }
    else
        insertionSort( a, left, right );
}