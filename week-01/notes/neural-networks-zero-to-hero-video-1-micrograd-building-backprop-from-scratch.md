# Video 1: micrograd, building backprop from scratch

- **Course:** Neural Networks: Zero to Hero (Karpathy)
- **Source:** https://github.com/karpathy/nn-zero-to-hero
- **Date studied:** 10/10/2026

## Key ideas (in my own words)

1. Backpropagation is a machinery that can be used to differentiate any mathematical operation. It is used to train neural networks. It recursively applies chain rule through the computation graph.

2. Micrograd is a scalar valued auto grad engine. The basic operation is differentiating scalars and it is sufficient for backpropagation. Tensors are just arrays of scalars and working with tensors will make large backpropagation on neural networks efficient. 

3. Implementing Forward Pass
    - every node should have its **value/data** field
    - implement **addition** and **multiplication** operations. *input: two nodes, output: a new node*
    - for every node, keep track of **child nodes**
    - keep track of **operations** that produced each node
    - additionally, let every node have a **name/label** field

4. Implementing Backward Pass
    - have a **grad** field for each node to track gradients
    - understand how multiplication and addition distribute gradients
    - there are two types of nodes - 
        - **leaf node** (independent variables - data, weights and biases). these do not require a backward function because they have no children
        - **non-leaf nodes** (activations, intermediate outputs). these require a backward function to allow chain rule to work through them
        - update the backward function of each node involved in an operation based on the behaviour of the operation
    - initialization of gradient values - 
        - at the output node 1.0
        - at all nodes 0.0
    - compute gradients by calling the backward function for each node in the right order (except the leaf nodes).
    - to call the backward function for each node in the right order, use **reversed topological sort**.
    - in case a node is has multiple children, then it should **accumulate** gradients from all its children. so this accumulation feature should be used in the backward functions for each node.
    - for implementing backward through activation functions, you can make it as a composition of several simpler operations and functions or keep it as it is as long as you know the local gradient.
    - if some operations are defined in terms of other operations, then do not need to specify the backward operation in these functions as long as the backward operation in the other functions are specified. For example, subtraction is implemented in terms of addition, division is implemented in terms of multiplication and power. So if the backward operations are specified in addition, multiplication, and power, then division and subtraction do not need their own backward operations.
    - In the same way, if we have specified the backward functions in addition, multiplication, and exponentiation, we do not need to specify a backward function in tanh
    - the above points hold as long as we are implementing these functions/operations using at least one Node object as input and node objects as outputs.
    - clear gradients between two consecutive iterations of backward pass because gradients are accumulated.

5. Implementing a numerical differentiation would require as many forward passes as there are independent variables (weights and biases) and would be expensive.

6. Python Implementation Details - 
    - `a + b = a.__add__(b)`
    - `a - b = a.__add__(b.__neg__())`
    - `a/b = a.__truediv__(b)`
    - `a*b = a.__mul__(b)`
    - `2*a = a.__rmul__(2)`: 2 is not a Node object.
    - `a*2` - modify the `__mul__` function for it to handle other data types
    - `a**b = a.__pow__(b)`

7. Loss functions -
    - Mean Squared Error
    - Cross Entropy

8. Pytorch allows us to define custom functions with their forward and backward signatures so that these can be used with the autograd engine. 

9. In my implementation, I have named the Value Class as Node.

## Definitions and results


## Derivations I worked through

## What confused me (questions for the weekly oral)

- Why for every node the children attribute was defined as a set?

- What if in the power operation, the second input is also a node object?

- Why some attributes have a preceeding `_` character? What about the functions that have this? What about the functions with two underscores before and after their name?

- Why is grad attribute of every node object a float? Why can't it be another node object? In pytorch the grad of a tensor is a tensor.

- While writing functions/methods inside a class, do we first have to write those that start and end with double underscores? or we can write the functions in any order?

- I want to understand the topological sort. Can we implement it with a python list instead of using a recursive approach as shown in the video? visited nodes is a set and we only explore the nodes that are not yet visited. Also, this feels like a depth first traversal rather than a breadth first one. Does it make a difference what traversal we use to implement backprop?

- I made an error in topological sort. My gradients for all parameters except the one on the top of the graph were zeros. I ran training a couple of times and losses never converged, then I used `draw_dot` to find if all gradients were actually zeros and they were. I found that I was not building the sort for every child node, rather the same node. I corrected it and my training went fine. 

- Why are we also writing `other.grad` field in backward function? Shouldn't `self.grad` alone be sufficient?

- What does `@staticmethod` do in python? 

## Links to code or exercises
