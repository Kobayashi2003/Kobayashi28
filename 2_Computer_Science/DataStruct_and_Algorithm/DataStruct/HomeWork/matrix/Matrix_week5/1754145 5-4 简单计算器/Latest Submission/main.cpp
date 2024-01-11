#include <iostream>
#include <string>
#include <cstring>
using namespace std;
char a[100];
char fz[100]; // 符号栈 
int sz[100]; // 数字栈 
int fhead = 0; // 符号栈指针 
int shead = 0; // 数字栈指针 

void math(char f, int & shead, int & fhead) // 从数字栈中取出栈顶的两个数字 进行 f 运算 结果继续放在栈中 
{
	switch (f)
	{
	case '+': 
		shead -= 1;
		sz[shead] += sz[shead + 1]; 
		break;
	case '-': 
		shead -= 1;
		sz[shead] -= sz[shead + 1];
		break;
	case '*':
		shead -= 1;
		sz[shead] *= sz[shead + 1]; 
		break;
	case '/': 
		shead -= 1;
		sz[shead] /= sz[shead + 1]; 
		break;
	}
	--fhead;
	sz[shead + 1] = 0;
}

int main()
{
	cin.getline(a, 100);
	int len = strlen(a) - 1;
	for (int i = 0; i <= len; ++i)
	{
		// 如果读到 "("  则直接放入栈中 
		if (a[i] == '(') {
			fz[++fhead] = a[i];
			continue;
		}
		// 如果读到 ")"  则将 "(" 之前的运算符全部出栈 
		if (a[i] == ')') {
			while (fz[fhead] != '(')
				math(fz[fhead],shead,fhead);
			--fhead;
			continue;
		}
		// 读到数字直接放在数字栈顶就ok啦 
		if (a[i] >= '0' && a[i] <= '9') {
			++shead;
			while (a[i] >= '0' && a[i] <= '9')
				sz[shead] = sz[shead] * 10 + a[i] - '0', i++;
			i--;
			continue;
		}
		else {
			if(a[i] == '-' && a[i - 1] == '(') {
				++shead;
				sz[shead] = 0;
				fz[++fhead] = a[i];
				continue;
			}
			else if (a[i] == '/' || a[i] == '*') {
				// 如果读到 "/" 或 "*"  直接放在符号栈栈顶 
				fz[++fhead] = a[i];
				continue;
			}
			else
				while (fz[fhead] == '*' || fz[fhead] == '/' || fz[fhead] == a[i]) {
					// 如果读到 "+" 或 "-"  
					// 则将栈顶跟自己一样的符号和 "/"  "*" 全部弹出
					// 这个可以手动列几个式子体会一下 (^-^) 
					math(fz[fhead], shead, fhead);
				}
			fz[++fhead] = a[i];
		}
	}
	while (fhead != 0) {
		math(fz[fhead], shead, fhead);
	}
	// 当栈中仅有一个数字的时候 运算式的答案就是它啦 
	cout << sz[shead];
	return 0;
}