
class mem_node:
    def __init__(self, start, size):
        self.start = start
        self.size = size
        self.pre_node = None
        self.next_node = None
        self.is_used = 0

    def __lt__(self, other):
        return (self.is_used < other.is_used or
                self.is_used == other.is_used and self.size > other.size)

    def __eq__(self, other):
        return self.start == other.start

    def __str__(self):
        return '(%s, %s)' % (self.start, self.size)

    def split(self, size):
        if size == self.size:
            return None
        new_node = mem_node(self.start+size, self.size-size)
        new_node.pre_node = self
        new_node.next_node = self.next_node
        self.next_node = new_node
        if new_node.next_node:
            new_node.next_node.pre_node = new_node
        self.size = size
        return new_node

    def del_node(self):
        if self.pre_node: self.pre_node.next_node = self.next_node
        if self.next_node: self.next_node.pre_node = self.pre_node

class pmm_manager:
    def __init__(self, root):
        self.nodes = [root]
        self.free_mem = root.size

    def alloc_node(self, size):
        print("alloc mem size : %s/%s" % (size, self.free_mem))
        node = self.nodes[0]
        if node.is_used or node.size < size:
            print("Can't alloc new mem " + str(node))
            return None
        new_node = node.split(size)
        if new_node:
            self.nodes.append(new_node)
        node.is_used = 1
        self.nodes.sort()
        self.free_mem -= size
        return node

    def free_node(self, node):
        print("free mem size : %s/%s" % (node, self.free_mem))
        node.is_used = 0
        self.free_mem += node.size
        if node.pre_node and node.pre_node.is_used == 0:
            node.pre_node.size += node.size
            node = node.pre_node
            self.nodes.remove(node.next_node)
            node.next_node.del_node()
        if node.next_node and node.next_node.is_used == 0:
            node.size += node.next_node.size
            self.nodes.remove(node.next_node)
            node.next_node.del_node()
        self.nodes.sort()
