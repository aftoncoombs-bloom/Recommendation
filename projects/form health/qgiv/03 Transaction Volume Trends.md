# Data prep

```{r}
analytic_base <- read.csv("~/Repositories/datasets/analytic_base.csv")
analytic_qgiv_stats <- read.csv("~/Repositories/datasets/analytic_qgiv_stats.csv")
transactions <- read.csv("~/Repositories/datasets/transactions.csv")

# merge dataframes
analytic_data <- merge(analytic_base, analytic_qgiv_stats, by.x="id", by.y="base")
rm(analytic_base)
rm(analytic_qgiv_stats)
analytic_data <- analytic_data[analytic_data$total_visits > 0,]
# remove duplicate columns (ie, ID)
analytic_data <- analytic_data[, !duplicated(colnames(analytic_data))]

df <- analytic_data

# create conversion, day & month columns
df$timestamp <- strptime(df$timestamp, "%Y-%m-%d %H:%M:%S")
df$conversion <- df$don_form_trans_count/df$total_visits * 100
df$day <- as.numeric(strftime(df$timestamp, format="%d"))
df$dayofweek <- as.factor(strftime(df$timestamp, format="%A"))
df$month <- as.numeric(strftime(df$timestamp, format="%m"))
df$hour <- as.numeric(strftime(df$timestamp, format="%H"))
```

_no outliers were removed from this dataset_

___

# Overall conversion & volume

```{r}
# aggregate conversion by time denominations - analytics tables
## month
agg.month.vol = aggregate(df$don_form_trans_vol ~ df$month, FUN=sum)
agg.month.conv = aggregate(df$conversion ~ df$month, FUN=mean)
## day of the month
agg.day.vol = aggregate(df$don_form_trans_vol ~ df$day, FUN=sum)
agg.day.conv = aggregate(df$conversion ~ df$day, FUN=mean)
## day of the week
agg.dayofweek.vol = aggregate(df$don_form_trans_vol ~ df$dayofweek, FUN=sum)
agg.dayofweek.conv = aggregate(df$conversion ~ df$dayofweek, FUN=mean)
## hour
agg.hour.vol = aggregate(df$don_form_trans_vol ~ df$hour, FUN=sum)
agg.hour.conv = aggregate(df$conversion ~ df$hour, FUN=mean)

# aggregate volume from transaction table
trans = transactions
rm(transactions)
trans$timestamp = strptime(trans$timestamp, "%Y-%m-%d %H:%M:%S")
trans$day <- as.numeric(strftime(trans$timestamp, format="%d"))
trans$dayofweek <- factor(strftime(trans$timestamp, format="%A"), levels=c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"))
trans$month <- as.numeric(strftime(trans$timestamp, format="%m"))
trans$hour <- as.numeric(strftime(trans$timestamp, format="%H"))
agg.month.tvol = aggregate(trans$amount ~ trans$month, FUN=sum)
agg.day.tvol = aggregate(trans$amount ~ trans$day, FUN=sum)
agg.dayofweek.tvol = aggregate(trans$amount ~ trans$dayofweek, FUN=sum)
agg.dayofweek.conv = aggregate(df$conversion ~ df$dayofweek, FUN=sum)
agg.hour.tvol = aggregate(trans$amount ~ trans$hour, FUN=sum)

# visualization
## volume
par(mfrow=c(2,2))
### top left
plot(agg.month.tvol, col="blue", type="l", lwd=2, ylab=NA, xlab="Month", yaxt='n')
### top right
plot(agg.day.tvol, col="blue", type="l", lwd=2, ylab=NA, xlab="Day of Month", yaxt='n')
### bottom left
plot(agg.dayofweek.tvol, col="blue", type="l", lwd=2, ylab=NA, xlab="Day of Week", yaxt='n')
### bottom right
plot(agg.hour.tvol, col="blue", type="l", lwd=2, ylab=NA, xlab="Hour", yaxt='n')
title("Volume", outer=TRUE)

## conversion
par(mfrow=c(2,2))
plot(agg.month.tvol, col="blue", type="l", lwd=2, ylab=NA, xlab="Month", yaxt='n')
par(new = T)
with(agg.month.conv, plot(agg.month.conv, pch=16, axes=F, xlab=NA, ylab=NA, yaxt='n', type="l", col="red", lwd=2))
legend("topleft", legend=c(expression("Volume", "Conversion")), lty=c(1,1), col=c("blue", "red"))
## top right
plot(agg.day.tvol, col="blue", type="l", lwd=2, ylab=NA, xlab="Day of Month", yaxt='n')
par(new = T)
with(agg.day.conv, plot(agg.day.conv, pch=16, axes=F, xlab=NA, ylab=NA, yaxt='n', type="l", col="red", lwd=2))
legend("topleft", legend=c(expression("Volume", "Conversion")), lty=c(1,1), col=c("blue", "red"))
## bottom left
plot(agg.dayofweek.tvol, col="blue", type="l", lwd=2, ylab=NA, xlab="Day of Week", yaxt='n')
par(new = T)
with(agg.dayofweek.conv, plot(agg.dayofweek.conv, pch=16, axes=F, xlab=NA, ylab=NA, yaxt='n', type="l", col="red", lwd=2))
legend("topleft", legend=c(expression("Volume", "Conversion")), lty=c(1,1), col=c("blue", "red"))
## bottom right
plot(agg.hour.vol, col="blue", type="l", lwd=2, ylab=NA, xlab="Hour", yaxt='n')
par(new = T)
with(agg.hour.conv, plot(agg.hour.conv, pch=16, axes=F, xlab=NA, ylab=NA, yaxt='n', type="l", col="red", lwd=2))
legend("topleft", legend=c(expression("Volume", "Conversion")), lty=c(1,1), col=c("blue", "red"))
title("Conversion", outer=TRUE)
```

