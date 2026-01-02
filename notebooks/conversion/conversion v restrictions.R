library(ggplot2)
source("~/Repositories/Recommendation/notebooks/conversion-load-n-cleanup.R")

# conversion v restrictions fit
df <- analytic_data[analytic_data$conversion < 500,]
df <- df[df$restrictions < 150,]
fit.restrictions <- lm(conversion ~ restrictions + restrictions2 + restrictions3 + multirestriction_system + restrictionsXmultirestriction + restrictions2Xmultirestriction, data=df)

summary(fit.restrictions)

anova(fit.restrictions)

layout(matrix(c(1,2,3,4),2,2))
plot(fit.restrictions)

plot(df$restrictions, df$conversion)
lines(sort(df$restrictions), fitted(fit.restrictions)[order(df$restrictions)], col='red', type='b')

prd <- df[1:200,]
err <- predict(fit.restrictions, newdata=prd, se.fit = TRUE)

prd$lci <- err$fit - 1.96 * err$se.fit
prd$fit <- err$fit
prd$uci <- err$fit + 1.96 * err$se.fit

ggplot(prd, aes(x = restrictions, y = fit)) +
  theme_bw() +
  geom_line() +
  geom_smooth(aes(ymin = lci, ymax = uci), stat = "identity") +
  geom_point(data = df, aes(x = restrictions, y = conversion))

