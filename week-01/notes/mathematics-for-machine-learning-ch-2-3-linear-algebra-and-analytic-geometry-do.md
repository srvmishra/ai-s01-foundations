# Ch 2–3: linear algebra and analytic geometry (do the exercises)

- **Course:** Mathematics for Machine Learning (Deisenroth, Faisal, Ong; free)
- **Source:** https://mml-book.github.io/
- **Date studied:** 11/10/2026

## Key ideas (in my own words)

1. A group requires one operation on a set. A vector space requires two operation - one on the set, and one outside the set.

2. For every vector space $V$, the trivial vector subspaces are $V$ and $\{0\}$.

3. The solutions of the set of homogeneous equations given by $Ax = 0$ with $A \in R^{n\times n}$ is a vector subspace of $R^n$ and it is the nullspace of $A$.

4. The intersection of arbitrarily many vector subsapces is a vector subspace.

5. A vector subspace is also a vector space.

6. A matrix is a collection of column vectors. It is also a linear mapping. 

7. In all bases changes and coordinate transforms, the underlying vector stays the same. Its representation changes because the bases change.

8. Change of bases can be understood in terms of chaining or composition of transforms.

## Definitions and results

1. **Group**: Consider a set $S$ and an operation $\otimes: S \times S \rightarrow S$. Then $G = (S, \otimes)$ is a group if:
    - **Closure**: $S$ is closed under $\otimes$ 
    $$\forall x, y \in S: \ x\otimes y \in S$$
    - **Associative**: $\otimes$ is associative on $S$
    $$\forall x, y, z \in S: \ (x \otimes y)\otimes z = x\otimes(y\otimes z)$$
    - **Neutral Element**: 
    $$\exists e \in S \ \text{such that} \ \forall x \in S: \  x\otimes e = e\otimes x = x$$
    - **Inverse Element**:
    $$\forall x \in S \ \exists y \in S \ \text{such that}: \ x\otimes y = y \otimes x = e$$

2. If $\otimes$ is also **commutative** on $S$, then $G$ is an Abelian group.

3. **General Linear Group (n)**: The set of all invertible matrices $A \in R^{n\times n}$ with the matrix multiplication operation is a group called the general linear group or $GL(n, R)$. It is not Abelian because the matrix multiplication is not commutative. 

4. **Vector Space:** Let $S$ be a set and $\otimes: S \times S \rightarrow S$ and $\odot: R \times S \rightarrow S$ be two operations. $V = (S, \otimes, \odot)$ is a vector space if:
    - $(S, \otimes)$ is an **Abelian** group.
    - $\odot$ has these properties:
        - **Associative**: $\lambda\odot(\psi\odot x) = (\lambda\odot\psi)\odot x, \ \forall \lambda, \psi \in R \ \text{and} \ x\in S$.
        - **Distributive**:
            - $\forall x, y \in S \ \text{and} \ \forall \lambda \in R: \ \lambda\odot(x+y) = \lambda\odot x + \lambda\odot y$
            - $\forall \lambda, \psi \in R \ \text{and} \ \forall x\in S: \ (\lambda + \psi)\odot x = \lambda\odot x + \psi\odot x$
        - **Neutral Element**: $\exists e \in R \ \text{such that} \ \forall x \in S: \ e\odot x = x\odot e = x$

5. **Vector Subspace**: Let $V = (S, \otimes, \odot)$ is a vector space and $T \subset S$. $U = (T, \otimes, \odot)$ is a vector subspace of $V$ if
    - $T \neq \empty$. In particular $0 \in T$.
    - $U$ is closed under $\otimes$
    $$\forall x, y \in T:  \ x\otimes y \in T$$
    - $U$ is closed under $\odot$
    $$\forall \lambda \in R, \forall x \in T:  \ \lambda\odot x\in T$$

6. Every subspace $U \subset (R^n, +, .)$ is the solution space of a homogeneous system of linear equations $Ax = 0$ for $x \in R^n$.

