#include "DisjSets.h"

/*
    * Construct the disjoint sets object.
    * for simplicity, we assume root1 and root2 are distinct
    * and represent set names.
    * root1 is the root of set 1.
    * root2 is the root of set 2.
*/
void DisjSets::unionSets( int root1, int root2 ) {
    if ( s[root2] < s[root1] ) { // root2 is deeper
        s[root1] = root2;     // Make root2 new root
    } else {
        if ( s[root1] == s[root2] )
            --s[root1];        // Update height if same
        s[root2] = root1;    // Make root1 new root
    }
}

