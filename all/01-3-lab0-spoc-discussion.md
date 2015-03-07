# lab0 SPOC思考题

## 个人思考题

---

能否读懂ucore中的AT&T格式的X86-32汇编语言？请列出你不理解的汇编语言。
- [x]  

>  对于常用指令有了解, 对于不了解的需要参考网上资料

虽然学过计算机原理和x86汇编（根据THU-CS的课程设置），但对ucore中涉及的哪些硬件设计或功能细节不够了解？
- [x]  

>   对大多数IO设备都不太了解, 在之前只接触过串口和VGA, 而且VGA还是使用硬件实现的

请给出你觉得的中断的作用是什么？使用中断有何利弊？
- [x]  

>   CPU暂停当前正在执行的程序，转而执行处理该事件的一个程序. 利弊是中断会打断当前程序, 当中断被再次被中断时情况会复杂很多

哪些困难（请分优先级）会阻碍你自主完成lab实验？
- [x]  

> 遇到不可重现的bug, 而且系统过于庞大无法调试

如何把一个在gdb中或执行过程中出现的物理/线性地址与你写的代码源码位置对应起来？
- [x]  

>   在gdb中可查看物理地址和行号

了解函数调用栈对lab实验有何帮助？
- [x]  

> 理解函数调用过程, ucore的从上到下的架构

你希望从lab中学到什么知识？
- [x]  

> 了解每个lab中使用到的技术, 如内存管理, 进程控制, 文件系统种种.

---

## 小组讨论题

---

搭建好实验环境，请描述碰到的困难和解决的过程。
- [x]  

> 困难：在virtualbox中设置虚拟机的时候找不到Linux的64位选项 解决：需要通过BIOS设置将电脑的虚拟化功能打开，如果不设置成64位，不能正常启动。在正常启动后，内存要设置较大，否则启动缓慢

熟悉基本的git命令，从github上（http://www.github.com/chyyuu/ucore_lab）下载ucore lab实验
- [x]  

> 完成

尝试用qemu+gdb（or ECLIPSE-CDT）调试lab1
- [x]  

> 完成


对于如下的代码段，请说明”：“后面的数字是什么含义
```
/* Gate descriptors for interrupts and traps */
struct gatedesc {
    unsigned gd_off_15_0 : 16;        // low 16 bits of offset in segment
    unsigned gd_ss : 16;            // segment selector
    unsigned gd_args : 5;            // # args, 0 for interrupt/trap gates
    unsigned gd_rsv1 : 3;            // reserved(should be zero I guess)
    unsigned gd_type : 4;            // type(STS_{TG,IG32,TG32})
    unsigned gd_s : 1;                // must be 0 (system)
    unsigned gd_dpl : 2;            // descriptor(meaning new) privilege level
    unsigned gd_p : 1;                // Present
    unsigned gd_off_31_16 : 16;        // high bits of offset in segment
};
```
- 表示数据所占的位数。  

> 

对于如下的代码段，
```
#define SETGATE(gate, istrap, sel, off, dpl) {            \
    (gate).gd_off_15_0 = (uint32_t)(off) & 0xffff;        \
    (gate).gd_ss = (sel);                                \
    (gate).gd_args = 0;                                    \
    (gate).gd_rsv1 = 0;                                    \
    (gate).gd_type = (istrap) ? STS_TG32 : STS_IG32;    \
    (gate).gd_s = 0;                                    \
    (gate).gd_dpl = (dpl);                                \
    (gate).gd_p = 1;                                    \
    (gate).gd_off_31_16 = (uint32_t)(off) >> 16;        \
}
```
如果在其他代码段中有如下语句，
```
unsigned intr;
intr=8;
SETGATE(intr, 0,1,2,3);
```
请问执行上述指令后， intr的值是多少？
- 运行程序计算，答案为65538。

> 

请分析 [list.h](https://github.com/chyyuu/ucore_lab/blob/master/labcodes/lab2/libs/list.h)内容中大致的含义，并能include这个文件，利用其结构和功能编写一个数据结构链表操作的小C程序
list是一通用的双向链表，提供添加，删除，更改的操作。尝试建立了一种新的数据结构test，然后提供了其的添加，删除查找等操作，代码如下

    #include "list.h"
    struct test
    {
        list_entry *entry;
        int data;
        test()
        {
            entry = (list_entry*)malloc(sizeof(list_entry));
            list_init(entry);
        }
    };

    int main() {
        test *t1 = new test();
        test *t2 = new test();
        list_add(t1->entry, t2->entry);
        list_delete(t1->entry);
        list_empty(t1->list);
        test *next = (test*)(list_next(t1->entry));
        test *prev = (test*)(list_prev(t2->prev));
        return 0;
    }

> 
---

## 开放思考题

---

是否愿意挑战大实验（大实验内容来源于你的想法或老师列好的题目，需要与老师协商确定，需完成基本lab，但可不参加闭卷考试），如果有，可直接给老师email或课后面谈。
- [x]  

>  

---
