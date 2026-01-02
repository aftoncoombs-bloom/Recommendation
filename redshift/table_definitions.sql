drop table transactions;
create table transactions (
  id int not null distkey sortkey,
  org int not null,
  form int not null,
  status char(2) not null,
  amount float not null default 0.0,
  donations_amt float not null default 0.0,
  purchases_amt float not null default 0.0,
  events_amt float not null default 0.0,
  registrations_amt float not null default 0.0,
  events_tickets int not null default 0,
  purchases_quantity int not null default 0,
  donations_count int not null default 0,
  events_count int not null default 0,
  purchases_count int not null default 0,
  registrations_count int not null default 0,
  fields int not null default 0,
  event_fieds int not null default 0,
  recurring  int not null default 0,
  payment_type varchar(6) null,
  creatingtransactionfor int not null default 0,
  transdonationentity int not null default 0,
  transdonationentitytype int not null default 0,
  source varchar(12) null,
  source_id int not null default 0,
  date timestamp,
  hour int not null default 0,
  day int not null default 0,
  month int not null default 0,
  year int not null default 0,
  zip varchar(12) null,
  state varchar(4) null,
  email varchar(64) null,
  matchinggifts_count int not null default 0,
  smspledge_count int not null default 0,
  smspledge_amt float not null default 0.0,
  auctionpurchase_count int not null default 0,
  auctiondonation_count int not null default 0,
  is_fraud boolean,
  form_amount_mean_diff float null,
  form_day_mean_diff float null,
  form_hour_mean_diff float null
);

alter table transactions add column gift_assist_count int not null default 0;
alter table transactions add column gift_assist_amt float not null default 0.0;
alter table transactions add column qgiv_fee float not null default 0.0;
alter table transactions drop column form_amount_mean_diff;
alter table transactions drop column form_day_mean_diff;
alter table transactions drop column  form_hour_mean_diff;
alter table transactions add column platform varchar(10) null default '';
alter table transactions add column isexpresscheckout boolean default 'False';

update transactions set platform='iPhone' where useragent LIKE '%iPhone%';
update transactions set platform='iPad' where useragent LIKE '%iPad%';
update transactions set platform='Android' where useragent LIKE '%Android%';
update transactions set platform='Mac' where useragent LIKE '%IntelMacOSX%';
update transactions set platform='Windows' where useragent LIKE '%Windows%';


create table Analytics (
  id int not null distkey sortkey,
  date timestamp,
  org int not null,
  form int not null,
  sic int null,
  ein int null,
  vt_trans_count int not null default 0,
  don_form_trans_count int not null default 0,
  kiosk_trans_count int not null default 0,
  p2p_trans_count int not null default 0,
  mobile_trans_count int not null default 0,
  mobilevt_trans_count int not null default 0,
  sms_trans_count int not null default 0,
  fb_trans_count int not null default 0,
  vt_trans_vol float not null default 0.0,
  don_form_trans_vol float not null default 0.0,
  kiosk_trans_vol float not null default 0.0,
  p2p_trans_vol float not null default 0.0,
  mobile_trans_vol float not null default 0.0,
  mobilevt_trans_vol float not null default 0.0,
  sms_trans_vol float not null default 0.0,
  fb_trans_vol float not null default 0.0,
  one_time_trans_vol float not null default 0.0,
  one_time_trans_count int not null default 0,
  rec_trans_vol float not null default 0.0,
  rec_trans_count int not null default 0,
  product smallint null
);

