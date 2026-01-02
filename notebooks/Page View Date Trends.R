base_stats = read.csv("~/Jupyter/analytic_base_2015-2016.csv")
base_stats$tm_stamp = as.Date(base_stats$tm_stamp, "%Y-%m-%d")

base_stats$day = format(base_stats$tm_stamp, format="%d")
visits_day = setNames(aggregate(base_stats$id ~ base_stats$tm_stamp, FUN=function(x) length(unique(x))), c("day", "visits"))

# plot by date
plot(visits_day$day, visits_day$visits, type="l", ylim=c(10000,25000), panel.first=grid(lty=1))

# plot by day
visits_day = setNames(aggregate(base_stats$id ~ base_stats$day, FUN=function(x) length(unique(x))), c("day", "visits"))
total = sum(visits_day$visits)
visits_day$visits = visits_day$visits/total * 100
plot(visits_day$day, visits_day$visits, type="h", lwd=20, ylab="Percentage visits per day", xlab="Day of the month", panel.first=grid(lty=1))
grid(ny=10, nx=0, lty=1)
title(main="Page views distribution across days of the month (3/2015 - 5/2016)")
