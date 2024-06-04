#include "memory.h"
#include "os_constant.h"
#include "stdlib.h"
#include "asm_utils.h"
#include "stdio.h"
#include "program.h"
#include "os_modules.h"

MemoryManager::MemoryManager()
{
    initialize();
}

void MemoryManager::initialize()
{
    this->totalMemory = 0;
    this->totalMemory = getTotalMemory();

    // 预留的内存
    int usedMemory = 256 * PAGE_SIZE + 0x100000;
    if (this->totalMemory < usedMemory)
    {
        printf("memory is too small, halt.\n");
        asm_halt();
    }
    // 剩余的空闲的内存
    int freeMemory = this->totalMemory - usedMemory;

    int freePages = freeMemory / PAGE_SIZE;
    int kernelPages = freePages / 2;
    int userPages = freePages - kernelPages;
    int virtualKernelPages = kernelPages * 2;
    
    int kernelPhysicalStartAddress = usedMemory;
    int userPhysicalStartAddress = usedMemory + kernelPages * PAGE_SIZE;

    int kernelPhysicalBitMapStart = BITMAP_START_ADDRESS;
    int userPhysicalBitMapStart = kernelPhysicalBitMapStart + ceil(kernelPages, 8);
    int kernelVirtualBitMapStart = userPhysicalBitMapStart + ceil(userPages, 8);

    int kernelPhysical_fifoQueue_Start = kernelVirtualBitMapStart + ceil(virtualKernelPages, 8);
    // int kernelPhysical_fifoQueue_Length = kernelPages;
    int kernelPhysical_fifoQueue_Length = 1024;

    int userPhysical_fifoQueue_Start = kernelPhysical_fifoQueue_Start + kernelPhysical_fifoQueue_Length * sizeof(int);
    // int userPhysical_fifoQueue_Length = userPages;
    int userPhysical_fifoQueue_Length = 1024;

    if ((uint32)(userPhysical_fifoQueue_Start + userPhysical_fifoQueue_Length) * sizeof(int) > (uint32)usedMemory)
    {
        printf("memory kept for bitmap and queue is not enough, halt.\n");
        asm_halt();
    }

    kernelPhysical.initialize(
        (char *)kernelPhysicalBitMapStart,
        kernelPages,
        kernelPhysicalStartAddress);

    userPhysical.initialize(
        (char *)userPhysicalBitMapStart,
        userPages,
        userPhysicalStartAddress);

    kernelVirtual.initialize(
        (char *)kernelVirtualBitMapStart,
        virtualKernelPages,
        KERNEL_VIRTUAL_START);

    kernelVirtualFIFOQueue.initialize(
        (int *)kernelPhysical_fifoQueue_Start,
        kernelPhysical_fifoQueue_Length);

    userVirtualFIFOQueue.initialize(
        (int *)userPhysical_fifoQueue_Start,
        userPhysical_fifoQueue_Length);

    printf("total memory: %d bytes ( %d MB )\n",
           this->totalMemory,
           this->totalMemory / 1024 / 1024);

    printf("kernel pool\n"
           "    start address: 0x%x\n"
           "    total pages: %d ( %d MB )\n"
           "    bitmap start address: 0x%x\n",
           kernelPhysicalStartAddress,
           kernelPages, kernelPages * PAGE_SIZE / 1024 / 1024,
           kernelPhysicalBitMapStart);

    printf("user pool\n"
           "    start address: 0x%x\n"
           "    total pages: %d ( %d MB )\n"
           "    bit map start address: 0x%x\n",
           userPhysicalStartAddress,
           userPages, userPages * PAGE_SIZE / 1024 / 1024,
           userPhysicalBitMapStart);

    printf("kernel virtual pool\n"
           "    start address: 0x%x\n"
           "    total pages: %d  ( %d MB ) \n"
           "    bit map start address: 0x%x\n",
           KERNEL_VIRTUAL_START,
           userPages, virtualKernelPages * PAGE_SIZE / 1024 / 1024,
           kernelVirtualBitMapStart);

    printf("kernel physical FIFO queue\n"
              "    start address: 0x%x\n"
              "    total pages: %d\n",
              kernelPhysical_fifoQueue_Start,
              kernelPhysical_fifoQueue_Length);

    printf("user physical FIFO queue\n"
              "    start address: 0x%x\n"
              "    total pages: %d\n",
              userPhysical_fifoQueue_Start,
              userPhysical_fifoQueue_Length);
}