create table AnalyticsQgiv (
  id int not null distkey sortkey,
  org int not null,
  analytics_base int not null,
  pledges_count int not null default 0,
  events_count int not null default 0,
  events_priv_count int not null default 0,
  restrictions int not null default 0,
  amounts int not null default 0,
  ded_types int not null default 0,
  opt_ded_flds int not null default 0,
  req_ded_flds int not null default 0,
  opt_fields int not null default 0,
  req_fields int not null default 0,
  pledge_active boolean,
  donation_active boolean,
  multirestriction_system boolean,
  min_amount float null,
  max_amount float null,
  show_amount smallint,
  permit_anonymous boolean,
  permit_recurring boolean,
  permit_other_amount boolean,
  permit_create_own_pledge boolean,
  collect_company boolean,
  collect_phone boolean,
  collect_optin smallint,
  collect_captcha boolean,
  collect_address_mobile smallint,
  enable_donorlogins boolean,
  enable_sms boolean,
  default_recurring_frequency char(2) null,
  event_stats int null,
  new_rec_volume float not null default 0.0,
  new_rec_count int not null default 0,
  reg_count int not null default 0,
  dl_trans_volume float not null default 0.0,
  dl_trans_count int not null default 0,
  dl_new_rec_count int not null default 0,
  dl_new_rec_volume float not null default 0.0,
  id_hash varchar null,
  appearance smallint not null default 0,
  cta_before smallint not null default 0,
  cta_after smallint not null default 0,
  image_size smallint not null default 0,
  conditional_fields int not null default 0
);
alter table analyticsqgiv add column appearance smallint not null default 0;
alter table analyticsqgiv add column cta_before smallint not null default 0;
alter table analyticsqgiv add column cta_after smallint not null default 0;
alter table analyticsqgiv add column image_size smallint not null default 0;
alter table analyticsqgiv add column conditional_fields int not null default 0;

alter table analyticsqgiv add column goals_count int not null default 0;
alter table analyticsqgiv add column permit_matching boolean;
alter table analyticsqgiv add column permit_gift_assist boolean;
alter table analyticsqgiv add column date timestamp null default null;


create table AnalyticsP2P (
  id int not null distkey sortkey,
  org int not null,
  analytics_base int not null,
  reg_count int not null default 0,
  sub_reg_count int not null default 0,
  teams_count int not null default 0,
  reg_volume float not null default 0.0,
  don_volume float not null default 0.0,
  don_count int not null default 0,
  class_count int not null default 0,
  cat_count int not null default 0,
  promo_count int not null default 0,
  rest_count int not null default 0,
  amt_count int not null default 0,
  ded_count int not null default 0,
  fields int not null default 0,
  opt_fields int not null default 0,
  req_fields int not null default 0,
  allows_reg_ind smallint,
  allows_teams smallint,
  allows_reg_team_create boolean,
  allows_reg_team_join boolean,
  allows_opt_reg_donation smallint,
  allows_sub_reg boolean,
  allows_sub_reg_pfp boolean,
  allows_other_don_amt smallint,
  allows_pfp_off_don boolean,
  allows_tfp_off_don boolean,
  allows_soc_post_pfp_tcp boolean,
  share_home boolean,
  share_pfp boolean,
  share_tfp boolean,
  share_therm boolean,
  share_donation boolean,
  allows_social boolean,
  social_templt_count int not null default 0,
  social_auto smallint,
  pcnt_posts float null,
  mon_posts int not null default 0,
  count_posts int not null default 0,
  date_posts int not null default 0,
  email_templt_count int not null default 0,
  sponsors_count int not null default 0,
  inappr_content int not null default 0
);
alter table analyticsp2p add column allows_recurring boolean;
alter table analyticsp2p add column allows_matching boolean;
alter table analyticsp2p add column allows_gift_assist boolean;
alter table analyticsp2p add column campaign_count int not null default 0;
alter table analyticsp2p add column badges_count int not null default 0;
alter table analyticsp2p add column display_reg_store boolean;
alter table analyticsp2p add column products_count int not null default 0;
alter table analyticsp2p add column rec_count int not null default 0;
alter table analyticsp2p add column rec_volume float not null default 0.0;
alter table analyticsp2p add column date timestamp null default null;

create table analyticsauction (
    id int not null,
    org int not null,
    days_to_cutoff_donation float not null default 0.0,
    days_to_cutoff_registration float not null default 0.0,
    days_to_startdate float not null default 0.0,
    days_to_enddate float not null default 0.0,
    packages int not null default 0,
    promo_codes int not null default 0,
    fields int not null default 0,
    restrictions int not null default 0,
    dedications int not null default 0,
    donations_amounts int not null default 0,
    sponsors int not null default 0,
    categories int not null default 0,
    items_auction int not null default 0,
    items_fundaneed int not null default 0,
    items_store int not null default 0,
    items_tags int not null default 0,
    allows_giftassist boolean,
    allows_matchinggifts boolean,
    trans_count int not null default 0,
    trans_volume float not null default 0.0,
    bids int not null default 0,
    items_bid_on int not null default 0,
    bids_vol float not null default 0.0,
    id_hash varchar null
);
alter table analyticsauction add column date timestamp null default null;

