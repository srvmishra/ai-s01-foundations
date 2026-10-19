# Ch 1 (rest): conditioning, Bayes' rule, independence, counting

- **Course:** Introduction to Probability, 2nd ed. (Bertsekas, Tsitsiklis) and Lectures 3 and 4 of MIT 6.041 SC: Probabilistic Systems Analysis and Applied Probability.
- **Source:** https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/
- **Date studied:** 14/10/2026

## Key ideas (in my own words)

1. If two events are governed by non interacting and distinct physical processes then they are usually independent.

2. Two disjoint events are never independent.

3. Conditional independence does not imply independece and vice versa because the sample space changes depending on the conditioning event. 

4. The outcomes of a Bernoulli trial can be viewed as successive coin tosses and can be represented in a tree.

5. Counting formulas/identities can tell us about the experiment stages and vice versa.

6. Conditional independence given an event $C$ is defined as independence under the probability law $P(\cdot | C)$.

7. Pairwise independence does not imply independence (not vice versa like conditional independence and independence).

## Definitions and results

1. **Independence of events** - Occurrence of one event does not provide any information about the occurrence of another
    - $$P(A \cap B) = P(A)P(B)$$
    - Sample space is constrained to the conditioning event.
    - Defined even when $P(A)$ or $P(B)$ is $0$.
    - Symmetric in nature

2. **Conditional Independence** - Occurence of $B$ does not provide any additional information about the occurrence of $A$ given that $C$ has occurred.
    - $$P(A \cap B | C) = P(A | C)P(B | C)$$
    - $$P(A \cap B | C) = P(B | C)P(A | B \cap C)$$
    - $$P(A | B \cap C) = P(A | C)$$

3. Independence and Conditional Independence carry over to the non occurrence of events as well. 
    - $A$ and $B$ are independent then $A$ and $B^c$ are independent
    - $A$ and $B$ are conditionally independent given $C$ then $A$ and $B^c$ are conditionally independent given $C$

4. Independence of a collection of events $A_1, A_2, ..., A_n$
    - $$P(\cap_{i\in S}A_i) = \prod_{i\in S}P(A_i) \ \forall S \ \subset \{1, 2, ..., n\}$$
    - all of the above conditions must hold simultaneously and if one holds it does not imply another also holds.
    - holds for non occurrence of any number of these events as well.

5. - In a system with multiple components, it is typically assumed that each component is independent of the other.
    - Probability that a **series system** will succeed - all components must work
    $$P(series) = p_1p_2...p_n$$
    - Probability that a **parallel system** will succeed - at least one of the components must work (all components should not fail simultaneously)
    $$P(parallel) = 1 - (1-p_1)(1-p_2)...(1-p_n)$$

6. **Bernoulli trials** - A series of independent trials/repetitions of an experiment with only two possible outcomes at each stage/repetition.

7. **Counting Principle** - 
    - An experiment is carried out in stages
    - For any sequence of possible results in the first $i-1$ stages, there are $n_i$ possible results at the $i$ th stage. The total number of possible results is $n_1n_2...n_r$.
    - The counting principle remains valid even if each first stage result leads to a different set of potential second stage results, etc. The only requirement is that the number of second stage results is constant, regardless of the first stage result

8. **Permutations** - Number of ways of choosing $k$ out of $n$ objects and arranging them into a sequence $(k \leq n)$ is

    $$^nP_k = \frac{n!}{(n-k)!}$$

9. **Combinations** - Number of ways of choosing $k$ out of $n$ objects

    $$^nC_k = {n \choose k} = \frac{n!}{k!(n-k)!}$$

    - number of $k$ element subsets from a $n$ element set
    - ordering within each subset is immaterial
    - $\sum_{k=1}^n {n \choose k} = 2^n$: total number of subsets (each element can either be included or excluded)
    - Also called **Binomial Coefficient**
    - derive using: $k$ permutations = first choose $k$ elements, and then arrange them.

10. **Partitions** - Number of ways of choosing subsets of sizes $n_1, n_2, ..., n_r$ from a set of $n$ elements such that $n_1 + n_2 + ... + n_r = n$ is 
    - $${n \choose n_1, n_2, ..., n_r} = \frac{n!}{n_1!n_2!...n_r!}$$
    - it is important to have $n_1 + n_2 + ... + n_r = n$
    - number of ways of choosing disjoint subsets from a set
    - think of this as a $r$ stage experiment in which each stage is creating a subset
    - Combinations is a special case when we are only doing two partitions. 
    - Also called **Multinomial Coefficient**


## Derivations I worked through

> $$\sum k {n - 1 \choose k} = n2^{n-1}$$

- number of ways of choosing one special person from a group of $n$ people followed by some others (potentially 0).
- see this as a two stage experiment
- LHS (For a fixed size of $k$ people): stage 1: we choose $k$ people out of $n$ and stage 2: we choose $1$ out of $k$ people.
- RHS: stage 1: there are $n$ ways to choose this special person and stage 2: the remaining people are to be chosen from the remaining $n-1$ people. since there are no restrictions on the number, it will be the total number of subsets
- this can be proved by binomial expansion, differentiation, and substitution 

## What confused me (questions for the weekly oral)

1. In the book, example 1.31, i think the identity is written wrong. It should be $\sum k {n - 1 \choose k} = n2^{n-1}$.

2. Doubt in tutorial problems
    - Tutorial 2 - 
        - Problem 1 - I did it following a sequential probability approach. Can we arrive at the same results by counting approach. I need the counting arguments.
    - Tutorial 1 - 
        - Problem 1 - including all cases. I only included $B = \Omega$. $A = \Phi$ is also a solution.
        - Problem 3 - part b - part i - definition and favourable outcomes of a surviving challenger.

3. Doubt in problem set problems
    - Problem 4 - how to describe the events. and in parts c and d. sometimes i am not sure whether normal or conditional probabilities are asked
        - part c - why does probability that dog is in forest $A$ matter here.
        - part d - why not consider that dog is alive on day 1 also. why to consider probability that dog is in forest $A$ when we are given that it is so. at least that is my understanding.
    - Other doubts which I clarified looking at the solutions: 
        - Problem 3 - I assumed that objects can be drawn with replacement/there are infinite objects with prior defined probabilities of being old and new. It is a sequential problem of selecting two objects.
        - Problem G1 - number of outcomes with the same probability also matters while calculating probability

4. I understood that defining the outcomes, the events, and the probability that is asked in terms of the events is very important to solving problems. I would like to redo the problems 3 and 4 from the problem set in the office hours to get better understanding.

5. I need to see the equivalence between the sequential and the counting approaches for probability calculations. I also want to be able to make counting arguments on my own and arrive at counting identities in different ways (using different arguments). I want to practice deriving these identities both algebraically and by using counting arguments. 


## Formula cheat sheet (only if you tested out of this item)


## Links to code or exercises

1. The lecture notes are also written in this document. Hence the `mit-6-041sc-probabilistic-systems-analysis-lectures-3-4-of-25-video-lectures-wit.md` document is empty.