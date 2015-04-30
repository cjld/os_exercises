# 同步互斥(lec 17) spoc 思考题


- 有"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的ucore_code和os_exercises的git repo上。

## 个人思考题

### 背景
 - 请给出程序正确性的定义或解释。
 - 在一个新运行环境中程序行为与原来的预期不一致，是错误吗？
 - 程序并发执行有什么好处和障碍？
 - 什么是原子操作？

### 现实生活中的同步问题

 - 家庭采购中的同步问题与操作系统中进程同步有什么区别？
 - 如何通过枚举和分类方法检查同步算法的正确性？
 - 尝试描述方案四的正确性。
 - 互斥、死锁和饥饿的定义是什么？

### 临界区和禁用硬件中断同步方法

 - 什么是临界区？
 - 临界区的访问规则是什么？
 - 禁用中断是如何实现对临界区的访问控制的？有什么优缺点？

### 基于软件的同步方法

 - 尝试通过枚举和分类方法检查Peterson算法的正确性。
 - 尝试准确描述Eisenberg同步算法，并通过枚举和分类方法检查其正确性。

### 高级抽象的同步方法

 - 如何证明TS指令和交换指令的等价性？
 - 为什么硬件原子操作指令能简化同步算法的实现？

## 小组思考题

1. （spoc）阅读[简化x86计算机模拟器的使用说明](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab7/lab7-spoc-exercise.md)，理解基于简化x86计算机的汇编代码。

了解了x86.py的使用方法, 并且阅读了程序`loop.s`和`looping-race-nolock.s`
几个参数如`-i`为中断频率, `-c`可以观察变量运行情况

loop.s 就是一个简单的使用寄存器的循环.

而`looping-race-nolock.s`则是在内存地址2000出记录了循环次数, 通过每次+1

2. （spoc)了解race condition. 进入[race-condition代码目录](https://github.com/chyyuu/ucore_lab/tree/master/related_info/lab7/race-condition)。

 - 执行 `./x86.py -p loop.s -t 1 -i 100 -R dx`， 请问`dx`的值是什么？

    dx值先初始化为0然后改为-1。

 - 执行 `./x86.py -p loop.s -t 2 -i 100 -a dx=3,dx=3 -R dx` ， 请问`dx`的值是什么？

    两个线程, Thread0先执行, Thread1后执行
    dx初始为3运行完4个循环后变为-1。

 - 执行 `./x86.py -p loop.s -t 2 -i 3 -r -a dx=3,dx=3 -R dx`， 请问`dx`的值是什么？

    两个线程以中断频率为3交替执行, 但因为修改只涉及寄存器, 所以运行结果和前者类似.

 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 1 -M 2000`, 请问变量x的值是什么？

    运行结束后为1

 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 2 -a bx=3 -M 2000`, 请问变量x的值是什么？为何每个线程要循环3次？

    第一个线程结束后为3, 第二个线程结束后为6, 循环三次因为循环变量b被重新赋值

 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 0`， 请问变量x的值是什么？

    可能是1也可能是2，若第二次读发生在第一次写后则为2，若第二次读发生在第一次写前则为1。

 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 1`， 请问变量x的值是什么？

    同上, seed似乎没有起到作用?

 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 2`， 请问变量x的值是什么？

     同上, seed似乎没有起到作用?

 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -a bx=1 -t 2 -M 2000 -i 1`， 请问变量x的值是什么？

    由于中断频率增加，这种情况下第二次读必然发生在第一次写之前，因此最终x值为1。

3. （spoc） 了解software-based lock, hardware-based lock, [software-hardware-lock代码目录](https://github.com/chyyuu/ucore_lab/tree/master/related_info/lab7/software-hardware-locks)

  - 理解flag.s,peterson.s,test-and-set.s,ticket.s,test-and-test-and-set.s 请通过x86.py分析这些代码是否实现了锁机制？请给出你的实验过程和结论说明。能否设计新的硬件原子操作指令Compare-And-Swap,Fetch-And-Add？

flag.s：多次使用命令./x86.py -p flag.s -t 2 -i 1 -R ax -c测试，可得count＝1情况，未实现锁机制。

peterson.s：多次使用命令./x86.py -p flag.s -t 2 -i 1 -R ax -c测试，可得count＝1情况，未实现锁机制。

test-and-set.s：使用了锁机制，通过自旋锁原理实现。

ticket.s：使用了锁机制，通过使获取允许进入临界区的线程号的操作成为原子操作实现。

test-and-test-and-set.s：使用了锁机制，通过使获取和修改互斥锁的值的操作成为原子操作实现。

关于能否设计硬件原子操作, 如果只有单核处理器还是可行的, 相当于在执行这条指令的时候
是不存在进程切换的.

但是多核的设计会相对更复杂, 有一些实现方法比如对总线加锁, 但是这种做法会严重影响并发度

```
Compare-And-Swap

int CompareAndSwap(int *ptr, int expected, int new) {
  int actual = *ptr;
  if (actual == expected)
    *ptr = new;
  return actual;
}
```

```
Fetch-And-Add

int FetchAndAdd(int *ptr) {
  int old = *ptr;
  *ptr = old + 1;
  return old;
}
```