drop table if exists forms;
create table forms (
  form int not null distkey sortkey,
  org int not null,
  path varchar(64) null,
  product smallint null,
  mean_transaction_amount float null,
  mean_transaction_daily_count float null,
  mean_transaction_hour int null,
  mean_transaction_day int null,
  mean_page_views float null,
  mean_conversion float null
);
alter table formtemplate add column enableEndDate bool null default null;
alter table formtemplate add column enableStartDate bool null default null;
alter table formtemplate add column recurringPlanEndDateRequired bool null default null;

create table Organizations (
  id int not null distkey sortkey,
  org_name varchar(128) null,
  tax_id varchar(24) null,
  city varchar(36) null,
  state varchar(5) null,
  zip varchar(12) null,
  country varchar(6) null,
  live_date timestamp null,
  signup_step_one timestamp null,
  first_transaction_date timestamp null,
  status varchar(14) null,
  pricing_package varchar(16) null,
  reseller varchar(80) null,
  previously_accepted_credit_online varchar(3) null,
  segment varchar(128) null,
  tags varchar(128) null,
  date_closed timestamp null,
  reason_closed varchar(128) null,
  new_provider varchar(128) null,
  additional_churn_info varchar(512) null
);

create table Integrations (
  org int not null,
  service varchar(64) null,
  status varchar(24) null,
  frequency varchar(36) null,
  last_export_date timestamp null,
  last_export_result varchar(24) null
);

create table logs (
  id int not null distkey sortkey,
  org int not null,
  form int null,
  entity int null,
  entitytype int null,
  systemid int null,
  systemtype int null,
  type int null,
  created timestamp null,
  userid int null,
  ghost int null,
  hidden int null,
  access int null,
  ack int null,
  count int null,
  message varchar(256) null
);

create table syslog_logs (
  id int not null distkey sortkey,
  org int not null,
  form int null,
  entity int null,
  entitytype int null,
  systemid int null,
  systemtype int null,
  type int null,
  created timestamp null,
  userid int null,
  ghost int null,
  hidden int null,
  access int null,
  ack int null,
  count int null,
  message varchar(256) null
);

create table org_websites (
    org int not null,
    date datetime not null default sysdate,
    calls_to_action int not null default 0,
    iframe_source_blackbaud int not null default 0,
    iframe_source_classy int not null default 0,
    iframe_source_donordrive int not null default 0,
    iframe_source_engagingnetworks int not null default 0,
    iframe_source_facebook int not null default 0,
    iframe_source_giveeffect int not null default 0,
    iframe_source_givelively int not null default 0,
    iframe_source_instagram int not null default 0,
    iframe_source_mobilecause int not null default 0,
    iframe_source_networkforgood int not null default 0,
    iframe_source_onecause int not null default 0,
    iframe_source_paypal int not null default 0,
    iframe_source_securegive int not null default 0,
    iframe_source_qgiv int not null default 0,
    iframe_source_stripe int not null default 0,
    iframe_source_twitter int not null default 0,
    image_count int not null default 0,
    internal_links int not null default 0,
    link_target_blackbaud int not null default 0,
    link_target_classy int not null default 0,
    link_target_donordrive int not null default 0,
    link_target_engagingnetworks int not null default 0,
    link_target_securegive int not null default 0,
    link_target_facebook int not null default 0,
    link_target_giveeffect int not null default 0,
    link_target_givelively int not null default 0,
    link_target_instagram int not null default 0,
    link_target_mobilecause int not null default 0,
    link_target_networkforgood int not null default 0,
    link_target_onecause int not null default 0,
    link_target_paypal int not null default 0,
    link_target_qgiv int not null default 0,
    link_target_stripe int not null default 0,
    link_target_twitter int not null default 0,
    outbound_links int not null default 0,
    script_source_blackbaud int not null default 0,
    script_source_classy int not null default 0,
    script_source_donordrive int not null default 0,
    script_source_engagingnetworks int not null default 0,
    script_source_facebook int not null default 0,
    script_source_giveeffect int not null default 0,
    script_source_givelively int not null default 0,
    script_source_instagram int not null default 0,
    script_source_mobilecause int not null default 0,
    script_source_networkforgood int not null default 0,
    script_source_onecause int not null default 0,
    script_source_paypal int not null default 0,
    script_source_securegive int not null default 0,
    script_source_qgiv int not null default 0,
    script_source_stripe int not null default 0,
    script_source_twitter int not null default 0,
    url varchar(256) null,
    word_count int not null default 0
);
alter table org_websites add column
    iframe_source_securegive int not null default 0;
