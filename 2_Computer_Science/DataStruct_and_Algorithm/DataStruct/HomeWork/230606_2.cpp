#include"iostream"
#include"ctime"
#include"fstream"
#include"string"
#include<vector>
using namespace std;

unsigned int rand_seed = 0;

// 生成随机数
int rand()
{
    rand_seed = rand_seed * 214013 + 2531011;
    return rand_seed>>16&((1<<15)-1);
}

struct Box
{
	int Ancestor;//记录方格（树）的祖先
	int position;//记录方格的位置
	int Status[4];//记录四面墙的状态，开为 1，闭为 0
};

class Maze
{
public:
	Maze(int m, int n);//重载构造函数
	void CreateMaze();//构建迷宫
	void Search_Path(vector<Box>& BoxTeam);//寻找迷宫路径
	~Maze();
private:
	int row;//每行房间数
	vector<Box> MyMaze;//存储迷宫
	bool Path_In(vector<Box>& BoxTeam, Box& m);//查询迷宫中房间是否在迷宫路径中
	bool Is_Connect(Box& m, Box& n);//用于检查两个房间是否相连通，即是否在同一个集合（等价类）中
	int Find_Ancestor(Box& m, int& n);//查找集合并保留祖宗的位置
	void MergeBox(Box& m, Box& n);//将两个方格合并到一个集合中
};

Maze::Maze(int m, int n) :row(m), MyMaze(m* n) //重载构造函数，初始化迷宫类
{
	int s = MyMaze.size();//迷宫中方格的数量
	if (s == 0)
		return;
	for (int i = 0; i < s; i++)
	{
		MyMaze[i].Ancestor = -1;//所有祖先都置为-1
		MyMaze[i].position = i;//位置保持对应
		for (int b = 0; b < 4; b++)
			MyMaze[i].Status[b] = 0;//0 为闭
		MyMaze[0].Status[2] = 1;//设置迷宫入口和出口，左上进，右下出
		MyMaze[s - 1].Status[0] = 1;
	}
}

