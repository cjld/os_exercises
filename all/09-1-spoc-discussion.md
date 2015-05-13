# 文件系统(lec 21) spoc 思考题

## 个人思考题
### 文件系统和文件
 1. 文件系统的功能是什么？

>  负责数据持久保存，功能是数据存储和访问

>  具体功能：文件分配、文件管理、数据可靠和安全

 1. 什么是文件？

>  文件系统中具有符号名的基本数据单位。

### 文件描述符
 1. 打开文件时，文件系统要维护哪些信息？

>  文件指针、打开文件计数、访问权限、文件位置和数据缓存

 1. 文件系统的基本数据访问单位是什么？这对文件系统有什么影响？
 1. 文件的索引访问有什么特点？如何优化索引访问的速度？

### 目录、文件别名和文件系统种类
 1. 什么是目录？

>  由文件索引项组成的特殊文件。

 1. 目录的组织结构是什么样的？

>  树结构、有向图

 1. 目录操作有哪些种类？
 1. 什么是文件别名？软链接和硬链接有什么区别？
 1. 路径遍历的流程是什么样的？如何优化路径遍历？
 1. 什么是文件挂载？
 1. 为什么会存在大量的文件类型？

### 虚拟文件系统
 1. 虚拟文件系统的功能是什么？

>  对上对下的接口、高效访问实现

 1. 文件卷控制块、文件控制块和目录项的相互关系是什么？
 1. 可以把文件控制块放到目录项中吗？这样做有什么优缺点？


### 文件缓存和打开文件
 1. 文件缓存和页缓存有什么区别和联系？
 1. 为什么要同时维护进程的打开文件表和操作系统的打开文件表？这两个打开文件表有什么区别和联系？为什么没有线程的打开文件表？

### 文件分配
 1. 文件分配的三种方式是如何组织文件数据块的？各有什么特征？
 1. UFS多级索引分配是如何组织文件数据块的位置信息的？

### 空闲空间管理和冗余磁盘阵列RAID
 1. 硬盘空闲空间组织和文件分配有什么异同？
 1. RAID-0、1、4和5分别是如何组织磁盘数据块的？各有什么特征？

## 小组思考题
 1. (spoc)完成Simple File System的功能，支持应用程序的一般文件操作。具体帮助和要求信息请看[sfs-homework](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab8/sfs-homework.md)

 <https://github.com/cjld/ucore_lab/blob/master/related_info/lab8/sfs-homework.py>

 1. (spoc)FAT、UFS、YAFFS、NTFS这几种文件系统中选一种，分析它的文件卷结构、目录结构、文件分配方式，以及它的变种。
  wikipedia上的文件系统列表参考
  - http://en.wikipedia.org/wiki/List_of_file_systems
  - http://en.wikipedia.org/wiki/File_system
  - http://en.wikipedia.org/wiki/List_of_file_systems

  请同学们依据自己的选择，在下面链接处回复分析结果。
  - [https://piazza.com/class/i5j09fnsl7k5x0?cid=416 FAT文件系统分析]
  - [https://piazza.com/class/i5j09fnsl7k5x0?cid=417 NTFS文件系统分析]
  - [https://piazza.com/class/i5j09fnsl7k5x0?cid=418 UFS文件系统分析]
  - [https://piazza.com/class/i5j09fnsl7k5x0?cid=419 ZFS文件系统分析]
  - [https://piazza.com/class/i5j09fnsl7k5x0?cid=420 YAFFS文件系统分析]

  NTFS文件卷结构：
  NTFS卷启动扇区（Volume Boot Sector），NTFS系统（元数据）文件，主文件列表（MFT），分配单元（allocation units）。

  目录结构：
  多级（hierarchical）模型或目录树（directory tree）模型。目录树的“基（base）”是根（root）目录，NTFS系统的重要元数据文件之一。
  在根目录里，存储了指向其他文件或目录的引用，每个子目录里又可以有任意的文件和目录，这样就形成了一个树状结构。文件就是属性的集合，会自己
  包含需要的描述信息和数据。目录同样只包含自己的信息，而不用管其下的文件。
  每个目录在MFT里都有一个记录，它是目录信息的主要存储地。MFT里的记录存储了目录的如下属性：

  ```
  Header (H)：                         这是NTFS用来管理文件或目录的数据，包括NTFS内部使用的标识序列号，指向文件或目录属性的指针，和记录空闲空间的指针。注意Header不是一个属性，而是MFT记录的头信息。
  Standard Information Attribute (SI)：这个属性是文件或目录的“标准”信息，例如创建、修改、访问时间戳，以及文件的“标准”属性（只读，隐藏等）。
  File Name Attribute (FN)：           这个属性存储目录的名字。注意一个目录可以有多个名字属性，例如“常规”名字，MS-DOS兼容的短名字，或者类似POSIX的硬链接名字。
  Index Root Attribute：               这个属性包含了目录下所有文件的“标准”信息。如果文件数太多，那么就只包含部分文件的信息，其余的文件信息存储于外部的index buffer attribute里，后面会介绍。
  Index Allocation Attribute：         如果目录下的文件过多，上面的Index Root Attribute放不下，就会使用这个属性包含指向index buffer入口的指针。
  Security Descriptor (SD) Attribute： 包含目录及其内容的访问控制信息，或叫安全信息（security information）。目录的访问控制列表（ACLs ：Access Control Lists）和相关数据就存储于此。
  ```
  文件分配方式：

  ```
  1.         首先NTFS试图把整个文件放进MFT记录里。只有少数非常小的文件可能成功。
  2.         如果失败，data属性转化成非驻留的。MFT里的data属性只包含指向这些数据范围（extents，又叫runs）的指针。数据范围（extents）是指存储数据若干个连续的块， 位于MFT的外面。
  3.         如果文件太大，导致指向数据范围的指针也不能存储在MFT记录里，那么这些指针会变成非驻留的。这样的文件在主MFT记录（main MFT record）里没有data属性，而是有一个指向下一个MFT记录的指针，data属性在这个记录里，并存储指向数据范围的指针。
  4.         如果文件继续增大，NTFS会重复这种扩展，为超大的文件创建出无限个非驻留的MFT记录，当然，只要磁盘能够容纳。由此可见，文件越大，它的存储结构也会越复杂。
  ```