alter table org_websites add column
    link_target_securegive int not null default 0;
alter table org_websites add column
    script_source_securegive int not null default 0;

create table googleanalytics_ids (
    date datetime null,
    org int null,
    form int null,
    views int not null default 0,
    path varchar(256) not null,
    devicecategory varchar(24) not null,
    globalaccountid int null,
    transregistrationid int null
);

drop table googleanalytics_traffic_new;
create table googleanalytics_traffic_new (
    date datetime null,
    org int null,
    form int null,
    views int not null default 0,
    sessions int not null default 0,
    sessionduration float not null default 0.0,
    bounces int not null default 0,
    path varchar(256) not null,
    devicecategory varchar(24) not null,
    controlpanel boolean default false,
    qgiv_frontend boolean default false,
    p2p_frontend boolean default false
);

alter table ga4_traffic add column bouncerate float not null default 0.0;

drop table if exists googleanalytics_referrer_new;
create table googleanalytics_referrer_new (
    date datetime null,
    org int null,
    form int null,
    views int not null default 0,
    sessions int not null default 0,
    sessionduration float not null default 0.0,
    bounces int not null default 0,
    path varchar(256) null,
    source varchar(256) null,
    qgiv_frontend boolean default false,
    p2p_frontend boolean default false,
    facebook boolean default false,
    twitter boolean default false
);

drop table if exists social_shares_facebook;
create table social_shares_facebook (
    org int not null,
    form int not null,
    url varchar(256) not null,
    reaction_count int not null default 0,
    comment_count int not null default 0,
    share_count int not null default 0
);
drop table if exists social_shares_twitter;
create table social_shares_twitter (
    tweet_id varchar(256) not null,
    twitter_user_id varchar(256) not null,
    org int not null,
    form int not null,
    url varchar(256) not null,
    date_created datetime not null default sysdate,
    content varchar(256) not null,
    retweet_count int not null default 0,
    like_count int not null default 0,
    hashtags varchar(256) not null default ''
);


/*
 PRODUCTION TABLE DUPLICATES - PRODUCTION SCHEMA
 */
drop table if exists production.organization;
create table if not exists production.organization (
    id int not null,
    datecreated timestamp null,
    datelive timestamp null,
    state varchar(64) null,
    country varchar(64) null,
    status smallint not null default 0,
    website varchar(512) null,
    segment varchar(100) null,
    pricing_package varchar(200) null
);

