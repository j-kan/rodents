library('ggplot2')

h = read.csv("entropy-24-bz.csv")

qplot(Zone.Transitions,         Entropy, data=h, color=Handling, facets = ~Session, shape=Rat, size=6)
qplot(Between.Zone.Transitions, Entropy, data=h, color=Handling, facets = ~Session, shape=Rat, size=6)

