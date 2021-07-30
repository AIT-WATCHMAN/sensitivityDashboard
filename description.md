# Sensitivity App
Shown above is a view of an arbitrary detector sensitivity under two selectable
statistical tests. The default is **discovery**, which is the sensitivity to reject
a non-zero hypothesis. The other option is **measurement**, which is the sensitivity
to measure the value of **s** given that **s** is true. The variables in the equation
are defined as:
```c++
Z = Sensitivity in units of σ
s = Signal rate
b = Background rate
t = time (units matching s and b)
σ = Background rate uncertainty
```

The contour plot above shows the time to reach the target sensitivity (defaults to 3 σ).
The plot itself stops at **Max Months** and anything outside that region is set to max,
this is to avoid the large infinite values that exist in that region (experiment is
said to be "systematically limited").
