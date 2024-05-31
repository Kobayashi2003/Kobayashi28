#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"
#include "sync.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;

Semaphore chopstick[5];


void philosopher_thread(void *arg)
{
    int id = (int)arg;
    int left = id;
    int right = (id + 1) % 5;

    while (true)
    {

        if (chopstick[left].available() && chopstick[right].available())
        {
            printf("philosopher %d pick up the left chopstick\n", id);
            chopstick[left].P();
            for (int i = 0; i < 1e5; ++i)
            {
                /* do nothing */
            }
            printf("philosopher %d pick up the right chopstick\n", id);
            chopstick[right].P();
        }
        else
        {
            continue;
        }

        printf("philosopher %d is eating\n", id);

        chopstick[left].V();
        chopstick[right].V();

        printf("philosopher %d is thinking\n", id);
    }
}


void first_thread(void *arg)
{
    // 第1个线程不可以返回
    stdio.moveCursor(0);
    for (int i = 0; i < 25 * 80; ++i)
    {
        stdio.print(' ');
    }
    stdio.moveCursor(0);

    for (int i = 0; i < 5; ++i)
    {
        chopstick[i].initialize(1);
    }

    for (int i = 0; i < 5; ++i)
    {
        programManager.executeThread(philosopher_thread, (void *)i, "philosopher thread", 1);
    }

    asm_halt();
}

extern "C" void setup_kernel()
{

    // 中断管理器
    interruptManager.initialize();
    interruptManager.enableTimeInterrupt();
    interruptManager.setTimeInterrupt((void *)asm_time_interrupt_handler);

    // 输出管理器
    stdio.initialize();

    // 进程/线程管理器
    programManager.initialize();

    // 创建第一个线程
    int pid = programManager.executeThread(first_thread, nullptr, "first thread", 1);
    if (pid == -1)
    {
        printf("can not execute thread\n");
        asm_halt();
    }

    ListItem *item = programManager.readyPrograms.front();
    PCB *firstThread = ListItem2PCB(item, tagInGeneralList);
    firstThread->status = RUNNING;
    programManager.readyPrograms.pop_front();
    programManager.running = firstThread;
    asm_switch_thread(0, firstThread);

    asm_halt();
}
