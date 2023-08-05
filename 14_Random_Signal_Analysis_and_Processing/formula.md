$$f(x) = \begin{cases}
    \frac{x}{2} & x \in [0, 2] \\
    0 & otherwise
\end{cases}$$

$$E(X) = \int_{-\infty}^{+\infty} xf(x) dx \\
\qquad \\
= \int_{0}^{2} \frac{x^2}{2} dx = \frac{4}{3}$$

$$E(X^2) = \int_{-\infty}^{+\infty} x^2 f(x) dx \\
\qquad \\
= \int_{0}^{2} \frac{x^3}{2} dx = 2$$

$$Var(X) = E(X^2) - E^2(X) = \frac{2}{9}$$

$$F(x) = \int_{-\infty}^{x} f(x) dx = \int_{0}^{x} \frac{x}{2} dx = \frac{x^2}{4} \quad (x \in [0, 2])$$

$$F^{-1}(y) = 2 \sqrt{y}$$

$$f_{R}(r) = \begin{cases}
    1 & r \in [0, 1] \\
    0 & otherwise
\end{cases}$$

$$X = F^{-1}(R)$$


$$m_{X} = R_{X}(0) = \frac{1}{1-0.64} 0.8^{|0|} = 0$$

$$C_{X}(m) = R_{X}(m) - m_{X}^{2} = R_{X}(m)$$

$$X(n) + 0.8X(n-1) = W(n)$$

$$h(n) = \frac{1}{1-0.8E^{-1}} = \frac{E}{E-0.8}$$

$$H(\omega) <=> h(n)$$

$$X(n) = h(n) * W(n)$$