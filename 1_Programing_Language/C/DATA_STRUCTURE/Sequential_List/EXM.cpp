https://www.jianshu.com/p/a1d8329e8292



#include<iostream> //malloc函数因为常用，被包含在iostream中，C++可以直接使用。
//#include<stdlib.h> malloc是C语言的申请内存函数。其包含在stdliib.h头文件中。
using namespace std;
int main(){
    //使用: 数据类型 * 指针变量名 = (数据类型 *) malloc (大小 * sizeof(数据类型) );
    //注意强制转换和sizeof获取数据类型所需要的空间大小。
    //例如int * p = (int *) malloc (sizeof(int)) ; 申请一个int类型的数据
    int * p = (int *) malloc ( 10 * sizeof(int) );//申请一个int类型的数组。空间大小为10
    for(int i=0;i<10;i++){
        p[i] = i;
    }
    for (int i = 0; i < 10; i++){
        cout<<p[i]<<endl;
    }
    free(p);
    system("PAUSE");
}

#include<iostream> //realloc函数因为常用，被包含在iostream中，C++可以直接使用。
//#include<stdlib.h> realloc是C语言的动态内存调整函数。其包含在stdliib.h头文件中。
using namespace std;
int main(){
    //使用: 数据类型 * 指针变量名 = (数据类型 *) realloc (需要调整空间的指针名 ,大小 * sizeof(数据类型) );
    //注意强制转换和sizeof获取数据类型所需要的空间大小。以及调整空间的指针名。
    int * p = (int *) malloc ( 10 * sizeof(int) );//申请一个int类型的数组。空间大小为10
    for(int i=0;i<10;i++){
        p[i] = i;
    }//放入10个数据
    //动态调整空间:扩容
    p = (int *) realloc ( p, 20 * sizeof(int));//扩容。再增加10个空间。
    for (int i = 10; i < 20; i++){
        p[i] = i;
    }
    //输出
    for (int i = 0; i < 20; i++){
        cout<<p[i]<< " ";
    }
    cout<<endl;//回车
    //动态调整空间:缩小
    p = (int *) realloc (p ,10 * sizeof(int) );//缩小。回归到10个空间大小，会引发数据被丢失
    //输出
    for (int i = 0; i < 20; i++){//继续循环到20个，会引发错误。
        cout<<p[i]<<" ";
    }
    cout<<endl;//回车
    free(p);
    system("PAUSE");
}



     /**
     * 动态顺序表类
     */ 
    template<typename T>
    class List : public ListSelf<T>{//List : 动态顺序表类 继承 顺序存储结构抽象类(ListSelf)
        private:
            const size_t SIZE = 10L;
            T * data;//数据首地址
            size_t length ;//数据长度大小
            size_t storage;//整体大小
            //核心函数
            /**
             * 扩容函数
             */
            Status addStorage(T elem,size_t index){
                const size_t len = length != 0 ? 2 * length : 1;
                //利用三元运算符，如果原大小为0，则分配为1
                //否则分配原大小的两倍

                //分配内存
                T * newData = new T[len];
                if (!newData){
                    return FAIL;
                }

                //移动数据
                size_t i = 0;
                for (i = 1; i < index ; i++){//先移动前面的数据
                    newData[i] = data[i];//移动数据
                }

                //再将需要插入的输入放入新的内存数据中
                newData[index] = elem;
                ++length;//长度增加

                //再次移动后面的数据
                size_t m = 0; 
                for ( m = i; m < length; m++){
                    newData[m+1] = data[m];
                }
                
                //释放原来的数据空间
                //delete []data;不知道为什么，这边不能释放data。释放的话会造成严重的内存错误

                //调整更新
                data = newData;
                storage = len;
                return SUCCESS;
            }
        protected:
            /**
             * 构造一个线性表,申请内存
             */
            Status init(){
                data = new T[SIZE+1];//多申请一个空间,空余出第一个数据空间,默认大小为11
                length = 0;//长度为0
                storage = SIZE;//整体长度默认大小为11
                if (!data){
                    exit(ERROR);//如果内存申请失败，退出
                }
                return SUCCESS;
            }

            /**
             * 销毁线性表，回收内存。
             */ 
            Status destroy(){
                if (!data){
                    return FAIL;
                }
                delete []data;
                return SUCCESS;
            } 
        public:
            /**
             * 默认的构造函数
             */
            List(){
               init(); 
            }
            /**
             * 析构函数
             */
            ~List(){
                destroy();
            } 

             /**
             * 在相应的位置上插入新的数据
             */ 
            Status insert(T elem,size_t index){
                if(index < 1 || index > length+1 ){//判断下标是否合法
                    return ARRAY_OUT_OF_BOUNDS;//返回下标越界错误
                } 
                if (storage == length){ //判断空间是否满了
                    return addStorage(elem,index);
                }
                size_t i = 0;
                for (i = length; i >= index; --i){//将数据往后面移动
                    data[i+1] = data[i];//将数据往后移动
                }
                data[i+1] = elem;//插入数据
                ++length;//长度增加
                return SUCCESS; 
            }

            /**
             * 在线性表的末尾插入新的数据 
             */
            Status insert(T elem){
                if (storage == length){ //判断空间是否满了
                    return addStorage(elem,length);
                }
                data[++length] = elem;//放入数据
                return SUCCESS;
            }

            /**
             * 返回整体容量大小
             */
            size_t capacity(){
                return storage;
            }

            /**
             * 取出线性表的数据元素
             */ 
            T at(size_t index){
                if(index < 1 || index > length){
                    throw std::out_of_range("Array out of bounds");//返回下标越界错误
                }
                return data[index];
            }

            /**
             * 返回数据的索引下标
             */  
            int local(T elem) {
                //安排哨兵
                data[0] = elem;
                size_t i= 0;
                for(i = length;data[i]!=elem;--i);//查询位置。数据相等就退出。
                if (i == 0){
                    return -1;//查找失败，返回-1
                }
                return i;//返回位置
            }

            /**
             * 修改指定位置的数据
             */ 
            Status updateIndex(T newElem,size_t index){
                if(index < 1 || index > length ){
                    return ARRAY_OUT_OF_BOUNDS;//返回数组下标错误
                }
                data[index] = newElem;//修改数据
                return SUCCESS;//返回成功
            }

            /**
             * 修改匹配的数据
             */
            Status update(T oldElem,T newElem){
                int index = local(oldElem);//先查询老数据的位置
                if (index == -1){
                    return FAIL;//如果没有查询到，就修改错误
                }
                data[index] = newElem;//更新数据 
                return SUCCESS;//返回成功
            }

            /**
             * 在相应的位置上删除数据
             */ 
            Status removeIndex(size_t index){
                if(index < 1 || index > length ){
                    return ARRAY_OUT_OF_BOUNDS;//返回数组下标错误
                }
                for (size_t i = index; i <= length; ++i){//数据往前面移动，覆盖掉原来的数据
                    data[i] = data[i+1];
                }
                --length;//长度减一
                return SUCCESS;
            }

            /**
             * 移除线性表中相同的元素
             */ 
            Status remove(T elem){
                int index = local(elem);//先查询数据的位置
                if(index == -1){
                    return FAIL;//没有数据就返回假
                }
                for (size_t i = index; i < length; ++i){//同removeIndex()
                    data[i] = data[i+1];
                }
                --length;
                return SUCCESS;
            }

            /**
             * 返回查找元素的直接前驱
             */ 
            T * prior(T elem){
                if (data[0] == elem){
                    return NULL;//第一个元素没有直接前驱
                }
                int index = local(elem);
                if(index == -1){
                    return NULL;//没有前驱返回空
                }
                return &data[index-1];
            }

            /**
             * 返回查找元素的直接后驱
             */ 
            T * next(T elem){
                if (elem == data[length]){
                    return NULL;//最后一个数据没有
                }
                int index = local(elem);
                if (index == -1){
                    return NULL;
                }
                return &data[index+1];
            }

            /**
             * 返回线性表中元素的个数
             */ 
            size_t size(){
                return length;
            }

            /**
             * 将线性表重置为空表，清空所有数据
             */ 
            void clear(){
                length = 0;//直接长度清空即可
            }

            /**
             * 判断线性表是否为空表，如果是空表，返回true，否则返回false
             */ 
            bool isEmpty(){
                return length==0;
            }

            /**
             * 遍历线性表
             */ 
            Status show(){
                for (size_t i = 1; i <= length; i++){
                    std::cout<<"data["<<i<<"]="<<data[i]<<"\n";
                }
                return SUCCESS;
            }
    };
