#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;

int source;

void producer_thread(void *arg)
{
    printf("producer_thread start\n");

    for (int i = 0; i < 1e5; ++i)
    {
        int temp = source;
        for (int i = 0; i < 1e3; ++i)
        {
            /* do nothing */
        }
        source = temp + 1;
    }

    printf("producer_thread end\n");
}

void consumer_thread(void *arg)
{
    printf("consumer_thread start\n");

    for (int i = 0; i < 1e5; ++i)
    {
        int temp = source;
        for (int i = 0; i < 1e3; ++i)
        {
            /* do nothing */
        }
        source = temp - 1;
    }

    printf("consumer_thread end\n");
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

    source = 0;
    
    for (int i = 0; i < 5; ++i) {
        programManager.executeThread(producer_thread, nullptr, "producer thread", 1);
        programManager.executeThread(consumer_thread, nullptr, "consumer thread", 1);
    }

    while (programManager.readyPrograms.size() > 1) { /* do nothing */ }
    printf("source = %d\n", source);

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