![volume plots.jpeg](../../resources/92D0A17F9CD70F41F189682ED0AF3DE3.jpg)

![conversion plots.jpeg](../../resources/A22D143E9C2189C163D636FE01E2ADAB.jpg)

_Note data from the analytics tables is bucketed into the times when the snapshot scripts run. Hence, when viewing the hourly breakdown of conversion it appears to step dramatically before falling to 0, then stepping again. The peak appears to be around 3PM (15) which would be consistent with the transaction data appearing to peak in volume around 12PM or 1PM as 3PM would be the next time the snapshot scripts had an opportunity to collect information._

___

# Breaking down transactions by type (one time vs recurring) and source

## Prep

```r
trans$source = as.factor(trans$source)
trans$is_recurring = FALSE
trans[trans$recurring!=0 | trans$recurring_creatingTransaction!=0,]$is_recurring = TRUE
```

## One time transaction volume

```r
# break down trends by source & recurring
trans.don_form = trans[trans$source=='don_form',]
agg.month.don_form_vol = aggregate(trans.don_form$amount ~ trans.don_form$month, FUN=sum)
agg.day.don_form_vol = aggregate(trans.don_form$amount ~ trans.don_form$day, FUN=sum)
agg.dayofweek.don_form_vol = aggregate(trans.don_form$amount ~ trans.don_form$dayofweek, FUN=sum)
agg.hour.don_form_vol = aggregate(trans.don_form$amount ~ trans.don_form$hour, FUN=sum)

par(mfrow=c(2,2))
plot(agg.month.don_form_vol, type="l", yaxt='n', ylab=NA, xlab="Month", lwd=2)
plot(agg.hour.don_form_vol, type="l", yaxt='n', ylab=NA, xlab="Hour", lwd=2)
plot(agg.day.don_form_vol, type="l", yaxt='n', ylab=NA, xlab="Day", lwd=2)
plot(agg.dayofweek.don_form_vol, type="l", yaxt='n', ylab=NA, xlab="Day of the Week", lwd=2)
```

![trans-vol-one-time.jpeg](../../resources/9605013D11C82CEB4EBE94DEB01D0E1B.jpg)

## Facebook transaction volume

