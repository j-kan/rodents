library('ggplot2')

h = read.csv("entropy.csv")

qplot(Zone.Transitions, Entropy, data=h, color=Handling, facets = ~ factor(Session), shape=Rat, size=6)