//创建迷宫，随机生成可由入口到出口的迷宫，不断拆墙合并房间，直到所有房间都在一个等价类（集合）中，即可由入口到出口，迷宫创建完成
void Maze::CreateMaze()
{
	int s = MyMaze.size(); //迷宫中方格的数量
	if (s <= 0) return; //迷宫中没有方格
	int p, w; //p 为随机生成的方格位置，w 为随机生成的方向
	int pos; //记录祖先的位置，祖先即为集合的代表，用于判断是否所有方格都在一个集合中

	srand(0);//随机种子
	while (1)
	{
		p = rand() % s; //随机生成方格位置
		w = rand() % 4; //随机生成方向，也就是随机拆除哪面墙，0 为右，1 为下，2 为左，3 为上
		switch (w)
		{
		case 0: //右端，p 为方格位置，p+1 为右边的方格位置，判断这两个方格是否相连通（同一个祖先，同个等价类），如果不相连通，则拆除右边的墙。
        //根据注释补全代码
            //若p为最右边的方格，则不需要拆除右边的墙
            if (p % row == row - 1)
                break;
            //使用is_Connect函数判断两个方格是否相连通，若p与右边的方格相连通，则不需要拆除右边的墙
            if (Is_Connect(MyMaze[p], MyMaze[p + 1]))
                break;
            //若p与右边的方格不相连通，则拆除右边的墙，使用MergeBox函数将两个方格合并为一个集合
            MergeBox(MyMaze[p], MyMaze[p + 1]);
            //将p的右边的墙置为1，将右边方格的左边的墙置为1，表示两个方格相连通，墙已拆除
            MyMaze[p].Status[0] = 1;
            MyMaze[p + 1].Status[2] = 1;
			break;

		case 1: //下端，p 为方格位置，p+row 为下边的方格位置，判断这两个方格是否相连通（同一个祖先，同个等价类），如果不相连通，则拆除下边的墙。
        //根据注释补全代码
            //若p为最下边的方格，则不需要拆除下边的墙
            if (p >= s - row)
                break;
            //使用is_Connect函数判断两个方格是否相连通，若p与下边的方格相连通，则不需要拆除下边的墙
            if (Is_Connect(MyMaze[p], MyMaze[p + row]))
                break;
            //若p与下边的方格不相连通，则拆除下边的墙，使用MergeBox函数将两个方格合并为一个集合
            MergeBox(MyMaze[p], MyMaze[p + row]);
            //将p的下边的墙置为1，将下边方格的上边的墙置为1，表示两个方格相连通，墙已拆除
            MyMaze[p].Status[1] = 1;
            MyMaze[p + row].Status[3] = 1;
			break;

		case 2: //左端，p 为方格位置，p-1 为左边的方格位置，判断这两个方格是否相连通（同一个祖先，同个等价类），如果不相连通，则拆除左边的墙。
        //根据注释补全代码
            //若p为最左边的方格，则不需要拆除左边的墙
            if (p % row == 0)
                break;
            //使用is_Connect函数判断两个方格是否相连通，若p与左边的方格相连通，则不需要拆除左边的墙
            if (Is_Connect(MyMaze[p], MyMaze[p - 1]))
                break;
            //若p与左边的方格不相连通，则拆除左边的墙，使用MergeBox函数将两个方格合并为一个集合
            MergeBox(MyMaze[p], MyMaze[p - 1]);
            //将p的左边的墙置为1，将左边方格的右边的墙置为1，表示两个方格相连通，墙已拆除
            MyMaze[p].Status[2] = 1;
            MyMaze[p - 1].Status[0] = 1;
			break;

		case 3: //上端，p 为方格位置，p-row 为上边的方格位置，判断这两个方格是否相连通（同一个祖先，同个等价类），如果不相连通，则拆除上边的墙。
        //根据注释补全代码
            //若p为最上边的方格，则不需要拆除上边的墙
            if (p < row)
                break;
            //使用is_Connect函数判断两个方格是否相连通，若p与上边的方格相连通，则不需要拆除上边的墙
            if (Is_Connect(MyMaze[p], MyMaze[p - row]))
                break;
            //若p与上边的方格不相连通，则拆除上边的墙，使用MergeBox函数将两个方格合并为一个集合
            MergeBox(MyMaze[p], MyMaze[p - row]);
            //将p的上边的墙置为1，将上边方格的下边的墙置为1，表示两个方格相连通，墙已拆除
            MyMaze[p].Status[3] = 1;
            MyMaze[p - row].Status[1] = 1;
			break;
		}
		if (Find_Ancestor(MyMaze[0], pos) == (-1 * s))//所有的方格都在一个集合中，即所有方格都相连通，迷宫生成完毕
			break;
	}
};

bool Maze::Is_Connect(Box& m, Box& n)//查看两个方格是否相连通，即是否在同一个集合中，即是否有相同的祖先，即是否在同一个等价类中
{

	int p, q; //p，q 为方格所在的位置
    //根据注释补全代码
    //使用Find_Ancestor函数寻找方格所在的集合以及祖先所在的位置
    Find_Ancestor(m, p);
    Find_Ancestor(n, q);
    if (p == q) 
        return true;
    else
        return false; 
}

//寻找方格所在的集合以及祖先所在的位置，即寻找等价类,并返回祖先所在的位置
int Maze::Find_Ancestor(Box& m, int& n)
{
	int s = m.Ancestor; //s 为祖先所在的位置
	n = m.position; //n 为方格所在的位置
	if (s >= 0)
		s = Find_Ancestor(MyMaze[s], n);
	return s;
};

