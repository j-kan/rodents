library('ggplot2')

x36   = read.csv("X36TrackData-5-26-11/h.csv")
x36ws = read.csv("X36TrackData-5-26-11/wse.csv")
x36z  = read.csv("X36TrackData-5-26-11/infogain-by-zone.csv")

xcu   = read.csv("X38TrackData-cppusl/h.csv")
xcuws = read.csv("X38TrackData-cppusl/wse.csv")
#xcuws6 = read.csv("X38TrackData-cppusl/wse6.csv")
xcuz  = read.csv("X38TrackData-cppusl/infogain-by-zone.csv")

xx = rbind(x36, xcu)
xws = rbind(x36ws, xcuws)
xz  = rbind(x36z, xcuz)

#------- by session

#--- treatment_vs_session boxplots

ggplot(xx,   aes(x = factor(Session),
                 y = Distance, 
                 colour = Treatment, 
                 shape = Rat)) + facet_grid(~Treatment) + geom_boxplot() + geom_jitter(size=3) + xlab("Session")

ggplot(xx,   aes(x = factor(Session),
                 y = Entropy, 
                 colour = Treatment, 
                 shape = Rat)) + facet_grid(~Treatment) + geom_boxplot() + geom_jitter(size=3) + xlab("Session")

ggplot(xx,   aes(x = factor(Session),
                 y = Cond.Entropy, 
                 colour = Treatment, 
                 shape = Rat)) + facet_grid(~Treatment) + geom_boxplot() + geom_jitter(size=3) + xlab("Session")

ggplot(xx,   aes(x = factor(Session),
                 y = Entropy/Distance, 
                 colour = Treatment, 
                 shape = Rat)) + facet_grid(~Treatment) + geom_boxplot() + geom_jitter(size=3) + xlab("Session")


#--- treatment_vs_session lines + boxplots

ggplot(xx, aes(x       = Session,
               y       = Distance, 
               colour  = Treatment)) + 
      facet_grid(~Treatment) + 
      geom_boxplot(aes(group=factor(Session)), alpha=0.4, color="grey40", size=0.2) + 
      geom_line(aes(group = Rat), size=1.5) + 
      scale_x_continuous(breaks=c(1,2))

ggplot(xx, aes(x       = Session,
               y       = Entropy, 
               colour  = Treatment)) + 
      facet_grid(~Treatment) + 
      geom_boxplot(aes(group=factor(Session)), alpha=0.4, color="grey40", size=0.2) + 
      geom_line(aes(group = Rat), size=1.5) + 
      scale_x_continuous(breaks=c(1,2))

ggplot(xx, aes(x       = Session,
               y       = Entropy/Distance, 
               colour  = Treatment)) + 
      facet_grid(~Treatment) + 
      geom_boxplot(aes(group=factor(Session)), alpha=0.4, color="grey40", size=0.2) + 
      geom_line(aes(group = Rat), size=1.5) + 
      scale_x_continuous(breaks=c(1,2))

ggplot(xx, aes(x       = Session,
               y       = Cond.Entropy,
               colour  = Treatment)) + 
      facet_grid(~Treatment) + 
      geom_boxplot(aes(group=factor(Session)), alpha=0.4, color="grey40", size=0.2) + 
      geom_line(aes(group = Rat), size=1.5) + 
      scale_x_continuous(breaks=c(1,2))

ggplot(xx, aes(x       = Session,
               y       = Cond.Entropy/Distance, 
               colour  = Treatment)) + 
      facet_grid(~Treatment) + 
      geom_boxplot(aes(group=factor(Session)), alpha=0.4, color="grey40", size=0.2) + 
      geom_line(aes(group = Rat), size=1.5) + 
      scale_x_continuous(breaks=c(1,2))

ggplot(xx, aes(x       = Session,
               y       = X.Zone.Transitions/Distance, 
               colour  = Treatment)) + 
      facet_grid(~Treatment) + 
      geom_boxplot(aes(group=factor(Session)), alpha=0.4, color="grey40", size=0.2) + 
      geom_line(aes(group = Rat), size=1.5) + 
      scale_x_continuous(breaks=c(1,2))