7. **Linear Mapping or Homomorphism**: Let $\Phi: V \rightarrow W$ be a mapping from a vector space $V$ to a vector space $W$. It is a linear mapping if:

    $$\forall \lambda, \psi \in R, \ \text{and} \ x, y \in V: \Phi(\lambda \odot x + \psi \odot y) = \lambda\odot\Phi(x) + \psi\odot\Phi(y)$$

8. **Types of Homomorphisms**:
    - **Isomorphism**: $\Phi: V\rightarrow W$ is bijective
    - **Endomorphism**: $\Phi: V\rightarrow V$ 
    - **Automorphism**: $\Phi: V\rightarrow V$ is bijective
    - **Identity Automorphism**: $\Phi: V\rightarrow V$ such that $x \mapsto x$ 

9. If $\Phi: V \rightarrow W$ is an isomorphism, then $\Phi^{-1}: W \rightarrow V$ is also an isomorphism. A linear transformation between two bases of the same vector space is an identity automorphism.

10. Composition of two homomorphisms is also a homomorphism. Addition and scaling of homomorphisms also result in homomorphism.

11. **Theorem**: Finite dimensional vector spaces $V$ and $W$ are isomorphic iff $dim(V) = dim(W)$.

12. Let $V$ be a $n-$ dimensional vector space with ordered basis $B = (b_1, b_2, ..., b_n)$. Then the mapping $\Phi: R^n \rightarrow V$ such that $\Phi(e_i) = b_i, \ i = 1, 2, ..., n$ is an isomorphism. $(e_1, e_2, ..., e_n)$ is the standard basis of $R^n$.

13. **Finding the transformation matrix of a homomorphism**:
    - Let $V$ and $W$ be vector spaces with ordered bases $B = (b_1, ..., b_n)$ and $C = (c_1, ..., c_m)$ respectively.
    - Let $\Phi: V \rightarrow W$ be a homomorphism.
    - $\Phi(b_j) = \sum_{i=1}^m\alpha_{ij}c_i$.
    - $\Phi(b_j)$ lives in $W$ and its coordinates with respect to basis $C$ is the vector $\alpha_j$.
    - The matrix $A_{\Phi}$ whose columns are $\alpha_j$ is the transformation matrix for $\Phi$. $A_{\Phi}(i, j) = \alpha_{ij}$.
    - $A_{\Phi}$ depends on bases $B$ and $C$. It changes if the bases change.
    - It transforms coordinates of vectors in $V$ (with respect to $B$) to coordinates of vectors in $W$ (with respect to $C$).

14. **Transformation Matrix Under Bases Change**:
    - Let $V$ be a vector space with ordered bases $B = (b_1, ..., b_n)$ and $\tilde{B} = (\tilde{b}_1, ..., \tilde{b}_n)$.
    - Let $\Psi: V\rightarrow V$ be an automorphism with matrix representation $A_{\Psi}$ that transforms coordinates of vectors from the basis $\tilde{B}$ to $B$.
    - Let $W$ be a vector space with ordered bases $C = (c_1, ..., c_m)$ and $\tilde{C} = (\tilde{c}_1, ..., \tilde{c}_m)$.
    - Let $\Omega: W \rightarrow W$ be an automorphism with matrix representation $A_{\Omega}$ that transforms coordinates of vectors from the basis $\tilde{C}$ to $C$.
    - Let $\Phi: V\rightarrow W$ be a homomorphism with matrix representation $A_{\Phi}$ with respect to bases $B$ and C. Let $\tilde{A}_{\Phi}$ be the matrix representation with respect to bases $\tilde{B}$ and $\tilde{C}$.
    - Consider a vector $v \in V$ with coordinates $\tilde{x}$ with respect to $\tilde{B}$ and $x$ with respect to $B$. Similarly, let $w \in W$ have coordinates $\tilde{y}$ with respect to $\tilde{C}$ and $y$ with respect to $C$. Also let $y = A_{\Phi}x$
    - We have $x = A_{\Psi}\tilde{x}$ and $y = A_{\Omega}\tilde{y}$. This gives $A_{\Omega}\tilde{y} = A_{\Phi}A_{\psi}\tilde{x}$ or $\tilde{y} = \tilde{A}^{-1}_{\Omega}A_{\Phi}A_{\Psi}\tilde{x} = \tilde{A}_{\Phi}x$. 
    - This gives $\tilde{A}_{\Phi} = \tilde{A}^{-1}_{\Omega}A_{\Phi}A_{\Psi}$