```r
trans.fb = trans[trans$source=='fb',]
agg.month.fb_vol = aggregate(trans.fb$amount ~ trans.fb$month, FUN=sum)
agg.day.fb_vol = aggregate(trans.fb$amount ~ trans.fb$day, FUN=sum)
agg.dayofweek.fb_vol = aggregate(trans.fb$amount ~ trans.fb$dayofweek, FUN=sum)
agg.hour.fb_vol = aggregate(trans.fb$amount ~ trans.fb$hour, FUN=sum)

par(mfrow=c(2,2))
plot(agg.month.fb_vol, type="l", yaxt='n', ylab=NA, xlab="Month", lwd=2)
plot(agg.hour.fb_vol, type="l", yaxt='n', ylab=NA, xlab="Hour", lwd=2)
plot(agg.day.fb_vol, type="l", yaxt='n', ylab=NA, xlab="Day", lwd=2)
plot(agg.dayofweek.fb_vol, type="l", yaxt='n', ylab=NA, xlab="Day of the Week", lwd=2)
```

![trans-vol-fb.jpeg](../../resources/48B7A29A038A7545F85408D77CDBB594.jpg)

## Kiosk transaction volume

```r
trans.kiosk = trans[trans$source=='kiosk',]
agg.month.kiosk_vol = aggregate(trans.kiosk$amount ~ trans.kiosk$month, FUN=sum)
agg.day.kiosk_vol = aggregate(trans.kiosk$amount ~ trans.kiosk$day, FUN=sum)
agg.dayofweek.kiosk_vol = aggregate(trans.kiosk$amount ~ trans.kiosk$dayofweek, FUN=sum)
agg.hour.kiosk_vol = aggregate(trans.kiosk$amount ~ trans.kiosk$hour, FUN=sum)

par(mfrow=c(2,2))
plot(agg.month.kiosk_vol, type="l", yaxt='n', ylab=NA, xlab="Month", lwd=2)
plot(agg.hour.kiosk_vol, type="l", yaxt='n', ylab=NA, xlab="Hour", lwd=2)
plot(agg.day.kiosk_vol, type="l", yaxt='n', ylab=NA, xlab="Day", lwd=2)
plot(agg.dayofweek.kiosk_vol, type="l", yaxt='n', ylab=NA, xlab="Day of the Week", lwd=2)
```

![trans-vol-kiosk.jpeg](../../resources/A6A0EE0696143C493B08224CF6C40019.jpg)

## Mobile transaction volume

```r
trans.mobile = trans[trans$source=='mobile',]
agg.month.mobile_vol = aggregate(trans.mobile$amount ~ trans.mobile$month, FUN=sum)
agg.day.mobile_vol = aggregate(trans.mobile$amount ~ trans.mobile$day, FUN=sum)
agg.dayofweek.mobile_vol = aggregate(trans.mobile$amount ~ trans.mobile$dayofweek, FUN=sum)
agg.hour.mobile_vol = aggregate(trans.mobile$amount ~ trans.mobile$hour, FUN=sum)

par(mfrow=c(2,2))
plot(agg.month.mobile_vol, type="l", yaxt='n', ylab=NA, xlab="Month", lwd=2)
plot(agg.hour.mobile_vol, type="l", yaxt='n', ylab=NA, xlab="Hour", lwd=2)
plot(agg.day.mobile_vol, type="l", yaxt='n', ylab=NA, xlab="Day", lwd=2)
plot(agg.dayofweek.mobile_vol, type="l", yaxt='n', ylab=NA, xlab="Day of the Week", lwd=2)
```

![trans-vol-mobile.jpeg](../../resources/E582413B662222EF162EAB2F0F687E63.jpg)

## Mobile VT transaction volume

```r
trans.mobilevt = trans[trans$source=='mobilevt',]
agg.month.mobilevt_vol = aggregate(trans.mobilevt$amount ~ trans.mobilevt$month, FUN=sum)
agg.day.mobilevt_vol = aggregate(trans.mobilevt$amount ~ trans.mobilevt$day, FUN=sum)
agg.dayofweek.mobilevt_vol = aggregate(trans.mobilevt$amount ~ trans.mobilevt$dayofweek, FUN=sum)
agg.hour.mobilevt_vol = aggregate(trans.mobilevt$amount ~ trans.mobilevt$hour, FUN=sum)

par(mfrow=c(2,2))
plot(agg.month.mobilevt_vol, type="l", yaxt='n', ylab=NA, xlab="Month", lwd=2)
plot(agg.hour.mobilevt_vol, type="l", yaxt='n', ylab=NA, xlab="Hour", lwd=2)
plot(agg.day.mobilevt_vol, type="l", yaxt='n', ylab=NA, xlab="Day", lwd=2)
plot(agg.dayofweek.mobilevt_vol, type="l", yaxt='n', ylab=NA, xlab="Day of the Week", lwd=2)
```

