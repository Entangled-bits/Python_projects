# CODE by Aman Agarwal

# This code works if and only if the tree is balanced.

# The expectimax algorithm is similar to the minimax algorithm wherein we try to maximize the best move for the current player.
# Instead of calculating minimum in the intermediate steps, we calculate the average of the children nodes of the current node.

# The no of leaf nodes can be used to determine the height and no of branches of the tree since the tree is a balanced tree.

# We implement recursion and calculate the particular value at every level and output the maximum value that can be obtained at the end. 
import math

# The group function assigns sublists for a given list according to the no of branches.
def group(list, branches):
	new_list=[]
	initial=0
	final=initial+2
	for j in range(len(list)//2):
		new_list.append([])
		for i in range(initial, final):
			new_list[j].append(list[i])
		initial=final
		final=initial+2
	return new_list

# The chance function is used to calculate the average of it's child nodes and it returns a list consisting of the nodes divided in sublists using group function.
def chance(nodes, branches):
	list=[]
	for i in nodes:
		sum=0
		for j in i:
			sum+=j
			list.append(sum//len(i))
	return group(list,branches)
	
# The max2 function similarly calulates the max value of each sublist and appends it in an empty list. It returns the list adjusted using group function.
def max2(nodes, branches):
	list=[]
	for i in nodes:
			list.append(max(i))
	return group(list, branches)

# This is the recursive function that calculates the best possible move for the current player. This function require that the minimum level of the tree must be 0 of multiple of 2 to implement this algorithm.
def expectiMax_1(nodes, level, branches):
	if level == 0:
		return max(nodes)
	if level%2==0:
		return expectiMax_1(chance(nodes, branches), level-1, branches)
	elif level==1:
		return expectiMax_1(max(nodes), level-1, branches)
	else:
		return expectiMax_1(max2(nodes, branches),level-1, branches)

# This function calculates the depth of tree based on the no of leaf nodes and length of the sublist which determines the no of branches in the tree.
# The formula is : no of leaf nodes = branches**depth.
# Hence, depth = log(no of leaf nodes) to the base of branches
def treeDepth(list):
	number_of_nodes = len(list)*len(list[0])
	return math.log(number_of_nodes,3)

# Let us see the implementation of the algorithm.
# We have 16 leaf nodes that means we have 4 levels and 2 branches as the length of sublist is 2.
nodes=[[3,12],[2,4],[15,6],[2,3],[1,1],[5,4],[9,12],[23,12],[90,12],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8]]

# We store the depth of the tree in this variable
depth = int(treeDepth(nodes))

# We store the no of branches of the tree in this variable.
branches=len(nodes[0])

#We finally print the output.
print("The best possible move for the player is:", expectiMax_1(nodes, depth, branches))

#Note: This code will work if and only if the tree is balanced as it ensures that the no of branches in each node is constant the the depth of tree can be calculated using the above formula.

# THE END
