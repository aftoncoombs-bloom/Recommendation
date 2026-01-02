import sys
sys.path.insert(1, '../../scripts/')
from s3_support import *


print("create table with dates")

print("\tp2p")
print("\t\tdropping p2p with date table")
q = "drop table if exists production.analyticsp2p_with_date"
redshift_query_write(q, schema='production')

print("\t\trecreating p2p with date table")
q = '''select
            ab.date, ab.form, ap.org, ap.analytics_base, ap.reg_count, ap.sub_reg_count, ap.teams_count,
            ap.reg_volume, ap.don_volume, ap.don_count, ap.class_count, ap.cat_count::int, ap.promo_count::int,
            ap.rest_count::int, ap.amt_count::int, ap.ded_count::int, ap.fields::int, ap.opt_fields::int,
            ap.req_fields::int, ap.allows_reg_ind::int, ap.allows_teams::int, ap.allows_reg_team_create::int,
            ap.allows_reg_team_join::int, ap.allows_opt_reg_donation::int, ap.allows_sub_reg::int,
            ap.allows_sub_reg_pfp::int, ap.allows_other_don_amt::int, ap.allows_pfp_off_don::int,
            ap.allows_tfp_off_don::int, ap.allows_soc_post_pfp_tcp::int, ap.share_home::int,
            ap.share_pfp::int, ap.share_tfp::int, ap.share_therm::int, ap.share_donation::int, ap.allows_social::int,
            ap.social_templt_count::int, ap.social_auto::int, ap.pcnt_posts::int, ap.mon_posts::int,
            ap.count_posts::int, ap.date_posts::int, ap.email_templt_count::int, ap.sponsors_count::int,
            ap.inappr_content::int
        into production.analyticsp2p_with_date
        from production.analytics as ab join production.analyticsp2p as ap on ab.id_hash=ap.id_hash'''
redshift_query_write(q, schema='production')


print("\tqgiv")
print("\t\tdropping qgiv with date table")
q = "drop table if exists production.analyticsqgiv_with_date"
redshift_query_write(q, schema='production')

print("\t\trecreating qgiv with date table")
q = '''select
            ab.date, ab.form, aq.org, aq.analytics_base, aq.pledges_count, aq.events_count, aq.events_priv_count, 
            aq.restrictions, aq.amounts, aq.ded_types, aq.opt_ded_flds, aq.req_ded_flds, aq.opt_fields, aq.req_fields, 
            aq.enable_pledge::int as pledge_active, aq.enable_donation::int as donation_active, 
            aq.multirestriction_system::int, aq.min_amount, aq.max_amount, aq.permit_anonymous::int,
            aq.enable_recurring::int as permit_recurring, aq.permit_other_amount::int, aq.permit_create_own_pledge::int, 
            aq.collect_company::int, aq.collect_phone::int, aq.collect_optin::int, aq.collect_captcha::int, 
            aq.collect_address_mobile::int, aq.enable_donorlogins::int, aq.enable_sms::int, aq.new_rec_volume, 
            aq.new_rec_count, aq.reg_count, aq.dl_trans_volume, aq.dl_trans_count, aq.dl_new_rec_count, 
            aq.dl_new_rec_volume, aq.cta_after, aq.cta_before,
            aq.conditional_fields, aq.appearance, aq.image_size
        into production.analyticsqgiv_with_date
        from production.analytics as ab join production.analyticsqgiv as aq on ab.id_hash=aq.id_hash'''
redshift_query_write(q, schema='production')


print("create weekly aggregates")

print("\tp2p")
print("\t\tdropping p2p weekly table")
q = "drop table if exists public.analyticsp2p_weekly"
redshift_query_write(q, schema='production')

