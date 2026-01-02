<?php
require_once("../control/dashboard_chart_new.php");


function org_comparison($request, $params) {
    /*
    Available request->GET parameters:
        range (string): date range, [start date]::[end date]
        selectedOrgs (array): list of specific orgs by ID, ints
        formTypes (array): qgiv, p2p, auction, givi
        pricingPackages (array): pricing packages (Fees.type)
        pricingTiers (array): pricing tiers (Organization.tier)
        features (array): categories, classifications, recurring, pledges, events, sms, kiosk, vt, donorlogins, integrations
        tags (array): religious, environmental, political, top 20
    
    Presently querying as an AND operation (line 148)
    */
    
    // process parameters to build query where statement and params array
    $shouldGetData = isset($request->get['shouldGetData']) ? $request->get['shouldGetData'] : false;

    $where = array();
    // handle date params
    $range_arr = array_key_exists('range', $request->get) ? explode('::', $request->get['range']) : array();
	if (count($range_arr) > 0) {
		if ($range_arr[0]) {
            $from_date = date("Y-m-d", strtotime($range_arr[0]));
            $where["t.date>=?"] = $from_date;
		}
		if ($range_arr[1]) {
            $to_date = date("Y-m-d", strtotime($range_arr[1]));
            $where["t.date<=?"] = $to_date;
		}
    }
    
    // handle specific orgs
    $selectedOrgs = array_key_exists('selectedOrgs', $request->get) ? $request->get['selectedOrgs'] : false;
    $selectedOrgs_forms = array();
    if ($selectedOrgs) {
        foreach ($selectedOrgs as $org) {
            $selectedOrgs_forms = array_merge($selectedOrgs_forms, dbFetchColumn("select id from Form where org in (".implode(",", intval($org)).")"));
        }
    }

    // handle form type
    $formTypes = array_key_exists('formTypes', $request->get) ? $request->get['formTypes'] : false;
    $formTypes_forms = array();
    if ($formTypes) {
        foreach ($formTypes as $type) {
            $formTypes_forms = array_merge($formType_forms, dbFetchColumn("select id from Form where type in (".implode(",", intval($type)).")"));
        }
    }

    // handle pricing tiers
    $pricingTier = array_key_exists('pricingTiers', $request->get) ? $request->get['pricingTiers'] : false;
    $pricingTier_forms = array();
    if ($pricingTier) {
        foreach ($pricingTier as $tier) {
            $pricingTier_forms = array_merge(dbFetchColumn("select f.id from Form as f left join Organization as o on f.org = o.id where o.tier = ?", array(intval($tier))), $pricingTier_forms);
        }
    }

    // handle pricing packages
    $pricingPackages = array_key_exists('pricingPackages', $request->get) ? $request->get['pricingPackages'] : false;
    $pricingPackages_forms = array();
    if ($pricingPackages) {
        $supported_packages = array("Mobile Package", "Auction Package", "Everything", "Data Package", "Peer-to-Peer Package");
        $q = "select
                f.id
            from Form as f
                left join Organization as o on f.org=o.id
                left join Fees as fee on o.id=fee.org
            where
                fee.active='y' and
                fee.type=?";
        foreach ($pricingPackages as $package) {
            if (in_array($package, $supported_packages)) {
                $pricingPackages_forms = array_merge(dbFetchColumn($q, array($package)), $pricingPackage_forms);
            }
        }
    }

    // handle features used
    $features = array_key_exists("features", $request->get) ? $request->get['features'] : false;
    $features_forms = array();
    if ($features) {
        if (in_array("categories", $features)) {
            $forms_categories = dfFetchColumn("select unique form from hn_Categories where status=?", array(Status::ACTIVE));
        }
        if (in_array("classifications", $features)) {
            $forms_classifications = dfFetchColumn("select unique form from hn_Classifications where status=?", array(Status::ACTIVE));
        }
        if (in_array("recurring", $features)) {
            $forms_recurring = dbFetchColumn("select id from Form where enableRecur='y'");
        }
        if (in_array("pledges", $features)) {
            $forms_pledges = dbFetchColumn("select id from Form where pledgeActive=1");
        }
        if (in_array("events", $features)) {
            // having had an event dated within the past 12 months?
            $q = "select
                    distinct e.form
                from Event as e
                where
                    e.status=".Status::ACTIVE." and
                    (e.e_date_end>=date_sub(now(), interval 1 year) or e.e_date_end=0000-00-00)";
            $forms_events = dbFetchColumn($q);
        }
        if (in_array("sms", $features)) {
            $forms_sms = dbFetchColumn("select id from Form where enableSMS=1");
        }
        if (in_array("vt", $features)) {
            $q = "select distinct form from Transaction where source='vt'";
            $forms_vt = dbFetchColumn($q);
        }
        if (in_array("donorlogins", $features)) {
            $forms_dl = dbFetchColumn("select id from Form where enableDonorLogins=1");
        }
        if (in_array("integrations", $features)) {
            // @TODO integration status
            // status=ACTIVE only? 
            // there are quite a few entries that are PENDING, what does that mean?
            $q = "select
                    distinct f.id
                from Form as f
                    left join Organization as o on f.org = o.id
                    left join ServiceIntegration as si on si.entity = o.id and si.entityType=".EntityType::ORGANIZATION."
                where
                    si.status=".Status::ACTIVE;
            $forms_integrations = dbFetchColumn($q);
        }

        // handle category
        $tags = array_key_exists("tags", $request->get) ? $request->get['tags'] : false;
        $tags_clean = $tags_forms = array();
        if ($tags) {
            foreach (explode(",", $tags) as $tag) {
                $tags_clean[] = intval($tag);
            }
            $q = "select
                    distinct f.id
                from Form as f
                    left join Organization as o on f.org=o.id
                    left join TagsOrgs as t on o.id=t.org
                where t.tag in (".implode(",", $tags_clean).")";
            $tags_forms = dbFetchColumn($q);
        }

        // @TODO is this an AND operation or OR operation?
        // an AND operation on selected options
        $features_forms = array_intersect($forms_categories, $forms_classifications, $forms_recurring, $forms_pledges, $forms_events, $forms_sms, $forms_vt, $forms_dl, $forms_integrations, $tags_forms);
        // an OR operation on selected options
        // $features_forms = array_unique(array_merge($forms_recurring, $forms_pledges, $forms_events, $forms_sms, $forms_vt, $forms_dl, $forms_integrations));
    }

    $where["t.form in (".implode(',', array_intersect($features_forms, $selectedOrgs_forms, $formTypes_forms, $pricingPackage_forms)).")"] = null;

    // get org stats with filters
    $stats = getFormComparisonDataStructure($where, $shouldGetData, true, true);

    $org_ids = dbFetchColumn("select distinct org from Form where id in (".implode(',', $features_forms).")");
    $stats['results'] = array(
        'total_orgs' => count($org_ids),
        'total_forms' => count($features_forms),
        'avg_forms_per_org' => round(count($features_forms) / count($org_ids), 1),
        'avg_org_age' => round(dbFetchCell("select avg(datediff(now(), dateLive)) from Organization where id in (".implode(',', $org_ids).")") / 365, 1),
        'avg_form_age' => round(dbFetchCell("select avg(datediff(now(), dateLive)) from Form where id in (".implode(",", $features_forms).")") / 365, 1)
    );

    return $stats;
}