//合并同一祖先的方格，即合并等价类
void Maze::MergeBox(Box& m, Box& n) //若拆墙后连通，合并为一个等价类
{
	int s1, s2, p1, p2;
	s1 = Find_Ancestor(m, p1);
	s2 = Find_Ancestor(n, p2);
	if (s1 <= s2)//若 s1（m）的祖先深度小于等于 s2（n）的祖先深度,则把 s1（m）的祖先指向 s2（n）,并把 s2（n）的祖先深度加到 s1（m）的祖先深度上
	{
		MyMaze[p1].Ancestor += MyMaze[p2].Ancestor;//s1（m）的祖先深度加到 s2（n）的祖先深度上,
		MyMaze[p2].Ancestor = m.position;//s2（n）的祖先指向 s1（m）
	}
	else
	{ //若 s1（m）的祖先深度大于 s2（n）的祖先深度,则把 s2（n）的祖先指向 s1（m）,并把 s1（m）的祖先深度加到 s2（n）的祖先深度上
		//补全代码,思路同上
        MyMaze[p2].Ancestor += MyMaze[p1].Ancestor;
        //补全代码,思路同上
        MyMaze[p1].Ancestor = n.position;
	}
};

//深度优先搜索寻找最短路径
void Maze::Search_Path(vector<Box>& BoxTeam)
{
    int s = MyMaze.size();
    if (BoxTeam.size() == 0)
        BoxTeam.push_back(MyMaze[0]);//vector 的 push_back 操作是将一个元素插入vector 的末尾，也就是把入口压入栈
    int i = 0;
    while (i < 4)//对四个门进行操作
    {
        switch (i)
        {
            case 0:
                if (BoxTeam.back().position == (s - 1))//已经到了最后一个，则退出
                    break;
                if (BoxTeam.back().Status[i] == 1)
                {
                    BoxTeam.push_back(MyMaze[BoxTeam.back().position + 1]);//若i = 0，右边一个入栈 BoxTeam
                    BoxTeam.back().Status[2] = 0;
                    Search_Path(BoxTeam);
                }
                break;
            case 1:
                if (BoxTeam.back().position == (s - 1))
                    break;
                if (BoxTeam.back().Status[i] == 1)
                {
                    BoxTeam.push_back(MyMaze[BoxTeam.back().position + row]);//若 i = 1，下面一个入栈 BoxTeam
                    BoxTeam.back().Status[3] = 0;
                    Search_Path(BoxTeam);
                }
                break;
            case 2:
                if (BoxTeam.back().position == (s - 1))
                    break;
                if (BoxTeam.back().Status[i] == 1)
                {
                    BoxTeam.push_back(MyMaze[BoxTeam.back().position - 1]);//若i = 2, 左边一个入栈 BoxTeam
                    BoxTeam.back().Status[0] = 0;
                    Search_Path(BoxTeam);
                }
                break;
            case 3:
                if (BoxTeam.back().position == (s - 1))
                    break;
                if (BoxTeam.back().Status[i] == 1)
                {
                    BoxTeam.push_back(MyMaze[BoxTeam.back().position - row]);//若 i = 3，上面一个入栈 BoxTeam
                    BoxTeam.back().Status[1] = 0;
                    Search_Path(BoxTeam);
                }
                break;
        }
        if (BoxTeam.back().position == (s - 1))//若刚刚好结束，则退出
            break;
        i++;//计数
    }
    if (i == 4)
        BoxTeam.pop_back();//删除 vector 中最后一个元素，也就是在四面不通的时候出栈
};


Maze::~Maze()
{ }
//查询迷宫中房间是否在迷宫路径中
bool Maze::Path_In(vector<Box>& BoxTeam, Box& m)
{
    vector<Box>::iterator iter = BoxTeam.begin();//使用容器的迭代器来遍历整个容器
    while (iter != BoxTeam.end())
    {
        if (iter->position == m.position)
            return true;
        iter++;
    }
    return false;
};

int main()
{
	int m, n; cin >> n >> m; //数据迷宫矩阵单元的行数和列数
	Maze M(m, n); //创建一个 m 行 n 列的迷宫类
	M.CreateMaze(); //生成所有方格均在一个等价类中的迷宫
	vector<Box> BoxTeam; //创建一个 vector 容器，用来存储迷宫路径
	M.Search_Path(BoxTeam); //寻找迷宫路径
	int i = 0;
	while (i < BoxTeam.size()) //输出迷宫路径
	{
		cout << BoxTeam[i].position << ' ';
		i++;
	}
	cout << endl;
	return 0;
}