print("\t\trecreating p2p weekly table")
q = '''select
            date_trunc('week', date) as date, form, org,
            sum(reg_count) as reg_count,
            sum(sub_reg_count) as sub_reg_count,
            sum(teams_count) as teams_count,
            sum(reg_volume) as reg_volume,
            sum(don_volume) as don_volume,
            sum(don_count) as don_count,
            avg(class_count) as class_count,
            avg(cat_count::int) as cat_count,
            avg(promo_count::int) as promo_count,
            avg(rest_count::int) as rest_count,
            avg(amt_count::int) as amt_count,
            avg(ded_count::int) as ded_count,
            avg(fields::int) as fields,
            avg(opt_fields::int) as opt_fields,
            avg(req_fields::int) as req_fields,
            avg(allows_reg_ind::int) as allows_reg_ind,
            avg(allows_teams::int) as allows_teams,
            avg(allows_reg_team_create::int) as allows_reg_team_create,
            avg(allows_reg_team_join::int) as allows_reg_team_join,
            avg(allows_opt_reg_donation::int) as allows_opt_reg_donation,
            avg(allows_sub_reg::int) as allows_sub_reg,
            avg(allows_sub_reg_pfp::int) as allows_sub_reg_pfp,
            avg(allows_other_don_amt::int) as allows_other_don_amt,
            avg(allows_pfp_off_don::int) as allows_pfp_off_don,
            avg(allows_tfp_off_don::int) as allows_tfp_off_don,
            avg(allows_soc_post_pfp_tcp::int) as allows_soc_post_pfp_tcp,
            avg(share_home::int) as share_home,
            avg(share_pfp::int) as share_pfp,
            avg(share_tfp::int) as share_tfp,
            avg(share_therm::int) as share_therm,
            avg(share_donation::int) as share_donation,
            avg(allows_social::int) as allows_social,
            avg(social_templt_count::int) as social_templt_count,
            avg(social_auto::int) as social_auto,
            avg(pcnt_posts::int) as pcnt_posts,
            avg(mon_posts::int) as mon_posts,
            avg(count_posts::int) as count_posts,
            avg(date_posts::int) as date_posts,
            avg(email_templt_count::int) as email_templt_count,
            avg(sponsors_count::int) as sponsors_count,
            avg(inappr_content::int) as inappr_content
        into public.analyticsp2p_weekly
        from production.analyticsp2p_with_date
        group by form, org, date_trunc('week', date)'''
redshift_query_write(q, schema='production')


print("\tqgiv")
print("\t\tdropping qgiv weekly table")
q = "drop table if exists public.analyticsqgiv_weekly"
redshift_query_write(q, schema='production')

print("\t\trecreating qgiv weekly table")
q = '''select
            date_trunc('week', date) as date, form, org,
            avg(pledges_count) as pledges_count,
            avg(events_count) as events_count,
            avg(events_priv_count) as events_priv_count,
            avg(restrictions) as restrictions,
            avg(amounts) as amounts,
            avg(ded_types) as ded_types,
            avg(opt_ded_flds) as opt_ded_flds,
            avg(req_ded_flds) as req_ded_flds,
            avg(opt_fields) as opt_fields,
            avg(req_fields) as req_fields,
            avg(pledge_active::int) as pledge_active,
            avg(donation_active::int) as donation_active,
            avg(multirestriction_system::int) as multirestriction_system,
            avg(min_amount) as min_amount,
            avg(max_amount) as max_amount,
            avg(permit_anonymous::int) as permit_anonymous,
            avg(permit_recurring::int) as permit_recurring,
            avg(permit_other_amount::int) as permit_other_amount,
            avg(permit_create_own_pledge::int) as permit_create_own_pledge,
            avg(collect_company::int) as collect_company,
            avg(collect_phone::int) as collect_phone,
            avg(collect_optin::int) as collect_optin,
            avg(collect_captcha::int) as collect_captcha,
            avg(collect_address_mobile::int) as collect_address_mobile,
            avg(enable_donorlogins::int) as enable_donorlogins,
            avg(enable_sms::int) as enable_sms,
            sum(new_rec_volume) as new_rec_volume,
            sum(new_rec_count) as new_rec_count,
            sum(reg_count) as reg_count,
            sum(dl_trans_volume) as dl_trans_volume,
            sum(dl_trans_count) as dl_trans_count,
            sum(dl_new_rec_count) as dl_new_rec_count,
            sum(dl_new_rec_volume) as dl_new_rec_volume,
            avg(cta_after) as cta_after,
            avg(cta_before) as cta_before,
            avg(conditional_fields) as conditional_fields,
            avg(appearance) as appearance,
            avg(image_size) as image_size
        into public.analyticsqgiv_weekly
        from production.analyticsqgiv_with_date
        group by form, org, date_trunc('week', date)'''
redshift_query_write(q, schema='public')


print("create monthly aggregates")

print("\tp2p")
print("\t\tdropping p2p monthly table")
q = "drop table if exists public.analyticsp2p_monthly"
redshift_query_write(q, schema='production')