15. **Equivalent Matrices**: $A \in R^{m\times n}$ and $B \in R^{m\times n}$ are equivalent if there exist regular matrices $S\in R^{m\times m}$ and $T \in R^{n\times n}$ such that $A = S^{-1}BT$

16. **Similar Matrices**: Square matrices $A, B \in R^{n\times n}$ are similar if there exist a regular matrice $S\in R^{n\times n}$ such that $A = S^{-1}BS$

15. **Image and Kernel**: Let $\Phi: V \rightarrow W$ be a linear transformation.
    - **kernel or null space**: the set of vectors in $V$ that map to $0$. 
    $$ker(\Phi) = \{v \in V | \Phi(v) = 0 \in W\}$$
    - **image or range**: the set of all vectors $w$ in $W$ that can be reached via $\Phi$ from any vector in $V$
    $$Im(\Phi) = \{w\in W| \exists v\in V: \Phi(v)=w \}$$
    - $ker(\Phi)\subset V$: kernel is a subspace of the domain of $\Phi$
    - $ker(\Phi) \neq \empty$ because $\Phi(0_V)=0_W$. Here $0_V$ is the zero vector in $V$ and $0_W$ is the zero vector in $W$.
    - $Im(\Phi) \subset W$: image is a subspace of codomain of $\Phi$.
    - $\Phi$ is injective iff $ker(\Phi)=\{0\}$
    - Let the transformation $\Phi: R^n \rightarrow R^m$ be given by $x \mapsto Ax$ where $A \in R^{m\times n}$.
        - $Im(\Phi) = Im(A) \subset R^m$ is the columnspace of $A$.
        - $dim(Im(A)) = rank(A) \leq m$.
        - $ker(\Phi) = ker(A) \subset R^n$ is the nullspace of $A$.
    - **Rank Nullity Theorem**: for any linear mapping $\Phi: V \rightarrow W$

        $$dim(Im(\Phi)) + dim(ker(\Phi)) = dim(V)$$

        - If $dim(Im(\Phi)) < dim(V)$, then $Ax=0$ has infinitely many solutions.
        - If $dim(V) = dim(W)$, then $\Phi$ is injective $\Leftrightarrow$ $\Phi$ is surjective $\Leftrightarrow$ $\Phi$ is bijective.

16. **Columnspace and Nullspace from Reduced Row Echelon form**:
    - **Columnspace**: span of pivot columns.
    - **Nullspace**: introduce $-e_i$ rows for missing pivots and read the non pivot columns. Nullspace is the span of these modified columns with -1s at missing pivot positions.

17. **Bilinear transformation and Inner Products**: Let $\Omega: V \times V \rightarrow R$ be a bilinear transformation, then:
    - $\Omega$ is linear in first argument:  $\forall x,y,z \in V, \forall\lambda, \psi\in R$
    $$\Omega(\lambda x + \psi y, z) = \lambda\Omega(x, z) + \psi\Omega(y, z)$$
    - $\Omega$ is linear in second argument: $\forall x,y,z \in V, \forall\lambda, \psi\in R$
    $$\Omega(x, \lambda y + \psi z) = \lambda\Omega(x, y) + \psi\Omega(x, z)$$
    - $\Omega$ is **symmetric** if $\forall x, y\in V: \Omega(x, y) = \Omega(y, x)$
    - $\Omega$ is **positive definite** if $\forall x, y \in V/\{0\}: \Omega(x,x)>0$ with $\Omega(0,0)=0$.
    - $\Omega$ is an **inner product** iff it is **symmetric and positive definite**.
    - A vector space with an inner product defined on it is called an **inner product space**.       

