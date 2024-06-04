#include "bitmap.h"
#include "stdlib.h"
#include "stdio.h"

BitMap::BitMap()
{
}

void BitMap::initialize(char *bitmap, const int length)
{
    this->bitmap = bitmap;
    this->length = length;

    int bytes = ceil(length, 8);

    for (int i = 0; i < bytes; ++i)
    {
        bitmap[i] = 0;
    }
}

bool BitMap::get(const int index) const
{
    int pos = index / 8;
    int offset = index % 8;

    return (bitmap[pos] & (1 << offset));
}

void BitMap::set(const int index, const bool status)
{
    int pos = index / 8;
    int offset = index % 8;

    // 清0
    bitmap[pos] = bitmap[pos] & (~(1 << offset));

    // 置1
    if (status)
    {
        bitmap[pos] = bitmap[pos] | (1 << offset);
    }
}

int BitMap::allocate(const int count)
{
    return allocateFirstFit(count);
    // return allocateBestFit(count);
}

int BitMap::allocateFirstFit(const int count) {
    if (count == 0)
        return -1;

    int index = 0;
    while (index < length) {
        // Skip over allocated resources
        while (index < length && get(index))
            ++index;

        // No continuous block of 'count' resources available
        if (index == length)
            return -1;

        // Found an unallocated resource, check for a continuous block of 'count' resources
        int empty = 0;
        int start = index;
        while (index < length && !get(index) && empty < count) {
            ++empty;
            ++index;
        }

        // If a continuous block of 'count' resources is found
        if (empty == count) {
            for (int i = 0; i < count; ++i) {
                set(start + i, true);
            }
            return start;
        }
    }

    return -1;
}

int BitMap::allocateBestFit(const int count) {
    if (count == 0)
        return -1;

    int bestStart = -1;
    int bestSize = 0x7FFFFFFF;
    int currentStart = -1;
    int currentSize = 0;

    for (int i = 0; i < length; ++i) {
        if (!get(i)) {
            if (currentStart == -1) {
                currentStart = i; // Start of a new free block
            }
            currentSize++;
        } else {
            if (currentStart != -1 && currentSize >= count && currentSize < bestSize) {
                bestStart = currentStart;
                bestSize = currentSize;
            }
            currentStart = -1;
            currentSize = 0;
        }
    }

    // Check the last block
    if (currentStart != -1 && currentSize >= count && currentSize < bestSize) {
        bestStart = currentStart;
        bestSize = currentSize;
    }

    if (bestStart != -1) {
        for (int i = 0; i < count; ++i) {
            set(bestStart + i, true);
        }
        return bestStart;
    }

    return -1;
}

void BitMap::release(const int index, const int count)
{
    for (int i = 0; i < count; ++i)
    {
        set(index + i, false);
    }
}

char *BitMap::getBitmap()
{
    return (char *)bitmap;
}

int BitMap::size() const
{
    return length;
}