int MemoryManager::allocatePhysicalPages(enum AddressPoolType type, const int count)
{
    int start = -1;

    if (type == AddressPoolType::KERNEL)
    {
        start = kernelPhysical.allocate(count);
    }
    else if (type == AddressPoolType::USER)
    {
        start = userPhysical.allocate(count);
    }

    return (start == -1) ? 0 : start;
}

void MemoryManager::releasePhysicalPages(enum AddressPoolType type, const int paddr, const int count)
{
    if (type == AddressPoolType::KERNEL)
    {
        kernelPhysical.release(paddr, count);
    }
    else if (type == AddressPoolType::USER)
    {

        userPhysical.release(paddr, count);
    }
}

int MemoryManager::getTotalMemory()
{

    if (!this->totalMemory)
    {
        int memory = *((int *)MEMORY_SIZE_ADDRESS);
        // ax寄存器保存的内容
        int low = memory & 0xffff;
        // bx寄存器保存的内容
        int high = (memory >> 16) & 0xffff;

        this->totalMemory = low * 1024 + high * 64 * 1024;
    }

    return this->totalMemory;
}

void MemoryManager::openPageMechanism()
{
    // 页目录表指针
    int *directory = (int *)PAGE_DIRECTORY;
    //线性地址0~4MB对应的页表
    int *page = (int *)(PAGE_DIRECTORY + PAGE_SIZE);

    // 初始化页目录表
    memset(directory, 0, PAGE_SIZE);
    // 初始化线性地址0~4MB对应的页表
    memset(page, 0, PAGE_SIZE);

    int address = 0;
    // 将线性地址0~1MB恒等映射到物理地址0~1MB
    for (int i = 0; i < 256; ++i)
    {
        // U/S = 1, R/W = 1, P = 1
        page[i] = address | 0x7;
        address += PAGE_SIZE;
    }

    // 初始化页目录项

    // 0~1MB
    directory[0] = ((int)page) | 0x07;
    // 3GB的内核空间
    directory[768] = directory[0];
    // 最后一个页目录项指向页目录表
    directory[1023] = ((int)directory) | 0x7;

    // 初始化cr3，cr0，开启分页机制
    asm_init_page_reg(directory);

    printf("open page mechanism\n");
}

int MemoryManager::allocatePages(enum AddressPoolType type, const int count) {
    // Allocate virtual pages
    int virtualAddress = allocateVirtualPages(type, count);
    if (!virtualAddress) {
        return 0;
    }

    int vaddress = virtualAddress;
    bool success_flg = true;

    // Allocate physical pages and set up mappings    
    for (int i = 0; i < count; ++i, vaddress += PAGE_SIZE) {
        int physicalPageAddress = allocatePhysicalPages(type, 1);

        // FIFO page replacement if no physica page is available
        if (!physicalPageAddress) {
            int page_addr_and_count = 0;
            if (type == AddressPoolType::KERNEL) {
                page_addr_and_count = kernelVirtualFIFOQueue.front();
            } else if (type == AddressPoolType::USER) {
                page_addr_and_count = userVirtualFIFOQueue.front();
            }

            int page_addr = page_addr_and_count & 0xfffff000;
            int page_count = (page_addr_and_count & 0x00000fff) + 1;

            releasePages(type, page_addr, page_count);

            physicalPageAddress = allocatePhysicalPages(type, 1);
        }

        // If still no physical page is available, release all resources
        if (!physicalPageAddress) {
            success_flg = false;
            break;
        }

        // Connect the virtual page to the physical page
        if (!connectPhysicalVirtualPage(vaddress, physicalPageAddress)) {
            success_flg = false;
            break;
        }
    }

    if (!success_flg) {
        releasePages(type, virtualAddress, count);
        releaseVirtualPages(type, virtualAddress, count);
        return 0;
    }

    int page_addr_and_count = 0;
    int virtualAddress_tmp = virtualAddress;

    for (int i = count; i > 0x1000; i -= 0x1000) {
        page_addr_and_count = virtualAddress_tmp | 0xfff;
        if (type == AddressPoolType::KERNEL) {
            kernelVirtualFIFOQueue.push(page_addr_and_count);
        } else if (type == AddressPoolType::USER) {
            userVirtualFIFOQueue.push(page_addr_and_count);
        }
        virtualAddress_tmp += 0x1000 * PAGE_SIZE;
    }
    page_addr_and_count = virtualAddress_tmp | (count - 1);
    if (type == AddressPoolType::KERNEL) {
        kernelVirtualFIFOQueue.push(page_addr_and_count);
    } else if (type == AddressPoolType::USER) {
        userVirtualFIFOQueue.push(page_addr_and_count);
    }
    
    return virtualAddress;
}

