---
title: Using Taylor Series to Improve the Euler Method
author: Alfie Chadwick
date: '2023-12-18'
lastmod: '`r Sys.Date()`'
Tags:
  - Calculus
---


# Euler's Method

Euler's method is a classic way of approximating first-order differential equations.
In short, it uses the derivative of a function and starting condition to estimate the value of the function a short distance from the starting point.

This is commonly written as:

$$
\frac{dy}{dx} = f(x, y)
$$
$$
y(x+h) = y(x) + hf(x, y(x)) + \epsilon
$$
$$
\lim_{h \to 0} |\epsilon| = 0
$$

Where $\epsilon$ is the error created by the approximation.

## Higher Order ODEs

Generalizing Euler's method to higher order ODEs is pretty easy. All you have to do is think of the ODE as a vector with each entry being the next derivative of the function. You can now write Euler's Method in terms of this function:

$$ 
\begin{bmatrix}
y(x+h)\\
y'(x+h)\\
y''(x+h)\\
...\\
y^{n-1}(x+h)\\
\end{bmatrix} = \begin{bmatrix}
y(x)\\
y'(x)\\
y''(x)\\
...\\
y^{n-1}(x)\\
\end{bmatrix} + \begin{bmatrix}
h & 0 & 0 &  ... & 0\\
0 & h & 0 &  ... & 0\\
0 & 0 & h &  ... & 0\\
... & ... & ... &  ... & ...\\
0 & 0 & 0 &  ... & h\\
\end{bmatrix} \cdot \begin{bmatrix}
y'(x)\\
y''(x)\\
y'''(x)\\
...\\
y^{n}(x)\\
\end{bmatrix} + \epsilon
$$

Or shifting the $Y'$ matrix to make it a bit prettier:

$$\begin{bmatrix}
y(x+h)\\
y'(x+h)\\
y''(x+h)\\
...\\
y^{n}(x+h)\\
\end{bmatrix} =  \begin{bmatrix}
1 & h & 0 &  ... & 0\\
0 & 1 & h &  ... & 0\\
0 & 0 & 1 &  ... & 0\\
... & ... & ... &  ... & ...\\
0 & 0 & 0 &  ... & 1\\
\end{bmatrix} \cdot \begin{bmatrix}
y(x)\\
y'(x)\\
y''(x)\\
...\\
y^{n}(x)\\
\end{bmatrix} + \epsilon $$

# Taylor Series

So everything up to now has been pretty textbook. But when I saw the matrix representation of the Euler method, I couldn't help but think of another method that combines derivatives and linear algebra, Taylor Series.
Taylor Series allows you to express functions as a polynomial of their derivatives at a single point $a$, as defined by this equation:

$$
y(x) =  \sum_{n = 0}^{\infty}  \frac{y^{(n)}(a)}{n!}\cdot(x - a)^n 
$$

The link between the Taylor Series and Euler's Method becomes clear when we replace $x$ with $x+h$ and $a$ with $x$:

$$
y(x+h) =  \sum_{n = 0}^{\infty}  \frac{y^{(n)}(x)}{n!}\cdot(h)^n 
$$

$$
y(x+h) = y(x) +  y'(x) \cdot h + \frac{y''(x)}{2!}\cdot(h)^2 + \frac{y'''(x)}{3!}\cdot(h)^3 ...
$$

The first two terms of this expansion are the same as Euler's Method, but the additional terms provide even greater accuracy, minimizing the error in the approximation!

# Putting it together

A nice property of Taylor Series is that they have a really simple derivative function:

$$ y'(a+h) = \sum_{n = 0}^{\infty}  \frac{y^{(n+1)}(a)}{n!}\cdot(h)^n $$
$$ y^{(m)}(a+h) = \sum_{n = 0}^{\infty}  \frac{y^{(n+m)}(a)}{n!}\cdot(h)^n $$

This means that not only the function can be described as a linear combination of the derivatives at a point, but so too can all derivatives of a function.

Using this, we can go back to the initial matrix representation of the Euler method and include these higher order terms.

$$ \begin{bmatrix}
y(x+h)\\
y'(x+h)\\
y''(x+h)\\
...\\
y^{n}(x+h)\\
\end{bmatrix} = \begin{bmatrix}
1 & \frac{h}{1!} & \frac{h^2}{2!} &  ... & \frac{h^n}{n!}\\
0 & 1 & \frac{h}{1!} &  ... & \frac{h^{n-1}}{(n-1)!}\\
0 & 0 & 1 &  ... & \frac{h^{n-2}}{(n-2)!}\\
... & ... & ... &  ... & ...\\
0 & 0 & 0 &  ... & 1\\
\end{bmatrix} \cdot \begin{bmatrix}
y(x)\\
y'(x)\\
y''(x)\\
...\\
y^{n}(x)\\
\end{bmatrix} + \epsilon $$

This should allow us to approximate higher order ODEs with more precision than just using Euler's method.
