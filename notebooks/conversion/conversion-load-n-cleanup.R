# load data sets
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

# drop irrelevant columns
analytic_data$org.y <- NULL
analytic_data$permit_other_amount <- NULL
analytic_data$permit_create_own_pledge <- NULL
analytic_data$redirect_sms_mobile <- NULL
analytic_data$opt_ded_flds <- NULL
analytic_data$ded_types <- NULL
analytic_data$req_ded_flds <- NULL
analytic_data$event_stats <- NULL
analytic_data$max_amount <- NULL
analytic_data$min_amount <- NULL
analytic_data$enable_donorlogins <- NULL
analytic_data$collect_phone <- NULL
analytic_data$collect_company <- NULL
analytic_data$collect_optin <- NULL
analytic_data$permit_international <- NULL
analytic_data$show_amount <- NULL
analytic_data$collect_address_mobile <- NULL
analytic_data$enable_sms <- NULL
analytic_data$default_recurring_frequency <- NULL
analytic_data$dl_trans_volume <- NULL
analytic_data$dl_trans_count <- NULL
analytic_data$dl_new_rec_count <- NULL
analytic_data$dl_new_rec_volume <- NULL
analytic_data$permit_recurring <- NULL
analytic_data$visits_mobile <- NULL
analytic_data$amounts_system <- NULL
analytic_data$vt_trans_vol <- NULL
analytic_data$vt_trans_count <- NULL
analytic_data$fb_trans_count <- NULL
analytic_data$fb_trans_vol <- NULL
analytic_data$mobilevt_trans_vol <- NULL
analytic_data$mobilevt_trans_count <- NULL
analytic_data$kiosk_trans_count <- NULL
analytic_data$kiosk_trans_vol <- NULL
analytic_data$permit_anonymous <- NULL
analytic_data$permit_mobile <- NULL
analytic_data$reg_count <- NULL
analytic_data$reg_volume <- NULL
analytic_data$sms_trans_vol <- NULL
analytic_data$sms_trans_count <- NULL
analytic_data$new_rec_volume <- NULL
analytic_data$new_rec_count <- NULL
analytic_data$p2p_trans_vol <- NULL
analytic_data$p2p_trans_count <- NULL
analytic_data$events_count <- NULL
analytic_data$events_priv_count <- NULL
analytic_data$pledges_count <- NULL
analytic_data$pledge_active <- NULL
analytic_data$sic <- NULL
analytic_data$ein <- NULL
analytic_data$rec_trans_count <- NULL
analytic_data$rec_trans_vol <- NULL

# create conversion, day & month columns
analytic_data$timestamp <- strptime(analytic_data$timestamp, "%Y-%m-%d %H:%M:%S")
analytic_data$conversion <- analytic_data$don_form_trans_count/analytic_data$total_visits * 100
analytic_data$day <- as.numeric(strftime(analytic_data$timestamp, format="%d"))
analytic_data$month <- as.numeric(strftime(analytic_data$timestamp, format="%m"))
analytic_data$avg_vol <- as.numeric(analytic_data$don_form_trans_vol / analytic_data$don_form_trans_count)

# add complexity & interaction terms
analytic_data$restrictionsXmultirestriction = analytic_data$restrictions*analytic_data$multirestriction_system
analytic_data$restrictions2 = analytic_data$restrictions*analytic_data$restrictions
analytic_data$restrictions2Xmultirestriction = analytic_data$restrictions2*analytic_data$multirestriction_system
analytic_data$restrictions3 = analytic_data$restrictions*analytic_data$restrictions*analytic_data$restrictions
analytic_data$restrictions3Xmultirestriction = analytic_data$restrictions3*analytic_data$multirestriction_system

analytic_data$opt_fields2 = analytic_data$opt_fields^2
analytic_data$opt_fields3 = analytic_data$opt_fields^3
analytic_data$req_fields2 = analytic_data$req_fields^2
analytic_data$req_fields3 = analytic_data$req_fields^3

analytic_data$fields = analytic_data$req_fields+analytic_data$opt_fields
analytic_data$fields2 = analytic_data$fields^2
analytic_data$fields3 = analytic_data$fields^3