ggplot(xx, aes(x       = Session,
               y       = X.Zone.Cond.Entropy/Distance,
               colour  = Treatment)) + 
      facet_grid(~Treatment) + 
      geom_boxplot(aes(group=factor(Session)), alpha=0.4, color="grey40", size=0.2) + 
      geom_line(aes(group = Rat), size=1.5) + 
      scale_x_continuous(breaks=c(1,2))


#--- vs_distance
                     
ggd = ggplot(xx, aes(x = Distance,
                     y = X.Zone.Cond.Entropy, 
                     colour = Treatment,
                     shape=Rat))

ggd + facet_grid(Treatment~Session) + geom_boxplot(alpha=0.4, color="grey40", size=0.2) + stat_smooth(size=1, method="lm") + geom_point(size=5) 

ggplot(xx, aes(x      = Distance,
               y      = X.Zone.Transitions/Distance, 
               colour = Treatment,
               shape  = Rat)) +
      facet_grid(Treatment~Session) + 
      geom_boxplot(alpha=0.4, color="grey40", size=0.2) + 
      geom_point(size=5) 

ggplot(xx, aes(x      = Distance,
               y      = Entropy/Distance, 
               colour = Treatment,
               shape  = Rat)) +
      facet_grid(Treatment~Session) + 
      geom_boxplot(alpha=0.4, color="grey40", size=0.2) + 
      geom_point(size=5) 


ggplot(xx, aes(x      = X.Zone.Transitions/Distance,
               y      = Cond.Entropy/Distance, 
               colour = Treatment,
               group  = Session,     
               shape  = Rat)) +
      facet_grid(~Treatment) + 
      geom_boxplot(alpha=0.4, color="grey40", size=0.2) + 
      geom_line(aes(group = Rat)) + 
      geom_point(aes(size=Session*4)) + scale_size(to=c(4,8), breaks=c(4,8), name="Session", labels=c("1","2"))

#------- by epoch

ggp = ggplot(xws, 
             aes(x = Epoch,
                 y = X.Zone.Transitions, 
                 colour = Treatment, 
                 shape = Rat,
                 group = Rat))

ggp + facet_grid(Treatment~Session) + geom_line()

ggplot(xws, 
       aes(x       = Epoch,
           y       = Distance, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))


ggplot(xws, 
       aes(x       = Epoch,
           y       = Entropy, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))

ggplot(xws, 
       aes(x       = Epoch,
           y       = Cond.Entropy, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))

ggplot(xws, 
       aes(x       = Epoch,
           y       = X.Zone.Transitions, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))

ggplot(xws, 
       aes(x       = Epoch,
           y       = X.Zone.Cond.Entropy, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))

ggplot(xws, 
       aes(x       = Epoch,
           y       = Entropy/Distance, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))

ggplot(xws, 
       aes(x       = Epoch,
           y       = Cond.Entropy/Distance, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))

ggplot(xws, 
       aes(x       = Epoch,
           y       = X.Zone.Transitions/Distance, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))

ggplot(xws, 
       aes(x       = Epoch,
           y       = X.Zone.Cond.Entropy/Distance, 
           colour  = Treatment)) + 
    facet_grid(Treatment~Session) + 
    geom_boxplot(aes(group=factor(Epoch)), alpha=0.4, color="grey40", size=0.2) + 
    geom_line(aes(group = Rat), size=0.5) + 
    scale_x_continuous(breaks=c(0,1,2))

    
#------- by zone
    
ggplot(xz, aes(x      = Session,
               y      = Occupancy, 
               colour = Treatment, 
               group  = Rat)) +
    facet_grid(~Zone) + 
    geom_line() + scale_x_continuous(limits = c(1,2), breaks=c(1,2)) 

ggplot(xz, aes(x      = Session,
               y      = Occupancy, 
               colour = Treatment, 
               group  = Rat)) +
    facet_grid(~Zone) + 
    geom_line(alpha=0.3) + 
    scale_x_continuous(limits = c(1,2), breaks=c(1,2)) 

ggpz = ggplot(xz, 
              aes(x = factor(Session),
                  y = Entropy, 
                  colour = Treatment, 
                  shape = Rat))

ggpz + facet_grid(~Zone) + geom_boxplot() + geom_jitter()

    
