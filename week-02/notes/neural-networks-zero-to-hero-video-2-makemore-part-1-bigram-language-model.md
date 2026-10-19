# Video 2: makemore part 1 (bigram language model)

- **Course:** Neural Networks: Zero to Hero (Karpathy)
- **Source:** https://github.com/karpathy/nn-zero-to-hero
- **Date studied:** 18/06/2026

## Key ideas (in my own words)

1. **Language Model** : $p(a_i|a_1, a_2, a_3, ..., a_{i-1})$
    - $a_i$s are individual tokens - they can be words, characters, etc.
    - **Bigram model** (two tokens) - $p(a_i|a_{i-1})$. Independent of other tokens given just the previous token.
    - special starting ($<s>$) and ending ($<e>$) tokens to encode starting and ending of a word.
    - special cases 
        - $p(<s>|.) = 0$, that is, starting token should always come first
        - $p(.|<e>) = 0$, that is, no token can follow the ending token
        - zero length tokens have zero probability $p(<e>|<s>) = 0$
    - *bigrams with 0 counts show up as -inf in the NLL loss*. to avoid this, we **add 1** to all bigram counts. If we add larger value, then the probabilities will be closer to uniform.
    - the bigram probabilities are the parameters of the bigram model.

2. No matter wherever we are in the sequence of tokens (characters or words), the bigram probability will only depend on the previous token. How to add length penalties during sampling:
    - right now we are stopping the generation whenever the end token is sampled.
    - also accumulate the probability of the generated text (product of individual tokens) and once it is lower than a threshold stop.
    - sampling is done using the multinomial distribution with replacement (because same token can occur twice or more)
    - for deterministic sampling, we use a generator and a seed value.

3. **Tensor broadcasting**:
    - it is important to understand if a row operation or a column operation is required and specify the dimension in pytorch commands accordingly.
    - keepdims matters for broadcasting. again, understanding of row or column operation is very important here. 
    - $X \cdot y$ where $\cdot$ is a scalar operation like addition, multiplication, etc. and $X$ is a 2D array while $y$ is a 1D array with shape as $[m]$, then pytorch will consider it as $[1, m]$. the default behaviour is to move this dimension to the right and then do the operation.
    - for conditional probability or transition matrices, it is important to understand whether to normalize along the row or column.

4. **Negative log lokelihood**:
    - Loss function for next token prediction
    - Maximizing likelihood = Maximizing log likelihood = Minimizing negative log likelihood
    - probability values get very small when multiplied, so we use log probabilities

5. **Softmax**:
    - activation of a neural network
    - used in output layers in classification problems
    - outputs a probability distribution
    - output of NN (before softmax): logits = log counts -> exponentiate (counts) -> normalize (softmax = exponentiate and normalize)

6. - weights of the simple neural network implemented in the video correspond to log of the counts in the bigram frequency matrix. in the video, these are identical models.
   - regularization is added to smooth the weights. the regularization strength corresponds to the smoothing value added to the bigrams that are not present in the data.

## Definitions and results



## Derivations I worked through

## What confused me (questions for the weekly oral)

- why append the special token `.` both at the start and the end of the word?
Answer: we are using the same character as start and end markers to make the bigram matrix smaller and discard the 0 rows and columns. it gets encoded in the bigram parameters as the end of word. it is also used during sampling to signify the end of sampling.

## Formula cheat sheet (only if you tested out of this item)


## Links to code or exercises
