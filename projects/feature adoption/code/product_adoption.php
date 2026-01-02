<?php

require_once($_SERVER['DOCUMENT_ROOT'] . '/admin/config.php');

if (!array_key_exists('key', $_POST) || $_POST['key'] != 'DSQR59VwyFhw21PKDF4K') die();

/*
Implementation/Adoption

we want to see if the client has engaged with the features. check form settings to see if settings have been changed/configured/enabled, etc.
*/
// global
$forms_with_notifications = dbFetchCell("select systemId as form, count(id) from Notification where systemType=4 group by systemId");
$orgs_with_notifications = dbFetchColumn("select systemId as form, count(id) from Notification where systemType=4 group by systemId");  // custom notifications
$service_integrations = dbFetchRows("select entity as org, count(id) from ServiceIntegration where entityType=3 group by entity");  // integrations
$custom_reports = dbFetchRows("select entity as org, count(id) from Report where entityType=3 group by entity");  // custom reports
// 4. admin accounts
$merchant_accounts = dbFetchRows("select form, paymentMethods, count(id) from Form_MerchantAccount group by paymentMethods, form"); // payment gateways
$embeds = dbFetchRows("select entity as org, count(id) from Embed where entityType=3 group by entity");  // embed
$promises = dbFetchRows("select form, count(id) from TransPromise group by form");  // promise

// check year round settings
$restrictions = dbFetchRows("select form, count(id) from Restriction group by form");  // restrictions
$custom_fields = dbFetchRows("select form, count(id) from Fields group by form");  // custom fields
$pledges = dbFetchRows("select form, count(id) from Pledge group by form");  // pledges
$recurring = dbFetchRows("select org, count(id) from Form where enableRecur='y' group by org");  // recurring
$events = dbFetchRows("select form, count(id) from Event group by form");  // events
$events_donations = dbFetchRows("select form, count(id) from Event where allowDonation=1 group by form");  // event donations
$events_fields = dbFetchRows("select e.form, count(p.id) from PartInfo as p left join Event as e on p.event=e.id group by e.form");  // event fields
$events_promo = dbFetchRows("select entity as event, count(id) from hn_PromoCode where entityType=14 group by entity");  // event promo
$sms = dbFetchRows("select form, count(id) from SMSShortcodes group by form");  // sms/text to give
$donor_logins = dbFetchRows("select org, count(id) from Form where enableDonorLogins=1 group by org");  // donor logins
// 11. donor login onetime
// 12. donor login recurring
// 13. donor login stored payment methods
$thermometers = dbFetchRows("select form, count(id) from Thermometers group by form");  // thermometers

// check p2p
$classifications = dbFetchRows("select form, count(id) from hn_Classification group by form");  // classification
$categories = dbFetchRows("select form, count(id) from hn_Category group by form");  // categories
// 3. custom fields
$registrations = dbFetchRows("select form, id from hn_EventSettings where displayRegStore=1");  // store in registration  @TODO not sure about this one, only 2 results
$product_fields = dbFetchRows("select form, count(id) from Products group by form");  // store product fields
$shipping_address = dbFetchRows("select form, count(id) from ProductShippingMethods group by form");  // shipping address
$nonfundraising_participants = dbFetchRows("select f.org as org, count(es.form) from hn_EventSettings as es left join Form as f on es.form=f.id where es.enableNonFundraising=1 group by f.org");  // nonfundraising participants
// 8. subregistrations
$teams = dbFetchRows("select f.org as org, count(es.form) from hn_EventSettings as es left join Form as f on es.form=f.id where es.enableTeams=1 group by f.org");  // teams
// 10. recurring
// 11. restrictions
$aggregator_page = dbFetchRows("select f.org as org, count(f.id) from AggregatorSettings as agg left join Form as f on agg.form=f.id group by f.org");  // aggregator page
$category_fields = dbFetchRows("select form, count(f.id) from CategoryFields as f left join hn_Category as c on f.category=c.id group by c.form");  // category fields

$implementation_data = array(
    'forms_with_notifications' => $forms_with_notifications,
    'orgs_with_notifications' => $orgs_with_notifications,
    'service_integrations' => $service_integrations,
    'custom_reports' => $custom_reports,
    'merchant_accounts' => $merchant_accounts,
    'embeds' => $embeds,
    'promises' => $promises,
    'restrictions' => $restrictions,
    'custom_fields' => $custom_fields,
    'pledges' => $pledges,
    'recurring' => $recurring,
    'events' => $events,
    'events_donations' => $events_donations,
    'events_fields' => $events_fields,
    'events_promo' => $events_promo,
    'sms' => $sms,
    'donor_logins' => $donor_logins,
    'thermometers' => $thermometers,
    'classifications' => $classifications,
    'categories' => $categories,
    'registrations' => $registrations,
    'product_fields' => $product_fields,
    'shipping_address' => $shipping_address,
    'nonfundraising_participants' => $nonfundraising_participants,
    'teams' => $teams,
    'aggregator_page' => $landing_page,
    'category_fields' => $category_fields
);

