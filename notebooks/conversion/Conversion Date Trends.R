library(ggplot2)

# localize transaction data
transactions = read.csv("~/Jupyter/transactions-comp.csv")
transactions$timestamp = as.Date(transactions$timestamp, "%Y-%m-%d %H:%M:%S")
transactions$day = format(transactions$timestamp, "%Y-%m-%d")

# localize analytics data
base_stats = read.csv("~/Jupyter/analytic_base_2015-2016.csv")
base_stats$tm_stamp = as.Date(base_stats$tm_stamp, "%Y-%m-%d %H:%M:%S")
base_stats$day = format(base_stats$tm_stamp, "%Y-%m-%d")

# aggregate transaction counts, volumes, & page views by date
trans_count_days = setNames(aggregate(transactions$id ~ transactions$day, FUN=function(x) length(unique(x))), c("date", "count"))
trans_vol_days = setNames(aggregate(transactions$amount ~ transactions$day, FUN=sum), c("date", "volume"))
visits_day = setNames(aggregate(base_stats$id ~ base_stats$tm_stamp, FUN=function(x) length(unique(x))), c("date", "visits"))

# merge into single data set for {date, count, amount, visits}
trans_days = merge(trans_count_days, trans_vol_days, by.x="date")
trans_by_date = merge(trans_days, visits_day, by.x="date")

# set the day of the month value
trans_by_date$day_of_month = format(trans_by_date$date, "%d")

# box plot for day of the month v conversion rate
p = ggplot(trans_by_date, aes(day_of_month, conversion)) + geom_boxplot()
p + scale_y_continuous(breaks=c(5, 10, 15, 20, 25, 40), name="Conversion Rate") + scale_x_discrete(name="Day of the Month")