![trans-vol-mobilevt.jpeg](../../resources/88C0B75D72A854C5443EB67B37A6EAB7.jpg)

## P2P transaction volume

```r
trans.p2p = trans[trans$source=='p2p',]
agg.month.p2p_vol = aggregate(trans.p2p$amount ~ trans.p2p$month, FUN=sum)
agg.day.p2p_vol = aggregate(trans.p2p$amount ~ trans.p2p$day, FUN=sum)
agg.dayofweek.p2p_vol = aggregate(trans.p2p$amount ~ trans.p2p$dayofweek, FUN=sum)
agg.hour.p2p_vol = aggregate(trans.p2p$amount ~ trans.p2p$hour, FUN=sum)

par(mfrow=c(2,2))
plot(agg.month.p2p_vol, type="l", yaxt='n', ylab=NA, xlab="Month", lwd=2)
plot(agg.hour.p2p_vol, type="l", yaxt='n', ylab=NA, xlab="Hour", lwd=2)
plot(agg.day.p2p_vol, type="l", yaxt='n', ylab=NA, xlab="Day", lwd=2)
plot(agg.dayofweek.p2p_vol, type="l", yaxt='n', ylab=NA, xlab="Day of the Week", lwd=2)
```

![trans-vol-p2p.jpeg](../../resources/C80EB3422078F992CE60E43E9807C01E.jpg)

## SMS transaction volume

```r
trans.sms = trans[trans$source=='sms',]
agg.month.sms_vol = aggregate(trans.sms$amount ~ trans.sms$month, FUN=sum)
agg.day.sms_vol = aggregate(trans.sms$amount ~ trans.sms$day, FUN=sum)
agg.dayofweek.sms_vol = aggregate(trans.sms$amount ~ trans.sms$dayofweek, FUN=sum)
agg.hour.sms_vol = aggregate(trans.sms$amount ~ trans.sms$hour, FUN=sum)

par(mfrow=c(2,2))
plot(agg.month.sms_vol, type="l", yaxt='n', ylab=NA, xlab="Month", lwd=2)
plot(agg.hour.sms_vol, type="l", yaxt='n', ylab=NA, xlab="Hour", lwd=2)
plot(agg.day.sms_vol, type="l", yaxt='n', ylab=NA, xlab="Day", lwd=2)
plot(agg.dayofweek.sms_vol, type="l", yaxt='n', ylab=NA, xlab="Day of the Week", lwd=2)
```

![trans-vol-sms.jpeg](../../resources/B0ABB9334C36A49CE375B8ED06A67485.jpg)

## VT transaction volume

```r
trans.vt = trans[trans$source=='vt' | trans$source=='VT',]
agg.month.vt_vol = aggregate(trans.vt$amount ~ trans.vt$month, FUN=sum)
agg.day.vt_vol = aggregate(trans.vt$amount ~ trans.vt$day, FUN=sum)
agg.dayofweek.vt_vol = aggregate(trans.vt$amount ~ trans.vt$dayofweek, FUN=sum)
agg.hour.vt_vol = aggregate(trans.vt$amount ~ trans.vt$hour, FUN=sum)

par(mfrow=c(2,2))
plot(agg.month.vt_vol, type="l", yaxt='n', ylab=NA, xlab="Month", lwd=2)
plot(agg.hour.vt_vol, type="l", yaxt='n', ylab=NA, xlab="Hour", lwd=2)
plot(agg.day.vt_vol, type="l", yaxt='n', ylab=NA, xlab="Day", lwd=2)
plot(agg.dayofweek.vt_vol, type="l", yaxt='n', ylab=NA, xlab="Day of the Week", lwd=2)
```

![trans-vol-vt.jpeg](../../resources/2D8F07F48536CEA8807EF0667B716B07.jpg)