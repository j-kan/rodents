library('ggplot2')

h = read.csv("entropy-24-bz.csv")


png("entropy-24-zones.png")
qplot(Zone.Transitions,         Entropy, data=h, color=Handling, facets = ~Session, shape=Rat, size=6)
dev.off()

png("entropy-24-zones-between-zone.png")
qplot(Between.Zone.Transitions, Entropy, data=h, color=Handling, facets = ~Session, shape=Rat, size=6)
dev.off()



hbz = read.csv("h-by-zone.csv")

png("entropy-per-zone.png", width=2000, height=1000)
qplot(Zone, Entropy, data=hbz, geom="jitter", facets = Session ~ Rat, shape = Rat, color=Handling)
dev.off()

png("bz-entropy-per-zone.png", width=2000, height=1000)
qplot(Zone, Between.Zone.Entropy, data=hbz, geom="jitter", facets = Session ~ Rat, shape = Rat, color=Handling)
dev.off()


hbhb = cbind(hbz[hbz$Session == 1,], hbz[hbz$Session == 2,])
names(hbhb)[i] = paste(names(hbhb)[i],(i-1) %/% 8 + 1, sep='.')

hbhb$Handling.2 = NULL
hbhb$Rat.2      = NULL
hbhb$Zone.2     = NULL
hbhb$Session.1  = NULL
hbhb$Session.2  = NULL

names(hbhb)[1]="Handling"
names(hbhb)[2]="Rat"
names(hbhb)[3]="Zone"


hbhb$Diff.Entropy              = hbhb$Entropy.2 - hbhb$Entropy.1
hbhb$Diff.Between.Zone.Entropy = hbhb$Between.Zone.Entropy.2 - hbhb$Between.Zone.Entropy.1
hbhb$Diff.Occupancy            = hbhb$Occupancy.2 - hbhb$Occupancy.1
hbhb$Diff.Out.Transitions      = hbhb$Out.Transitions.2 - hbhb$Out.Transitions.1


png("diff-entropy.png", width=800, height=600)
qplot(Handling, Diff.Entropy, data=hbhb, geom="jitter", facets = ~Zone, shape = Rat, color=Handling)
dev.off()

png("diff-between-zone-entropy.png", width=800, height=600)
qplot(Handling, Diff.Between.Zone.Entropy, data=hbhb, geom="jitter", facets = ~Zone, shape = Rat, color=Handling)
dev.off()



png("diff-entropy-aggregate-over-zones.png", width=600, height=600)
qplot(Handling, Diff.Entropy, data=hbhb, geom=c("boxplot","jitter"), shape = Rat, color=Handling)
dev.off()

png("diff-bz-entropy-aggregate-over-zones.png", width=600, height=600)
qplot(Handling, Diff.Between.Zone.Entropy, data=hbhb, geom=c("boxplot","jitter"), shape = Rat, color=Handling)
dev.off()

png("diff-bz-transitions-over-zones.png", width=400, height=800)
qplot(Handling, Diff.Out.Transitions, data=hbhb, geom=c("boxplot","jitter"), shape = Rat, color=Handling)
dev.off()


hag = aggregate(. ~ Rat, data=hbhb, "sum")


he1 = h[h$Session ==1 & h$Handling=='e',]
he2 = h[h$Session ==2 & h$Handling=='e',]
hn1 = h[h$Session ==1 & h$Handling=='n',]
hn2 = h[h$Session ==2 & h$Handling=='n',]


t.test(hn1$Entropy, hn2$Entropy, paired=TRUE, alternative="greater")
t.test(hn1$Between.Zone.Entropy, hn2$Between.Zone.Entropy, paired=TRUE, alternative="greater")