int MemoryManager::allocateVirtualPages(enum AddressPoolType type, const int count)
{
    int start = -1;

    if (type == AddressPoolType::KERNEL)
    {
        start = kernelVirtual.allocate(count);
    }

    return (start == -1) ? 0 : start;
}

bool MemoryManager::connectPhysicalVirtualPage(const int virtualAddress, const int physicalPageAddress)
{
    // 计算虚拟地址对应的页目录项和页表项
    int *pde = (int *)toPDE(virtualAddress);
    int *pte = (int *)toPTE(virtualAddress);

    // 页目录项无对应的页表，先分配一个页表
    if(!(*pde & 0x00000001)) 
    {
        // 从内核物理地址空间中分配一个页表
        int page = allocatePhysicalPages(AddressPoolType::KERNEL, 1);
        if (!page)
            return false;

        // 使页目录项指向页表
        *pde = page | 0x7;
        // 初始化页表
        char *pagePtr = (char *)(((int)pte) & 0xfffff000);
        memset(pagePtr, 0, PAGE_SIZE);
    }

    // 使页表项指向物理页
    *pte = physicalPageAddress | 0x7;

    return true;
}

int MemoryManager::toPDE(const int virtualAddress)
{
    return (0xfffff000 + (((virtualAddress & 0xffc00000) >> 22) * 4));
}

int MemoryManager::toPTE(const int virtualAddress)
{
    return (0xffc00000 + ((virtualAddress & 0xffc00000) >> 10) + (((virtualAddress & 0x003ff000) >> 12) * 4));
}

void MemoryManager::releasePages(enum AddressPoolType type, const int virtualAddress, const int count)
{
    int vaddr = virtualAddress;
    int *pte;
    for (int i = 0; i < count; ++i, vaddr += PAGE_SIZE)
    {
        // 第一步，对每一个虚拟页，释放为其分配的物理页
        releasePhysicalPages(type, vaddr2paddr(vaddr), 1);

        // 设置页表项为不存在，防止释放后被再次使用
        pte = (int *)toPTE(vaddr);
        *pte = 0;
    }

    // 第二步，释放虚拟页
    releaseVirtualPages(type, virtualAddress, count);

    int virtualAddress_tmp = virtualAddress;

    for (int i = count; i > 0x1000; i -= 0x1000) {
        if (type == AddressPoolType::KERNEL) {
            kernelVirtualFIFOQueue.earse(virtualAddress_tmp | 0xfff);
        } else if (type == AddressPoolType::USER) {
            userVirtualFIFOQueue.earse(virtualAddress_tmp | 0xfff);
        }
        virtualAddress_tmp += 0x1000 * PAGE_SIZE;
    }
    if (type == AddressPoolType::KERNEL) {
        kernelVirtualFIFOQueue.earse(virtualAddress_tmp | (count - 1));
    } else if (type == AddressPoolType::USER) {
        userVirtualFIFOQueue.earse(virtualAddress_tmp | (count - 1));
    }
}

int MemoryManager::vaddr2paddr(int vaddr)
{
    int *pte = (int *)toPTE(vaddr);
    int page = (*pte) & 0xfffff000;
    int offset = vaddr & 0xfff;
    return (page + offset);
}

void MemoryManager::releaseVirtualPages(enum AddressPoolType type, const int vaddr, const int count)
{
    if (type == AddressPoolType::KERNEL)
    {
        kernelVirtual.release(vaddr, count);
    }
}