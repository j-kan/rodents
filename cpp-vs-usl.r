library('ggplot2')

xcu   = read.csv("X38TrackData-cppusl/h.csv")
xcuws = read.csv("X38TrackData-cppusl/wse.csv")
xcuws6 = read.csv("X38TrackData-cppusl/wse6.csv")

diff.frame <- function(frame, colname) {
    s1 = frame[frame[colname] == 1, ]
    s2 = frame[frame[colname] == 2, ]

    names(s1) = paste(names(s1), ".1", sep="")
    names(s2) = paste(names(s2), ".2", sep="")
    
    names(s1)[names(s1) == "Rat.1"] = "Rat"
    names(s2)[names(s2) == "Rat.2"] = "Rat"
    names(s1)[names(s1) == "Treatment.1"] = "Treatment"
    names(s2)[names(s2) == "Treatment.2"] = "Treatment"

    merge(s1, s2)
}


zzcu = diff.frame(xcu, "Session")


zzcu$Diff.Entropy              = zzcu$Entropy.2 - zzcu$Entropy.1
zzcu$Diff.Cond.Entropy         = zzcu$Cond.Entropy.2 - zzcu$Cond.Entropy.1
zzcu$Diff.X.Zone.Cond.Entropy  = zzcu$X.Zone.Cond.Entropy.2 - zzcu$X.Zone.Cond.Entropy.1
zzcu$Diff.X.Zone.Transitions   = zzcu$X.Zone.Transitions.2 - zzcu$X.Zone.Transitions.1


ggpc = ggplot(xcuws, 
              aes(x = Distance, 
              y = Cond.Entropy, 
              colour = Treatment, 
              shape = Rat))

ggpc + facet_grid(Treatment~Session+Epoch) + geom_boxplot() + geom_jitter()

ggpc = ggplot(xcuws, 
              aes(x = factor(Epoch),
              y = Cond.Entropy/Distance, 
              colour = Treatment, 
              shape = Rat))

ggpc + facet_grid(Treatment~Session) + geom_boxplot() + geom_jitter()

ggpc = ggplot(xcuws6, 
              aes(x = factor(Epoch),
              y = Cond.Entropy, 
              colour = Treatment, 
              shape = Rat))

ggpc + facet_grid(Treatment~Session) + geom_boxplot() + geom_jitter()

ggp = ggplot(xcuws6, 
             aes(x = Epoch,
                 y = X.Zone.Transitions, 
                 colour = Treatment, 
                 shape = Rat,
                 group = Rat))

ggp + facet_grid(Treatment~Session) + geom_line()


ggpc = ggplot(xcuws6, 
              aes(x = factor(Epoch),
              y = Cond.Entropy, 
              colour = Rat, 
              group = Rat,
              shape = Rat))

ggpc + facet_grid(Treatment~Session) + geom_line() #+ stat_smooth(method = "lm")




qplot(Distance,         Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance,         X.Zone.Cond.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Cond.Entropy,     X.Zone.Cond.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance, Cond.Entropy/X.Zone.Cond.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance,         X.Zone.Unweighted.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance,         Unweighted.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance,         X.Zone.Transitions, data=xcu, color=Treatment, facets = ~Session, shape=Rat, size=6)
qplot(Distance,         Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance,         X.Zone.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance,         Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance,         X.Zone.Transitions, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(Distance,         X.Zone.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(X.Zone.Transitions,         X.Zone.Cond.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)
qplot(X.Zone.Transitions,         X.Zone.Unweighted.Entropy, data=xcu, color=Treatment, shape=Rat, size=6)


png("entropy-cppusl.png")
qplot(X.Zone.Transitions,         Entropy, data=xcu, color=Treatment, facets = ~Session, shape=Rat, size=6)
dev.off()

png("entropy-t-between-zone.png")
qplot(X.Zone.Transitions, Entropy, data=h4t, color=Handling, facets = ~Session, shape=Rat, size=6)
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
ggplot(h4t, aes(x = factor(Session), y = X.Zone.Transitions, colour = Handling, group=Rat, shape=Rat))+ geom_line() + geom_point(size=6) 
dev.off()



ggplot(h4t, aes(x = factor(Session), y = Entropy, colour = Handling, group=Rat, shape=Rat))+ geom_line() + geom_point(size=6) 



hbz4 = read.csv("s4-by-zone.csv")
hbz4t = read.csv("s4-t-by-zone.csv")

png("entropy-per-zone.png", width=2000, height=1000)
qplot(Zone, Entropy, data=hbz4, geom="jitter", facets = Session ~ Rat, shape = Rat, color=Handling)
dev.off()

png("bz-entropy-per-zone.png", width=2000, height=1000)
qplot(Zone, X.Zone.Entropy, data=hbz4, geom="jitter", facets = Session ~ Rat, shape = Rat, color=Handling)
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
hbhb$Diff.X.Zone.Entropy = hbhb$X.Zone.Entropy.2 - hbhb$X.Zone.Entropy.1
hbhb$Diff.Occupancy            = hbhb$Occupancy.2 - hbhb$Occupancy.1
hbhb$Diff.Out.Transitions      = hbhb$Out.Transitions.2 - hbhb$Out.Transitions.1


png("diff-entropy.png", width=800, height=600)
qplot(Handling, Diff.Entropy, data=hbhb, geom="jitter", facets = ~Zone, shape = Rat, color=Handling)
dev.off()

png("diff-between-zone-entropy.png", width=800, height=600)
qplot(Handling, Diff.X.Zone.Entropy, data=hbhb, geom="jitter", facets = ~Zone, shape = Rat, color=Handling)
dev.off()



png("diff-entropy-aggregate-over-zones.png", width=600, height=600)
qplot(Handling, Diff.Entropy, data=hbhb, geom=c("boxplot","jitter"), shape = Rat, color=Handling)
dev.off()

png("diff-bz-entropy-aggregate-over-zones.png", width=600, height=600)
qplot(Handling, Diff.X.Zone.Entropy, data=hbhb, geom=c("boxplot","jitter"), shape = Rat, color=Handling)
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
t.test(hn1$X.Zone.Entropy, hn2$X.Zone.Entropy, paired=TRUE, alternative="greater")






hbye = read.csv("wse.csv")

png("h-by-epoch.png",width=500,height=600)
qplot(factor(Epoch), Entropy, data=hbye, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()

png("bz-transitions-by-epoch.png",width=500,height=600)
qplot(factor(Epoch), X.Zone.Transitions, data=hbye, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()

hbye3 = read.csv("wse3.csv")

png("bz-transitions-by-3-epochs.png",width=500,height=600)
qplot(factor(Epoch), X.Zone.Transitions, data=hbye3, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()

png("h-by-3-epochs.png",width=500,height=600)
qplot(factor(Epoch), Entropy, data=hbye3, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()



qplot(factor(Epoch), Entropy, data=het, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))

png("h-t-4-sessions--3-epochs.png",width=1000,height=600)
qplot(factor(Epoch), Entropy, data=het, facets=Handling~Session, color=Handling, shape=Rat, geom=c("boxplot","jitter"))
dev.off()

