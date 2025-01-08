# arr = [3, 2, 4, 7, 10, 6, 5]
#
# def print_odd(arr):
#     for i in range(len(arr)):
#         if arr[i] % 2 != 0:
#             print(arr[i])
# print_odd(arr)

# class Node:
#     def __init__(self, value):
#         self.value = value
#         self.next = None
#
# class LinkedList:
#     def __init__(self):
#         self.head = None
#         self.tail = None
#
#     def append(self, value):
#         new_node = Node(value)
#         if not self.head:
#             self.head = new_node
#             self.tail = new_node
#         else:
#             self.tail.next = new_node
#             self.tail = new_node
#     def display(self):
#         current = self.head
#         while current:
#             print(current.value, end=" -> ")
#             current = current.next
#         print(None)
#
#
#
# new_list = LinkedList()
# for i in range(0,100, 34):
#     new_list.append(i)
#
# new_list.display()


# def efficient_gcd(a, b):
#     while b != 0:
#         a, b = b, a % b  # Update a to b, and b to a % b
#     return a  # When b becomes 0, a is the GCD
#
# print(efficient_gcd(357,234))


#enter a list as an argument
#get the max number on the list
#append that number to another list
#remove the number from current list
#loop

# arr = [2,345,5,7,78,32,43]
#
# def desc_order(arr):
#     desc = []
#     while arr:
#         n_max = max(arr)
#         desc.append(n_max)
#         arr.remove(n_max)
#     return desc
#
#
# print(desc_order(arr))
#
#
#        5
#     3      8
#   2   4  7
#

# class TreeNode:
#     def __init__(self, val, right=None, left=None):
#         self.val = val
#         self.right = right
#         self.left = left
#
#     def __str__(self):
#         return str(self.val)
#
# A = TreeNode(5)
# B = TreeNode(3)
# C = TreeNode(8)
# D = TreeNode(2)
# E = TreeNode(4)
# F = TreeNode(7)
#
# A.right = C
# A.left = B
# B.right = E
# B.left = D
# C.left = F
#
#
#  def pre_order(node):
#      if not node:
#         return
#
#     print(node)
#     pre_order(node.left)
#     pre_order(node.right)
#
# pre_order(A)

# def in_order(node):
#     if not node:
#         return
#
#     in_order(node.left)
#     print(node)
#     in_order(node.right)
#
# in_order(A)

# def post_order(node):
#     if not node:
#         return
#
#     post_order(node.left)
#     post_order(node.right)
#     print(node)
#
# post_order(A)

from collections import deque

# def level_traversal(node):
#     q = deque()
#     q.append(node)
#
#     while q:
#         current_node = q.popleft()
#         print(current_node)
#         if current_node.left : q.append(current_node.left)
#         if current_node.right : q.append(current_node.right)
#
# level_traversal(A)


# def level_traversal(node):
#     q = []
#     q.append(node)
#
#     for i in q:
#         current_node = q[i.val]
#         print(current_node)
#         if current_node.left : q.append(current_node.left)
#         if current_node.right : q.append(current_node.right)
#
# level_traversal(A)
#
# def twoSum(nums, target):
#     """
#     :type nums: List[int]
#     :type target: int
#     :rtype: List[int]
#     """
#     for i in nums:
#         if i < len(nums) - 1:
#             sum = nums[i] + nums[i + 1]
#             if sum == target:
#                 return [i, i + 1]
#
#
# class Node:
#     def __init__(self, val):
#         self.val = val
#         self.left = None
#         self.right = None
#
#     def __str__(self):
#         return str(self.val)
#
# class BinaryTree:
#     def __init__(self):
#         self.root = None
#
#     def insert(self, val):
#         if not self.root:
#             self.root = Node(val)
#         else:
#             self._insert(self.root, val)
#
#     def _insert(self, current, val):
#         if val < current.val:
#             if current.left:
#                 self._insert(current.left, val)
#             else:
#                 current.left = Node(val)
#         else:
#             if current.right:
#                 self._insert(current.right, val)
#             else:
#                 current.right = Node(val)
#
#     def __str__(self):
#         return self._in_order(self.root, []).__str__()
#
#     def in_order(self):
#         result = []
#         self._in_order(self.root, result)
#         return result
#
#     def _in_order(self, node, result):
#         if result is None:
#             result = []
#         if node:
#             self._in_order(node.left, result)
#             result.append(node.val)
#             self._in_order(node.right, result)
#
#
#     def pre_order(self):
#         result = []
#         self._pre_order(self.root, result)
#         return result
#
#     def _pre_order(self, node, result):
#         if node:
#             result.append(node.val)
#             self._pre_order(node.left, result)
#             self._pre_order(node.right, result)
#
#     def post_order(self):
#         result = []
#         self._post_order(self.root, result)
#         return result
#
#     def _post_order(self, node, result):
#         if node:
#             self._post_order(node.left, result)
#             self._post_order(node.right, result)
#             result.append(node.val)
#
#
# tree = BinaryTree()
#
# tree.insert(6)
# tree.insert(2)
# tree.insert(4)
# tree.insert(7)
# tree.insert(1)
# tree.insert(3)
#
# for i in range(100):
#     tree.insert(i)
#
# print(tree.in_order())
#
# from collections import Counter
# print(Counter(tree.in_order()))

# class Node:
#     def __init__(self, val, right=None, left=None):
#         self.val = val
#         self.right = right
#         self.left = left
#
# a = Node("a")
# b = Node("b")
# c = Node("c")
# d = Node("d")
# e = Node("e")
# f = Node("f")
#
# a.right = c
# a.left = b
# b.left = d
# b.right = e
# c.right = f
#

# DFS iteratively (using a stack)

# def dfs(node):
#     if node is None:
#         return []
#
#     stack = [ node ]
#     result = []
#
#     while stack:
#         current = stack.pop()
#         result.append(current.val)
#
#         if current.right:
#             stack.append(current.right)
#         if current.left:
#             stack.append(current.left)
#
#     return result
#
# print(dfs(a))

# DFS recursively

# def dfs_recursive(node):
#     if node is None:
#         return []
#
#     left = dfs_recursive(node.left) if node.left else []
#     right = dfs_recursive(node.right) if node.right else []
#
#     return [node.val, *left, *right]
#
#
# nums = [2,3,4,5,6,7,3]
#
# print(enumerate(nums))


i =[1,2,3]
#     print(True)
# else:
#     print(False)

# make hash map (seen)
# iterate over the array
# calculate the complement
# check if complement is in seen
# if it is return indexes
# if not add it to hashmap
seen = {}



for i in range(3):
 print(i)






