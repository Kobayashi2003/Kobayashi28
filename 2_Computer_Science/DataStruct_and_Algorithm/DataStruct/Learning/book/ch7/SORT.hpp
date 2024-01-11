#include <vector>

using namespace std;

template <typename Comparable>
void SORT( vector<Comparable> & items ) {
    if ( items.size( ) > 1 ) {
        vector<Comparable> smaller;
        vector<Comparable> same;
        vector<Comparable> larger;

        auto chosenItem = items[ items.size( ) / 2 ];

        for ( auto & i : items ) {
            if ( i < chosenItem )
                smaller.push_back( std::move( i ) );
            else if ( chosenItem < i )
                larger.push_back( std::move( i ) );
            else
                same.push_back( std::move( i ) );
        }

        SORT( smaller ); 
        SORT( larger );

        std::move( begin( smaller ), end( smaller ), begin( items ) );
        std::move( begin( same ), end( same ), begin( items ) + smaller.size( ) );
        std::move( begin( larger ), end( larger ), end( items ) - larger.size( ) );
    }
}