create table if not exists embed (
    id int not null,
    entity int null,
    entitytype int null,
    widgettype smallint not null default 1,
    url varchar(512) null,
    date timestamp null default null
);
alter table embed add column widget int not null default 0;
drop table if exists form;
create table if not exists form (
    id int not null,
    org int not null,
    datecreated timestamp null,
    datelive timestamp null,
    path varchar(128) null,
    status smallint not null default 0,
    type smallint not null default 0,
    template smallint not null default 0
);
alter table form add column categorization int not null default 0;
alter table form add column isvirtual int not null default 0;
create table if not exists thermometers (
    id int not null,
    form int not null,
    status smallint not null default 0,
    fundraisinggoal float null,
    begindate timestamp null,
    enddate timestamp null,
    targetentity int null,
    targetentitytype smallint null,
    totalraised float null,
    primarygoal int null,
    date timestamp null default null
);
create table if not exists facebookfundraisers (
    id int not null,
    entity int null,
    entitytype smallint null,
    fundraiserid varchar(128) null,
    fundraiserstatus smallint null,
    date timestamp null default null
);
create table if not exists socialsettings (
    id int not null,
    form int null,
    youtubeurl varchar(512) null,
    twitterurl varchar(512) null,
    facebookurl varchar(512) null,
    instagramurl varchar(512) null,
    fbthumbnail varchar(512) null,
    fbdescription varchar(512) null,
    enablefbfundraiser smallint null,
    facebookfundraiserdescription varchar(512) null,
    date timestamp null default null
);
create table if not exists givi (
    form int not null,
    website varchar(512) null,
    facebookurl varchar(512) null,
    twitterurl varchar(512) null,
    instagramurl varchar(512) null,
    date timestamp null default null
);
create table if not exists badges (
    entity int null,
    entitytype smallint null,
    status smallint not null default 0,
    badgetype smallint null,
    targetentitytype smallint null,
    date timestamp null default null
);
alter table badges add column badge int not null default 0;
create table if not exists lists (
    id int not null,
    created timestamp null,
    creatingentity int null,
    creatingentitytype smallint null,
    listtype smallint null,
    status smallint not null default 0,
    date timestamp null default null
);
create table if not exists emailcampaign (
    entity int null,
    entitytype smallint null,
    template int null,
    mailinglist varchar(512) null,
    predicate int null,
    sent timestamp null,
    status smallint not null default 0,
    created timestamp null,
    recipients varchar(512) null,
    date timestamp null default null
);
drop table if exists smscampaign;
create table if not exists smscampaign (
    id	int not null,
    created	timestamp null,
    creatingEntity int not null,
    creatingEntityType int not null,
    listtype int not null,
    status	int not null,
    listlength int not null
);
create table if not exists reminders (
    id int not null,
    entity int null,
    entitytype smallint null,
    delayval smallint null,
    delayincrement varchar(12) null,
    status smallint not null default 0,
    weight smallint null,
    specifictime timestamp null,
    isrelative smallint null,
    remindermsg varchar(256) null,
    date timestamp null default null
);
create table if not exists smspledge (
    id int not null,
    org int null,
    form int null,
    shortcode int null,
    startdate timestamp null,
    enddate timestamp null,
    amountrequired int null,
    status smallint not null default 0,
    created timestamp null,
    listid int null,
    date timestamp null default null
);

/*
 FEATURE ADOPTION TABLES
 */
