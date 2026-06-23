# Method Section Writing Guide

## Core Principle: Intuition First, Then Formalization

For each component:
1. Intuitive explanation (1-2 paragraphs, no math)
2. Formal definition (equations, algorithms)
3. Implementation details (practical considerations)

## Structure

### 3.1 Overview / Problem Setup
- Define the problem formally
- State assumptions clearly
- Introduce notation that will be used throughout

### 3.2 [Component 1]
- Motivation: Why do we need this?
- Intuition: How does it work in plain language?
- Formulation: Mathematical definition
- Implementation: How to compute it efficiently

### 3.3 [Component 2]
- Same structure as 3.2

### 3.4 Training / Inference
- How the components fit together
- Training objective
- Inference procedure
- Computational complexity analysis

## Symbol Table Consistency

Define all symbols in a consistent way:
- Lowercase (x, y, z) for scalars
- Bold lowercase (**x**, **y**) for vectors
- Uppercase (X, Y, Z) for matrices
- Calligraphic (𝒳, 𝒴) for sets/distributions
- Same symbol = same meaning throughout the paper

## Algorithm Pseudocode Norms

```latex
\begin{algorithm}[t]
\caption{[Algorithm Name]}
\label{alg:[label]}
\begin{algorithmic}[1]
\REQUIRE Input: $\mathbf{X}$, hyperparameters
\ENSURE Output: $\mathbf{Y}$
\STATE Initialize $\theta$ with [method]
\FOR{each epoch}
  \STATE $\mathbf{Z} \leftarrow \text{Component1}(\mathbf{X}, \theta)$
  \STATE $\mathcal{L} \leftarrow \text{Loss}(\mathbf{Z}, \mathbf{Y})$
  \STATE Update $\theta$ via $\nabla_\theta \mathcal{L}$
\ENDFOR
\RETURN $\theta$
\end{algorithmic}
\end{algorithm}
```

## Figure-First Principle
- Method overview figure should appear BEFORE the detailed description
- Refer to the figure in the text: "As shown in Figure 2, our method consists of..."
- The figure should convey the key idea even without reading the text
