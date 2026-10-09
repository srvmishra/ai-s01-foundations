# Ch 1 Sample space and probability, sections 1.1–1.3; end-of-chapter problems

- **Course:** Introduction to Probability, 2nd ed. (Bertsekas, Tsitsiklis)
- **Source:** https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/
- **Date studied:** 09/10/2026

## Key ideas (in my own words)

1. Probability views - 
    - frequency of occurrence
    - beliefs about events in uncertain situations

2. Probability law assigns every event (set of outcomes) a non-negative number (probability).

3. Outcomes must be mutually exclusive (every trial of the experiment produces a unique outcome). Sample space must contain all the outcomes (collectively exhaustive). Any trial cannot produce an outcome outside the sample space. An event is a subset of the sample space.

4. If a probabilistic experiment is carried out in sequential stages, then the sample space can be depicted as a tree. Outcomes are at the leaves of the tree. Multiplication rule, conditional probabilities are also linked to this tree depiction of sample space.

5. Equally likely outcomes:
    - counting in the discrete case
    - length/area in the continuous case

6. In conditional probability, we are dealing with partial/new information. The conditioning event becomes our new sample space. Conditional probability laws can therefore be viewed as probability laws on the conditioning event.

## Definitions and results

1. Set:
    - collection of elements
    - **countable/uncountable**: elements *can/cannot* be **enumerated**.
    - can be **infinite/finite**.
    - **Universal Set** ($\Omega$): Set of all objects of interest in a particular context

2. $A$ is a **subset** of $B$:
    - Every element of $A$ is also an element of $B$
    - Denoted as $A \subset B$
    - $A = B$ if and only if $A \subset B$ and $B \subset A$

3. Set Operations:
    - **Union**: $A \cup B = \{x | x \in A \ \text{or} \ x \in B\}$
    - **Intersection**: $A \cap B = \{x | x \in A \ \text{and} \ x \in B\}$
    - **Complement**: $A^c = \{x | x \ \text{in} \ \Omega \ \text{and} \ x\notin A\}$

4. Disjoint Sets and Partition:
    - $A$ and $B$ are **disjoint**: $A \cap B = \empty$.
    - $A_1, A_2, ..., A_n$ are **pairwise disjoint** if $A_i\cap A_j = \empty \ \forall \ i,j$.
    - If $A_1, A_2, ..., A_n$ are **pairwise disjoint** and $\cup_{i=1}^nA_i = B$,  then $A_i$ s are a **partition** of $B$.

5. Properties of Sets:
    - $A \cup A^c = \Omega$
    - $A \cap A^c = \empty$
    - $(A^c)^c = A$
    - $A \cup \Omega = \Omega$
    - $A \cap \Omega = A$
    - Union and Intersection operations are:
        - commutative
        - associative
        - distribute over each other

## Derivations I worked through

## What confused me (questions for the weekly oral)

1. How to specify a probability law that will satisfy all the axioms in the following cases assuming that all outcomes are equally likely - 
    - sample space is the set of real numbers 
    - or the set of natural numbers

2. I understood the two approaches to the Bertrand's paradox. But is there a way to solve the problem and come up with a clear answer. In the first approach, the slope of the chord was fixed and in the second approach, one of the end points was fixed. How to do this if both ends are freely moving on the circle?

3. I want to understand the Monty Hall Problem. After one door is opened and we are shown that it is not having the prize, doesn't the probability that the prize could be behind one of the remaining doors become 0.5?

4. Doubts in textbook problems - 
    - better explanation of cantor's diagonalization argument (problem 4)
    - problem 8
    - problem 15

## Links to code or exercises
