#include <string>
#include <vector>

using namespace std;

/*
    * Radix sort an array of Strings
    * Assume all are all ASCII
    * Assume all have same length
*/
void radixSortA( vector<string> & arr, int stringLen ) {
    const int BUCKETS = 256;
    vector<vector<string>> buckets( BUCKETS );

    for ( int pos = stringLen - 1; pos >= 0; --pos ) {
        for ( string & s : arr )
            buckets[ s[ pos ] ].push_back( std::move( s ) );

        int idx = 0;
        for ( auto & thisBucket : buckets ) {
            for ( string & s : thisBucket )
                arr[ idx++ ] = std::move( s );

            thisBucket.clear();
        }
    }
}