18. **Positive definite matrix and Inner Product**:
    - A square matrix $A \in R^{n\times n}$ is positive definite if $x^TAx>0, \ \forall x \in R^n/\{0\}$.
    - Every positive definite matrix $A$ defines an inner product $<x, y> = x^TAy$ with respect to some ordered basis $B$ of $R^n$.
    - Conversely $<.,.>: V\times V\rightarrow R$ is an inner product if there exists a positive definite matrix $A\in R^{n\times n}$ such that $<x,y> = x^TAy$.
    - If $A$ is positive definite, then $ker(A) = \{0\}$.
    - The diagonal elements of $A$ are all positive.

19. **Cauchy Schwarz Inequality**: 
    $$<x, y> \leq ||x||\cdot ||y||$$

20. **Projection with Inner Product**: A vector $x$ is projected onto another vector $b$:

    $$\pi_U(x) = \frac{<b, x>}{<b, b>}b$$

21. **Projecting on to a Basis**: 

    $$\pi_U(x) = B(B^TB)^{-1}B^Tx$$

22. Two vectors are **orthogonal** if their inner product is 0. A square matrix is **orthogonal** if its transpose is its inverse.

23. In 2D, the rotation matrix is given by 

    $$\begin{bmatrix}\cos(\theta) & -\sin(\theta) \\ \sin(\theta) & \cos(\theta)\end{bmatrix}$$

24. **Gram Schmidt Process**: Given a set of basis vectors $B$, we apply Gaussian elimination to the augmented matrix $[BB^T|B]$ to obtain an orthonormal basis. 

## Derivations I worked through

## What confused me (questions for the weekly oral)

- Is commutativity independent of associativity? Which properties are needed and what others can be derived from it - commutativity, associativity, distributive, identity, inverse, etc.?

- I want you to quiz me on groups, abelian groups, vector spaces.

- Proof of the fact that every vector subspace of $R^n$ arises from the solution of a system of homogeneous linear equations.

- Proof of the fact that two vector spaces are isomorphic if they have the same dimensions. Why the dimensions have to be finite?

- Are there any infinite dimensional vector spaces?

- Proof of rank-nullity theorem.

- Proof that the Reduced Row Echelon Form is unique for a matrix. 

- Let $\Phi : R^{m\times n} \rightarrow R^{m \times n}$ be a transformation that maps a matrix $A$ to its Reduced Row Echelon form. Is $\Phi$ a linear transformation? What are its kernel and image, and their dimensions? Since the reduced row echelon form for a matrix is unique, if we fix a particular reduced row echelon form, then the do set of matrices that map to it under $\Phi$ form a subspace of $R^{m\times n}$? Is this analysis just an extension of solving systems of linear equations in matrix vector notation?

- I want an explanation of how the summation operation was manipulated using bilinearity of inner product in 3.10

- I want to understand the proof of the change of bases given in the book - especially the part where indices inside summation get manipulated when we are looking at the transformation in two ways.

- Proof that a symmetric positive definite matrix represents an inner product with respect to some ordered basis and vice versa.

- General Rotations and Givens Rotations are new to me. I am not sure where these will be used later on. 

- Can we get the 2D rotation matrix from differential equaions using matrix exponentials and complex numbers. I saw one such derivation long ago.

- Proof of problem 2.18 and 3.7. I have a very simple one.

## Links to code or exercises

Since I knew most of the material, I tested out of this section by attempting few exercise problems. Currently the notes span sections 2.4 and 2.7 and parts of chapter 3. I will add notes from the other sections in the future. The books contain surprisingly more material than what was covered in the Coursera Mathematics of Machine Learning Specialization offered by the authors.