/*
Bidirectional Adoption

we want to see if the donors have engaged with the features. check presence in transactions.
*/
// global / source transactions
// $transactions_by_source = dbFetchRows("select form, source, count(id) from Transaction group by source, form");
$giftassist_transactions = dbFetchRows("select t.form, count(distinct ga.id) from TransGiftAssist as ga left join Transaction as t on t.id=ga.transaction group by t.form");  // gift assist

// check year round settings
$restrictions = dbFetchRows("select t.form, count(distinct t.id) from Transaction as t left join TransDonation as td on td.transaction=t.id where td.restriction != '' group by t.form");  // restrictions
$fielddata = dbFetchRows("select t.form, count(distinct fld.id) from FieldData as fld left join Transaction as t on fld.transaction=t.id where fld.transEvent=0 and fld.transRegistration=0 group by t.form");  // fielddata
$pledge = dbFetchRows("select t.form, count(distinct td.pledge) from TransDonation as td left join Transaction as t on t.id=td.transaction where td.pledge!=0 group by t.form");  // pledge
$recurring = dbFetchRows("select form, count(id) from Transaction where recurring!=0 group by form");  // recurring
$events = dbFetchRows("select t.form, count(distinct te.transaction) from TransEvent as te left join Transaction as t on te.transaction=t.id group by t.form");  // events
$events_donatiosn = dbFetchRows("select t.form, count(distinct td.id) from TransDonation as td left join Transaction as t on td.transaction=t.id left join TransEvent as te on te.transaction=t.id group by t.form");  // event donation
$events_fielddata = dbFetchRows("select form, count(distinct pd.id) from PartData as pd left join TicketHolder as th on pd.tick_holder=th.id left join TransEvent as te on th.transEvent=te.id left join Transaction as t on te.transaction=t.id group by t.form");  // event fielddata
$event_promo = dbFetchRows("select form, count(distinct p.id) from TransPromo as p left join TransEvent as te on te.id=p.entity left join Transaction as t on t.id=te.transaction where p.entityType=10 group by t.form");  // event promo
// 9. sms/text transactions # in source
// 10. donor logins # one time + recurring
$dl_onetime = dbFetchRows("select t.form, count(distinct et.id) from EntityTransactions as et left join Transaction as t on et.transaction=t.id where et.entityType=1 and t.recurring=0 group by t.form");  // 11. donor logins onetime
$dl_recurring = dbFetchRows("select t.form, count(distinct et.id) from EntityTransactions as et left join Transaction as t on et.transaction=t.id where et.entityType=1 and t.recurring!=0 group by t.form");  // 12. donor logins recurring
// 13. donor logins stored payment methods

// check p2p
$classifications = dbFetchRows("select form, count(id) from TransRegistration where classification<>0 group by form"); // 1. classification
$categories = dbFetchRows("select form, count(id) from TransRegistration where category!=0 group by form"); // 2. categories
// 3. custom fields
$purchases = dbFetchRows("select form, count(id) from TransPurchase group by form"); // 4. store in registration
// 5. store product fields
$purchases_shipping = dbFetchRows("select form, count(id) from TransPurchase where shippingMethod is not null group by form"); // 6. shipping address
$registrations_nonfundraising = dbFetchRows("select form, count(id) from TransRegistration where activityRole=2 group by form"); // 7. nonfundraising participants
$registrations_subregistrants = dbFetchRows("select form, count(id) from TransRegistration where parentRegistration is not null group by form"); // 8. subregistrations
$teams = dbFetchRows("select form, count(id) from hn_Team group by form"); // 9. teams
// 10. recurring # already in year round
// 11. restrictions # already covered in year round
// 12. aggregator page # in source
// 13. category fields

$bidirectional_adoption_data = array(
    // 'transactions_by_source' => $transactions_by_source,
    'giftassist_transactions' => $giftassist_transactions,
    'restrictions' => $restrictions,
    'fielddata' => $fielddata,
    'pledge' => $pledge,
    'recurring' => $recurring,
    'events' => $events,
    'events_donatiosn' => $events_donatiosn,
    'events_fielddata' => $events_fielddata,
    'event_promo' => $event_promo,
    'dl_transactions' => $dl_onetime + $dl_recurring,
    'dl_onetime' => $dl_onetime,
    'dl_recurring' => $dl_recurring,
    'classifications' => $classifications,
    'categories' => $categories,
    'purchases' => $purchases,
    'purchases_shipping' => $purchases_shipping,
    'registrations_nonfundraising' => $registrations_nonfundraising,
    'registrations_subregistrants' => $registrations_subregistrants,
    'teams' => $teams
);

$data = array(
    'implementation_data' = $implementation_data,
    'bidirectional_adoption_data' => $bidirectional_adoption_data
);

die(json_encode(array($data)));

?>