library('ggplot2')

hcppusl = read.csv("cppusl-bigrams.csv")

#h4t = read.csv("s4-t-entropy.csv")
#h4s3et = read.csv("s4-t-wse.csv")

#het = h4s3et[h4s3et$Epoch != 3, ]


png("entropy-cppusl.png")
qplot(Between.Zone.Transitions,         Entropy, data=h4t, color=Treatment, facets = ~Session, shape=Rat, size=6)
dev.off()

png("entropy-t-between-zone.png")
qplot(Between.Zone.Transitions, Entropy, data=h4t, color=Handling, facets = ~Session, shape=Rat, size=6)
dev.off()



ggplot(h4t, aes(x = factor(Session), y = Entropy, colour = Handling, group=Rat))+ geom_line() + geom_point(shape=Rat)
ggplot(h4t, aes(x = factor(Session), y = Entropy, colour = Handling, group=Rat, shape=Rat, size=6))+ geom_line() + geom_point() 

qplot(factor(Session), Entropy, data=h4t, color=Handling, facets = ~Handling, shape=Rat, size=6, geom="jitter")

qplot(factor(Session.Epoch), Entropy, data=h4s3et, color=Handling, facets = ~Handling, shape=Rat, size=6, geom="jitter")
ggplot(het, aes(x = factor(Epoch), y = Entropy, colour = Handling, group=Rat, shape=Rat), facets=~Session)+ geom_line() + geom_point(size=6) 


png("entropy-vs-session.png")
ggplot(h4t, aes(x = factor(Session), y = Entropy, colour = Handling, group=Rat, shape=Rat))+ geom_line() + geom_point(size=6) 
dev.off()

png("zone-transitions-vs-session.png")
ggplot(h4t, aes(x = factor(Session), y = Between.Zone.Transitions, colour = Handling, group=Rat, shape=Rat))+ geom_line() + geom_point(size=6) 
dev.off()



ggplot(h4t, aes(x = factor(Session), y = Entropy, colour = Handling, group=Rat, shape=Rat))+ geom_line() + geom_point(size=6) 



hbz4 = read.csv("s4-by-zone.csv")
hbz4t = read.csv("s4-t-by-zone.csv")

png("entropy-per-zone.png", width=2000, height=1000)
qplot(Zone, Entropy, data=hbz4, geom="jitter", facets = Session ~ Rat, shape = Rat, color=Handling)
dev.off()

png("bz-entropy-per-zone.png", width=2000, height=1000)
qplot(Zone, Between.Zone.Entropy, data=hbz4, geom="jitter", facets = Session ~ Rat, shape = Rat, color=Handling)
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






hbye = read.csv("wse.csv")

png("h-by-epoch.png",width=500,height=600)
qplot(factor(Epoch), Entropy, data=hbye, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()

png("bz-transitions-by-epoch.png",width=500,height=600)
qplot(factor(Epoch), Between.Zone.Transitions, data=hbye, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()

hbye3 = read.csv("wse3.csv")

png("bz-transitions-by-3-epochs.png",width=500,height=600)
qplot(factor(Epoch), Between.Zone.Transitions, data=hbye3, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()

png("h-by-3-epochs.png",width=500,height=600)
qplot(factor(Epoch), Entropy, data=hbye3, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()



qplot(factor(Epoch), Entropy, data=het, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))

png("h-t-4-sessions--3-epochs.png",width=1000,height=600)
qplot(factor(Epoch), Entropy, data=het, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()

