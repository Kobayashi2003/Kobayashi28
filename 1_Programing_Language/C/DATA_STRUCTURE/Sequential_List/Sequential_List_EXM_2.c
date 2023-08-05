//SeqList.h
#pragma once

#include<stdio.h>
#include<assert.h>
#include<malloc.h>


typedef int ElemType;


typedef struct SeqList {
	ElemType* data;
	int size;			//	有效数据的个数
	int capacity;		//	数组的容量
}SeqList;

void SeqListInit(SeqList* ps);
void SeqListDestory(SeqList* ps);

void SeqListPrint(SeqList* ps);
void SeqListPushBack(SeqList* ps, ElemType x);
void SeqListPushFront(SeqList* ps, ElemType x);
void SeqListPopFront(SeqList* ps);
void SeqListPopBack(SeqList* ps);
int SeqListFind(SeqList* ps, ElemType x);
void SeqListInsert(SeqList* ps, size_t pos, ElemType x);
void SeqListErase(SeqList* ps, size_t pos);


#include"SeqList.h"
void SeqListInit(SeqList* ps) {
	assert(ps);
	ps->data = NULL;
	ps->capacity = 0;
	ps->size = 0;
}

void SeqListDestory(SeqList* ps) {
	assert(ps);
	SeqListInit(ps);
	free(ps);
}

void SeqListPrint(SeqList* ps) {
	assert(ps);
	int i = 0;
	for (i = 0; i < ps->size; i++) {
		printf("%d ", ps->data[i]);
	}
}
void IsFull(SeqList* ps) {
	if (ps->size == ps->capacity) {
		ps->capacity = (ps->capacity > 0 ? 2 * ps->capacity : 4);
		ps->data = (ElemType*)realloc(ps->data, ps->capacity * sizeof(ElemType));
	}
}

void SeqListPushBack(SeqList* ps, ElemType x) {
	assert(ps);
	IsFull(ps);
	ps->size++;
	ps->data[ps->size - 1] = x;
}

void SeqListPushFront(SeqList* ps, ElemType x) {
	assert(ps);
	IsFull(ps);
	int i = 0;
	for (i = ps->size ; i > 0; i--) {
		ps->data[i] = ps->data[i - 1];
	}
	ps->size++;
	ps->data[0] = x;
}

void SeqListPopFront(SeqList* ps) {
	assert(ps);
	IsFull(ps);
	int i = 0;
	for (i = 0; i < ps->size - 1; i++) {
		ps->data[i] = ps->data[i + 1];
	}
	ps->size--;
}

void SeqListPopBack(SeqList* ps) {
	assert(ps);
	IsFull(ps);
	ps->size--;
}

int SeqListFind(SeqList* ps, ElemType x) {
	assert(ps);
	int i = 0;
	for (i = 0; i < ps->size; i++) {
		if (x == ps->data[i]) {
			return i;
		}
	}
	return -1;
}

void SeqListInsert(SeqList* ps, size_t pos, ElemType x) {
	assert(ps);
	IsFull(ps);
	int i = 0;
	for (i = ps->size; i > pos; i--) {
		ps->data[i] = ps->data[i - 1];
	}
	ps->data[pos] = x;
	ps->size++;
}

void SeqListErase(SeqList* ps, size_t pos) {
	assert(ps);
	int i = 0;
	for (i = pos; i < ps->size - 1; i++) {
		ps->data[i] = ps->data[i + 1];
	}
	ps->size--;
}
