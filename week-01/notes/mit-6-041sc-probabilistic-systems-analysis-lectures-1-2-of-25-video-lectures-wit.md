# Lectures 1–2 of 25 (video lectures, with the matching book sections)

- **Course:** MIT 6.041SC Probabilistic Systems Analysis (Tsitsiklis)
- **Source:** https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/
- **Date studied:** 09/10/2026

## Key ideas (in my own words)

1. Proabbility views - 
    - beliefs about some events in uncertain situations
    - frequency of occurrence 

2. Steps to calculate probability:
    - Define sample space
    - Describe the probability law
    - Define the event of interest
    - Calculate Probability

3. Example of a probability law - Discrete Uniform law:
    - All outcomes are equally likely
    - Computing probabilities = Counting

4. Discrete vs Continuous: 
    - Discrete uniform law -> Integration (or Area) in continuous case
    - In the discrete case, individual outcomes can be assigned non-zero probabilities.
    - In the continuous case, individual points have zero probabilities but areas have non-zero probabilities. So events in the continuous case are areas/regions in the sample space.

5. Unlikely cases:  
    - Individual outcomes/points with 0 probability can occur. 
    - In the same way events with probability 1 cannot happen. 

6. Conditional Probability:
    - reasoning with partial/additional information.
    - constrains/changes the sample space.
    - follows all the rules of normal probability.
    - can be seen as branches/stages of an experiment.
    - sometimes conditional interpretations can be counter intuitive because of class imbalance and false positives.

7. Total Probability:
    - also known as marginalization
    - requires a partition of the sample space

## Definitions and results

- **Sample space ($\Omega$)**: space of all possible outcomes in an experiment
    - outcomes are **mutually exclusive** and **collectively exhaustive**
    - sample space can be as detailed or brief depending on the requirement
    - outcomes can be represented by trees if the experiment is performed in stages, eg., multiple tosses of a coin
    - sample space could be finite, infinite, continuous, discrete

- **Probability Axioms**:
    - $P(A) \geq 0 \ \forall A$
    - $P(\Omega) = 1$
    - for disjoint events A and B, $P(A \cup B) = P(A) + P(B)$

- For $n$ pairwise disjoint events $A_1, A_2, ..., A_n$, we have $$P(A_1 \cup A_2 \cup ... \cup A_n) = P(A_1) + P(A_2) + ... + P(A_n)$$ These events can be ordered or unoredered. 

- **Countable Additivity Axiom**: The above extends for a *countable sequence* of *disjoint* events. 

- **Conditional Probability**: Probability of an event $A$ given information about another event $B$.
    - Denoted as $P(A|B)$
    - Defined as $$P(A|B) = \frac{P(A \cap B)}{P(B)}$$ Only when $P(B) \neq 0$.

- **Conditional Probability follows all rules of normal probability.**
    - $P(A|B) \geq 0$
    - $P(B|B) = 1$
    - $P(\Omega|B) = 1$
    - $A \cap C =\empty \Rightarrow P(A \cup C | B) = P(A|B) + P(C|B)$

- **Multiplication Rule**: 

$$P(A \cap B) = P(A)P(B|A) = P(B)P(A|B)$$
$$P(A \cap B \cap C) = P(C)P(B|C)P(A|B,C)$$
$$P(A_1\cap A_2\cap ... \cap A_n) = P(A_1)\prod_{i=1}^nP(A_i|A_1, A_2, ..., A_{i-1})$$

- **Total Probability**:
    - $A_1, A_2, ..., A_n$ are **partitions** of the sample space.
    - So, all the $A_i$ s are **pairwise disjoint** and **collectively exhaustive**.
    - So, $\Omega = \cup_{i=1}^nA_i$ and $A_i \cap A_j = \empty \ \forall i, j$. Therefore, $\Sigma_{i=1}^nP(A_i) = 1$. $P(A_i)$ act as weights.
    - Any event $B$ can be expressed as $B = \cup_{i=1}^n(B \cap A_i)$.
    - $$P(B) = \Sigma_{i=1}^nP(B\cap A_i) = \Sigma_{i=1}^nP(A_i)P(B|A_i)$$
    - $A_i$ s are a countable set/sequence of events. 

- **Bayes Rule**:
    - Initial beliefs: $P(A_i)$ are known
    - $P(B|A_i)$ are known (model)
    - Revised beliefs (inference): $$P(A_i|B) = \frac{P(A_i)P(B|A_i)}{\Sigma_{j=1}^nP(A_j)P(B|A_j)}$$

## Derivations I worked through

> $P(A) \leq 1$

$A \cup A^c = \Omega \Rightarrow$ These events are collectively exhaustive

$A \cap A^c = \empty \Rightarrow$ These events are mutually exclusive (disjoint)

$\Rightarrow P(\Omega) = P(A \cup A^c) = P(A) + P(A^c) = 1$

Since $P(A^c) \geq 0 \Rightarrow P(A) \leq 1$

> $P(\empty) = 0$

$P(\Omega) = 1$ and $\Omega^c = \empty$

From above, $P(\empty) = 1 - P(\Omega) = 0$

> If $A \subset B$ then $P(A) \leq P(B)$

$B = B \cap \Omega = B \cap (A \cup A^c) = (B\cap A) \cup (B \cap A^c)$

Since $A \subset B \Rightarrow B \cap A = A$

$\Rightarrow B = A + B \cap A^c$ and $A \cap (B \cap A^c) = \empty$

$\Rightarrow P(B) = P(A) + P(B \cap A^c)$

Since $P(B \cap A^c) \geq 0 \Rightarrow P(B) \leq P(A)$

> $P(A \cup B) = P(A) + P(B) - P(A \cap B)$

$A = A \cap \Omega = A \cap (B \cup B^c) = (A \cap B) \cup (A \cap B^c)$ and $(A \cap B) \cap (A \cap B^c) = \empty$

Similarly, $B = (B \cap A) \cup (B \cap A^c)$ and $(B\cap A) \cap (B \cap A^c) = \empty$

And, $A \cup B = (A \cap B) \cup (A \cap B^c) \cup (B \cap A^c)$

$\Rightarrow P(A \cup B) = P(A \cap B) + P(A \cap B^c) + P(B \cap A^c) = P(A \cap B) + P(A \cap B^c) + P(B \cap A^c) + P(A \cap B) - P(A \cap B) = P(A) + P(B) - P(A \cap B)$

$\Rightarrow P(A \cup B) = P(A) + P(B) - P(A \cap B)$

> $P(A|B) \geq 0$

$P(A\cap B) \geq 0$ and $P(B) > 0 \Rightarrow P(A|B) \geq 0$. It is 0 only when $A \cap B = \empty$

> $P(B|B) = 1$

$B\cap B = B \Rightarrow P(B|B) = 1$.

> $P(\Omega|B) = 1$

$\Omega\cap B = B \Rightarrow P(\Omega|B) = 1$.

> $A \cap C =\empty \Rightarrow P(A \cup C | B) = P(A|B) + P(C|B)$

$(A \cup C) \cap B = (A \cap B) \cup (C \cap B)$

$A \cap C = \empty \Rightarrow (A \cap B) \cap (C \cap B) = \empty$

$\Rightarrow P((A \cup C) \cap B) = P(A \cap B) + P(C \cap B)$

$\Rightarrow P(A \cup C | B) = P(A|B) + P(C|B)$

## What confused me (questions for the weekly oral)

- All recitation problems (Recitations 1 and 2) are covered in the textbook problems.

## Links to code or exercises

