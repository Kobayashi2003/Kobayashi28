#include <vector>
#include <string>

using namespace std;


/*
    * Radix sort an array of Strings
    * Assume all are all ASCII
    * Assume all have same length
*/
void contingRradixSort( vector<string> & arr, int stringLen ) {
    const int BUCKETS = 256;

    int N = arr.size();
    vector<string> buffer( N );

    vector<string> *in = &arr;
    vector<string> *out = &buffer;

    for ( int pos = stringLen - 1; pos >= 0; --pos ) {
        vector<int> count( BUCKETS + 1 );

        for ( int i = 0; i < N; ++i )
            ++count[ (*in)[ i ][ pos ] + 1 ];

        for ( int b = 1; b <= BUCKETS; ++b )
            count[ b ] += count[ b - 1 ];

        for ( int i = 0; i < N; ++i )
            (*out)[ count[ (*in)[ i ][ pos ] ]++ ] = std::move( (*in)[ i ] );

        // swap in and out roles
        std::swap( in, out );
    }

    // if odd number of passes, in is buffer, out is arr; so copy back
    if ( stringLen % 2 == 1 )
        for ( int i = 0; i < arr.size(); ++i )
            (*out)[ i ] = std::move( (*in)[ i ] );
}