create table if not exists notifications_forms (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists notifications_orgs (
    org int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists integrations (
    org int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists reports (
    org int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists merchant_accounts (
    form int not null,
    paymentmathods varchar(4),
    count int not null default 0,
    date timestamp null default null
);
create table if not exists embeds (
    org int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists promises (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists restrictions (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists customfields (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists pledges (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists recurring (
    org int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists events (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists donations (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists eventfields (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists eventpromo (
    event int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists sms (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists donorlogins (
    org int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists thermometers (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists classifications (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists categories (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists registrationstore (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists productfields (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists shippingaddress (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
create table if not exists nonfundraisingparticipants (
    org int not null,
    countforms int not null default 0,
    date timestamp null default null
);
create table if not exists teams (
    org int not null,
    countforms int not null default 0,
    date timestamp null default null
);
create table if not exists categoryfields (
    form int not null,
    count int not null default 0,
    date timestamp null default null
);
/*
aggregator page
*/

alter table transactions add column matchinggifts_count int not null default 0;
alter table transactions add column smspledge_count int not null default 0;
alter table transactions add column smspledge_amt float not null default 0.0;
alter table transactions add column auctionpurchase_count int not null default 0;
alter table transactions add column auctiondonation_count int not null default 0;
alter table transactions add column channel int not null default 0;
alter table transactions add column recurring_origin int not null default 0;
alter table transactions add column is_new_form int not null default 0;

create table if not exists auctionbids (
    form int not null,
    date timestamp not null,
    ticketholder int null default 0,
    product int null default 0,
    source int not null default 0
);

create table if not exists transauction (
    id int not null,
    form int not null,
    transaction int not null default 0,
    bidder int not null,
    product int not null,
    checknumber int not null default 0,
    offlinetype int null,
    originalamount float not null default 0.00,
    tax float not null default 0.00,
    total float not null default 0.00,
    quantity int not null default 0,
    unitcost float not null default 0.00,
    status int not null,
    createddate timestamp not null,
    lastupdate timestamp null
);
create table if not exists transauctiondonation (
    id int not null,
    form int not null,
    transaction int not null default 0,
    bidder int not null,
    product int not null,
    status int not null,
    amount float not null default 0.00,
    entity int not null,
    entitytype int not null,
    offlinetype int not null,
    createddate timestamp not null,
    lastupdate timestamp not null
);

create table if not exists users (
    id int not null,
    org int not null,
    createddate timestamp null,
    lastlogin timestamp null,
    status int not null
);

create table if not exists auctionitem (
    id int not null,
    product int not null,
    winner int not null default 0,
    maxbid float not null default 0.0,
    reserve float not null default 0.0,
    bidincrement float not null default 0.0,
    number int not null default 0,
    value float not null default 0.0
);

create table if not exists bidders (
    ticketholder int not null,
    form int not null,
    product int not null,
    amount float not null default 0.0,
    date_created timestamp not null
);

create table if not exists form_daily_aggregates (
    form int not null,
    date timestamp not null,
    trans_onetime_count int not null default 0,
    trans_onetime_vol float not null default 0.0,
    trans_recurring_count int not null default 0,
    trans_recurring_vol float not null default 0.0,
    pageviews int not null default 0,
    bounces int not null default 0,
    is_new_template boolean default false
);

create table if not exists zendesk (
    id int not null,
    org int null default null,
    created timestamp null default null,
    updated timestamp null default null,
    type varchar(10) null default null,
    priority varchar(10) null default null,
    status varchar(10) null default null,
    requester bigint null default null,
    submitter bigint null default null,
    assignee bigint null default null,
    internal_organization_id bigint null default null,
    group_id bigint null default null,
    forum_topic int null default null,
    problem int null default null,
    has_incidents boolean default false,
    satisfaction_rating varchar(10) null default null,
    satisfaction_comment varchar(110) null default null,
    comment_count int null default null,
    subject varchar(70) null default null,
    description varchar(1000) null default null
);

create table if not exists formtemplate (
    form int not null,
    template smallint not null default 0,
    date timestamp not null default now()
);


/*
 AGGREGATE TABLES
 */
create table if not exists form_daily_traffic (
    org int not null,
    form int not null,
    date timestamp not null,
    views int not null,
    bounces int not null,
    desktop_views int not null,
    desktop_bounces int not null,
    tablet_views int not null,
    tablet_bounces int not null,
    mobile_views int not null,
    mobile_bounces int not null
);

drop table system_daily_traffic;
create table if not exists system_daily_traffic (
    date timestamp not null,
    views int not null,
    bounces int not null,
    desktop_views int not null,
    desktop_bounces int not null,
    tablet_views int not null,
    tablet_bounces int not null,
    mobile_views int not null,
    mobile_bounces int not null
);

create table if not exists form_daily (
    org int not null,
    form int not null,
    date timestamp not null,
    conversion float not null,
    conversion_onetime float not null,
    conversion_recurring float not null,
    is_embed boolean not null,
    is_new_standard_form boolean not null
);

create table if not exists system_daily (
    date timestamp not null,
    conversion float not null,
    conversion_onetime float not null,
    conversion_recurring float not null
);

create table if not exists form_daily_transactions (
    org int not null,
    form int not null,
    date timestamp not null,
    count int not null,
    volume float not null,
    count_onetime int not null,
    volume_onetime float not null,
    count_recurring int not null,
    volume_recurring float not null,
    count_recurring_origin int not null,
    volume_recurring_origin float not null
);

create table if not exists system_daily_transactions (
    date timestamp not null,
    count int not null,
    volume float not null,
    count_onetime int not null,
    volume_onetime float not null,
    count_recurring int not null,
    volume_recurring float not null,
    count_recurring_origin int not null,
    volume_recurring_origin float not null
);

create table if not exists control_panel_views (
    org int not null default 0,
    date timestamp not null,
    url varchar(240) not null default '',
    views int not null default 0,
    page_type varchar(50) not null default ''
);

create table if not exists user_logins (
    userid int not null default 0,
    date timestamp not null,
    logins int not null default 0,
    org int not null default 0
);

drop table recurring_agg;
create table if not exists recurring_agg (
    form int not null,
    org int not null,
    date timestamp not null,
    recurring int not null default 0,
    installments_mean float not null default 0.0,
    total_sum float not null default 0.0,
    total_mean float not null default 0.0,
    single_amount_sum float not null default 0.0,
    single_amount_mean float not null default 0.0,
    duration varchar(25),
    is_new_template boolean not null default False,
    is_embedded boolean not null default False,
    appearance float not null default 0.0,
    cta_before float not null default 0.0,
    cta_after float not null default 0.0,
    conditional_fields float not null default 0.0,
    multistep float not null default 0.0,
    image_size float not null default 0.0,
    views int not null default 0,
    bounces int not null default 0,
    onetime int not null default 0,
    onetime_total float not null default 0.0,
    onetime_avg float not null default 0.0,
    transactions int not null default 0,
    conversion float not null default 0.0,
    conversion_recurring float not null default 0.0,
    recurring_trans_perc float not null default 0.0,
    form_type int not null default 0,
    form_template int not null default 0,
    segment varchar(75),
    pricing_package varchar(100),
    type int not null default 0,
    template int not null default 0,
    enableenddate boolean default False,
    enablestartdate boolean default False,
    recurringplanenddaterequired boolean default False
);
drop table matomo_traffic;
create table matomo_traffic (
    id varchar(26) not null,
    ip varchar(26) null default '',
    visitorId varchar(24) null default '',
    visitDuration int not null default 0,
    actions int not null default 0,
    referrerType varchar(24) null default '',
    referrerName varchar(100) null default '',
    deviceType varchar(50) not null default '',
    deviceBrand varchar(50) not null default '',
    deviceModel varchar(100) not null default '',
    operatingSystemName varchar(50) not null default '',
    browser varchar(100) not null default '',
    url varchar(300) not null default '',
    timeSpent int not null default 0,
    pageviewPosition varchar(10) not null default '',
    timestamp timestamp not null,
    org int not null default 0,
    form int not null default 0
);

create table causeiq_data (
    id int not null,
    org int not null,
    ein varchar(9) null,
    address varchar(255) null,
    description varchar(255)
    ntee varchar(255) null,
    501_c_type varchar(255) null,
    form990_type varchar(255) null,
    year_formed varchar(255) null,
    fiscal_year_end varchar(255) null,
    most_recent_tax_period varchar(255) null,
    pub78_eligible_tax_deduction varchar(255) null,
    causeiq_url varchar(255) null,
    employees int null,
    employees_one_year_growth float null,
    revenues_total int null,
    expenses_total int null,
    assets_total int null,
    liabilities_total int null,
    one_year_growth float null,
    last_updated timestamp null
);

create table causeiq_historicaldata (
    id int not null,
    org int not null,
    ein varchar(9) null,
    type varchar(12) null,
    value int null,
    year int null
);

create table bidders (
    id int not null,
    form int not null,
    biddernumber int not null default 0,
    ticketholder int not null default 0,
    status int not null default 0,
    paymentmethod int not null default 0,
    offlinetype int not null default 0,
    isanonymous bool default False,
    lastupdate timestamp,
    incheckout bool not null default False,
    bidderstatus int not null default 0
);


create table bids (
    id int not null,
    form int not null,
    biddeer int not null default 0,
    product int not null default 0,
    amount float not null default 0.0,
    status int not null default 0,
    timestamp timestamp,
    lastupdate timestamp,
    source int not null default 0,
    parent int not null default 0,
    ismaxbid bool not null default False
);


create table message_history (
    id int not null,
    org int not null,
    date timestamp,
    entitytype int not null,
    entity int not null,
    endpoint varchar(12),
    message varchar(256),
    isinbound smallint not null,
    status smallint not null
);
select * from message_history limit 5;


create table org_retention (
    org int not null,
    retention float not null default 0.0,
    churn float not null default 0.0,
    new_donors float not null default 0.0,
    mean_value_change float not null default 0.0,
    median_value_change float not null default 0.0
);


create table if not exists production.ga4_traffic_weekly (
    week datetime null,
    org int not null default 0,
    form int not null default 0,
    views int not null default 0
);
create table if not exists production.ga4_traffic_daily (
    date datetime null,
    org int not null default 0,
    form int not null default 0,
    views int not null default 0
);
create table if not exists production.ga4_traffic_weekly_device (
    week datetime null,
    org int not null default 0,
    form int not null default 0,
    devicecategory varchar(128) null,
    views int not null default 0
);
create table if not exists production.ga4_traffic_daily_device (
    date datetime null,
    org int not null default 0,
    form int not null default 0,
    devicecategory varchar(128) null,
    views int not null default 0
);

truncate table system_daily_traffic;
select * from integrations limit 10;

/*
count transaction types/targets?

event donations, registrations, participant & team donations, etc.?
 */

select * from stl_load_errors order by starttime desc;
