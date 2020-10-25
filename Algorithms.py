class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Function to add node
    def at_end(self, data_in):
        new_node = Node(data_in)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while(last.next):
            last = last.next
        last.next = new_node

    # Function to remove node
    def remove_node(self, remove_key):

        head_val = self.head

        if head_val is not None:
            if head_val.data == remove_key:
                self.head = head_val.next
                head_val = None
                return

        while head_val is not None:
            if head_val.data == remove_key:
                break
            prev = head_val
            head_val = head_val.next

        if head_val == None:
            return

        prev.next = head_val.next

        head_val = None

    def llist_print(self):
        print_val = self.head
        while print_val:
            print(print_val.data),
            print_val = print_val.next

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
