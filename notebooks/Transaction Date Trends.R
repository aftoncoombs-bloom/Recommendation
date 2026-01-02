# localize data & transform
transactions = read.csv("~/Jupyter/transactions-comp.csv")
transactions$timestamp = as.Date(transactions$timestamp, "%Y-%m-%d")

vol_by_date = setNames(aggregate(transactions$amount ~ transactions$timestamp, FUN=sum), c("date", "amount"))
count_by_date = setNames(aggregate(transactions$id ~ transactions$timestamp, FUN=function(x) length(unique(x))), c("date", "count"))

###################
# descriptive stats
print("Summary of volume by date")
summary(vol_by_date$amount)
cat("Standard deviation: ", sd(vol_by_date$amount))
cat("Variance: ", var(vol_by_date$amount))
print("Summary of count by date")
summary(count_by_date$count)
cat("Standard deviation: ", sd(count_by_date$count))
cat("Variance: ", var(count_by_date$count))

###################
# plot daily volume
format(vol_by_date$amount, scientific=FALSE)
plot(vol_by_date$date, vol_by_date$amount, type="l", ylim=c(100000, 500000), ylab="Volume", xlab="Date")
# plot linear model to data & plot
abline(lm(vol_by_date$amount ~ vol_by_date$date), col="green", lwd=5)
# smooth line & plot
smoothingSpline = smooth.spline(vol_by_date$date, vol_by_date$amount, spar=0.8)
lines(smoothingSpline, lwd=5, col="blue")

###################
# plot daily count
format(count_by_date$count, scientific=FALSE)
plot(count_by_date$date, count_by_date$count, type="l", ylim=c(0, 5000), ylab="Volume", xlab="Date")
# plot linear model to data & plot
abline(lm(count_by_date$count ~ count_by_date$date), col="green", lwd=5)
# smooth line & plot
smoothingSpline = smooth.spline(count_by_date$date, count_by_date$count, spar=0.8)
lines(smoothingSpline, lwd=5, col="blue")

##################################################
# plot transaction percentages by day of the month
transactions$day = format(transactions$timestamp, "%d")
trans_days = setNames(aggregate(transactions$id ~ transactions$day, FUN=function(x) length(unique(x))), c("day", "count"))
total = sum(trans_days$count)
trans_days$count = trans_days$count/total * 100
plot(trans_days$day, trans_days$count, type="h", ylab="Percentage of Transactions", xlab="Day of the Month", xlim=c(1, 31), ylim=c(2.5, 7.0), lwd=20, panel.first=grid(lty=1))
title(main="Transaction distribution across days of the month (2/2015 - 2/2016)")
cat("Standard deviation: ", var(trans_days$count))
cat("Variance: ", var(trans_days$count))
cat("Excluding the 1st & 15th of the month...")
cat("Standard deviation: ", sd(trans_days[!(trans_days$day == '01' | trans_days$day == '15'),]$count))
cat("Variance: ", var(trans_days[!(trans_days$day == '01' | trans_days$day == '15'),]$count))