print("\t\trecreating p2p monthly table")
q = '''select
            date_trunc('month', date) as date, form, org,
            sum(reg_count) as reg_count,
            sum(sub_reg_count) as sub_reg_count,
            sum(teams_count) as teams_count,
            sum(reg_volume) as reg_volume,
            sum(don_volume) as don_volume,
            sum(don_count) as don_count,
            avg(class_count) as class_count,
            avg(cat_count::int) as cat_count,
            avg(promo_count::int) as promo_count,
            avg(rest_count::int) as rest_count,
            avg(amt_count::int) as amt_count,
            avg(ded_count::int) as ded_count,
            avg(fields::int) as fields,
            avg(opt_fields::int) as opt_fields,
            avg(req_fields::int) as req_fields,
            avg(allows_reg_ind::int) as allows_reg_ind,
            avg(allows_teams::int) as allows_teams,
            avg(allows_reg_team_create::int) as allows_reg_team_create,
            avg(allows_reg_team_join::int) as allows_reg_team_join,
            avg(allows_opt_reg_donation::int) as allows_opt_reg_donation,
            avg(allows_sub_reg::int) as allows_sub_reg,
            avg(allows_sub_reg_pfp::int) as allows_sub_reg_pfp,
            avg(allows_other_don_amt::int) as allows_other_don_amt,
            avg(allows_pfp_off_don::int) as allows_pfp_off_don,
            avg(allows_tfp_off_don::int) as allows_tfp_off_don,
            avg(allows_soc_post_pfp_tcp::int) as allows_soc_post_pfp_tcp,
            avg(share_home::int) as share_home,
            avg(share_pfp::int) as share_pfp,
            avg(share_tfp::int) as share_tfp,
            avg(share_therm::int) as share_therm,
            avg(share_donation::int) as share_donation,
            avg(allows_social::int) as allows_social,
            avg(social_templt_count::int) as social_templt_count,
            avg(social_auto::int) as social_auto,
            avg(pcnt_posts::int) as pcnt_posts,
            avg(mon_posts::int) as mon_posts,
            avg(count_posts::int) as count_posts,
            avg(date_posts::int) as date_posts,
            avg(email_templt_count::int) as email_templt_count,
            avg(sponsors_count::int) as sponsors_count,
            avg(inappr_content::int) as inappr_content
        into public.analyticsp2p_monthly
        from production.analyticsp2p_with_date
        group by form, org, date_trunc('month', date)'''
redshift_query_write(q, schema='production')


print("\tqgiv")
print("\t\tdropping qgiv monthly table")
q = "drop table if exists public.analyticsqgiv_monthly"
redshift_query_write(q, schema='public')

print("\t\trecreating qgiv monthly table")
q = '''select
            date_trunc('month', date) as date, form, org,
            avg(pledges_count) as pledges_count,
            avg(events_count) as events_count,
            avg(events_priv_count) as events_priv_count,
            avg(restrictions) as restrictions,
            avg(amounts) as amounts,
            avg(ded_types) as ded_types,
            avg(opt_ded_flds) as opt_ded_flds,
            avg(req_ded_flds) as req_ded_flds,
            avg(opt_fields) as opt_fields,
            avg(req_fields) as req_fields,
            avg(pledge_active::int) as pledge_active,
            avg(donation_active::int) as donation_active,
            avg(multirestriction_system::int) as multirestriction_system,
            avg(min_amount) as min_amount,
            avg(max_amount) as max_amount,
            avg(permit_anonymous::int) as permit_anonymous,
            avg(permit_recurring::int) as permit_recurring,
            avg(permit_other_amount::int) as permit_other_amount,
            avg(permit_create_own_pledge::int) as permit_create_own_pledge,
            avg(collect_company::int) as collect_company,
            avg(collect_phone::int) as collect_phone,
            avg(collect_optin::int) as collect_optin,
            avg(collect_captcha::int) as collect_captcha,
            avg(collect_address_mobile::int) as collect_address_mobile,
            avg(enable_donorlogins::int) as enable_donorlogins,
            avg(enable_sms::int) as enable_sms,
            sum(new_rec_volume) as new_rec_volume,
            sum(new_rec_count) as new_rec_count,
            sum(reg_count) as reg_count,
            sum(dl_trans_volume) as dl_trans_volume,
            sum(dl_trans_count) as dl_trans_count,
            sum(dl_new_rec_count) as dl_new_rec_count,
            sum(dl_new_rec_volume) as dl_new_rec_volume,
            avg(cta_after) as cta_after,
            avg(cta_before) as cta_before,
            avg(conditional_fields) as conditional_fields,
            avg(appearance) as appearance,
            avg(image_size) as image_size
        into public.analyticsqgiv_monthly
        from production.analyticsqgiv_with_date
        group by form, org, date_trunc('month', date)'''
redshift_query_write(q, schema='public')


print("clean up")

print("\t\tdropping qgiv with date table")
q = "drop table if exists production.analyticsqgiv_with_date"
redshift_query_write(q, schema='public')

print("\t\tdropping p2p with date table")
q = "drop table if exists production.analyticsp2p_with_date"
redshift_query_write(q, schema='public')