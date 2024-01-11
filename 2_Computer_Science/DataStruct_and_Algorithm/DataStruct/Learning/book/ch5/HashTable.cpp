#include <vector>
#include <list> 
#include <string>

using namespace std;

template <typename HashedObj>
class HashTable {
public:
    explicit HashTable( int size = 101 );

    bool contains( const HashedObj & x ) const;

    void makeEmpty( );
    bool insert( const HashedObj & x );
    bool insert( HashedObj && x );
    bool remove( const HashedObj & x );  

private:
    vector<list<HashedObj>> theLists;   // The array of Lists
    int currentSize;

    void rehash( );
    size_t myhash( const HashedObj & x ) const;
};

template <typename HashedObj>
size_t HashTable<HashedObj>::myhash( const HashedObj & x ) const {
    static hash<HashedObj> hf;
    return hf( x ) % theLists.size( );
}


// template <typename key>
// class hash {
// public:
//     size_t operator() ( const key & k ) const;
// };

template <>
class hash<string> {
public:
    size_t operator() ( const string & key ) {
        size_t hashVal = 0;
        for ( char ch : key )
            hashVal = 37 * hashVal + ch;
        return hashVal;
    }   
};


