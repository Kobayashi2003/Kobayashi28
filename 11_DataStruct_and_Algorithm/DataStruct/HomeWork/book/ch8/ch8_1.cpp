#include <iostream>
#include "DisjSets.h"

int main() {

    DisjSets ds{ 17 };

    ds.unionSets( 1, 2 );
    ds.unionSets( 3, 4 );
    ds.unionSets( 3, 5 );
    ds.unionSets( 1, 7 );
    ds.unionSets( 3, 6 );
    ds.unionSets( 8, 9 );
    ds.unionSets( 1, 8 );
    ds.unionSets( 3, 10 );
    ds.unionSets( 3, 11 );
    ds.unionSets( 3, 12 );
    ds.unionSets( 3, 13 );
    ds.unionSets( 14, 15 );
    ds.unionSets( 16, 0 );
    ds.unionSets( 14, 16 );
    ds.unionSets( 1, 3 );
    ds.unionSets( 1, 14 );

    // arbitary union
    for ( auto i : ds )
        cout << i << " ";
    cout << endl;


    DisjSets ds1{ 17 };
    ds1.unionSets_by_height( 1, 2 );
    ds1.unionSets_by_height( 3, 4 );
    ds1.unionSets_by_height( 3, 5 );
    ds1.unionSets_by_height( 1, 7 );
    ds1.unionSets_by_height( 3, 6 );
    ds1.unionSets_by_height( 8, 9 );
    ds1.unionSets_by_height( 1, 8 );
    ds1.unionSets_by_height( 3, 10 );
    ds1.unionSets_by_height( 3, 11 );
    ds1.unionSets_by_height( 3, 12 );
    ds1.unionSets_by_height( 3, 13 );
    ds1.unionSets_by_height( 14, 15 );
    ds1.unionSets_by_height( 16, 0 );
    ds1.unionSets_by_height( 14, 16 );
    ds1.unionSets_by_height( 1, 3 );
    ds1.unionSets_by_height( 1, 14 );

    // union by height
    for ( auto i : ds1 )
        cout << i << " ";
    cout << endl;


    DisjSets ds2{ 17 };
    ds2.unionSets_by_size( 1, 2 );
    ds2.unionSets_by_size( 3, 4 );
    ds2.unionSets_by_size( 3, 5 );
    ds2.unionSets_by_size( 1, 7 );
    ds2.unionSets_by_size( 3, 6 );
    ds2.unionSets_by_size( 8, 9 );
    ds2.unionSets_by_size( 1, 8 );
    ds2.unionSets_by_size( 3, 10 );
    ds2.unionSets_by_size( 3, 11 );
    ds2.unionSets_by_size( 3, 12 );
    ds2.unionSets_by_size( 3, 13 );
    ds2.unionSets_by_size( 14, 15 );
    ds2.unionSets_by_size( 16, 0 );
    ds2.unionSets_by_size( 14, 16 );
    ds2.unionSets_by_size( 1, 3 );
    ds2.unionSets_by_size( 1, 14 );

    // union by size
    for ( auto i : ds2 )
        cout << i << " ";
    cout << endl;


    return 0;
}