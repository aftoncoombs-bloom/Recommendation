<?php
/**
 * Retrieves traffic activity and basic stats from Matomo page view stats for a given organization, query refined by optional begin and end dates. 
 * 
 * int $org Organization ID
 * date $date_begin (optional) Start date for activity query
 * date $date_end (optional) End date for activity query
 */
function get_org_analytics($org, $date_begin=false, $date_end=false) {
    // &token_auth=38fd323ceed1df7a94de0c5d2ce4b847

    $url_keywords = array();
    $requests = array();

    // collect keywords from organizations
    //  /form/[id], /event/[id], /widget/[id], /embed/[id], /form/[alias], etc.
    $form_ids = dbFetchColumn("select id, path, type from Form where org=?", array($request->get['org']));
    foreach ($form_ids as $form) {
        if ($form['type'] == ProductType::QGIV) {
            $url_keywords[] = '/for/'.$form['path'];
        } elseif ($form['type'] == ProductType::HOBNOB || $form['type'] == ProductType::AGGREGATOR) {
            $url_keywords[] = '/event/'.$form['id'];
            // look for alias
            $alias = dbFetchCell("select alias from hn_EventSettings where form=?", array($form['id']));
            if ($alias && $alias != '') {
                $url_keywords[] = '/event/'.$alias;
            }
        }
    }

    // clean date formats
    if ($date_begin) {
        $date_begin = date("Y-m-d", strtotime($date_begin));
    }
    if ($date_end) {
        $date_end = date("Y-m-d", strtotime($date_end));
    }
    // get traffic data for URLs
    foreach ($url_keywords as $keyword) {
        $requests[] = get_request_for_keyword($keyword, $date_begin, $date_end);
    }

    // build query URL
    $path = "https://matomo.qgiv.com/index.php";
    $token = "38fd323ceed1df7a94de0c5d2ce4b847";

    $data = array(
        'token_auth' => $token,
        'module' => 'API',
        'method' => 'API.getBulkRequest',
        'format' => 'json'
    );
    for ($i = 0; $i++; $i < count($requests)) {
        $data['url['.$i.']'] = $requests[$i];
    }

    // make API call
    $ch = curl_init($path);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    $rsp = curl_exec($ch);
    curl_close($ch);

    // process response
    $data = json_decode($rsp);
    $clean_data = array();
    $segment_counter = 0;
    if (count($data)) {
        foreach ($data as $segment) {
            $segment_counter += 1;
            foreach ($segment as $date => $entry) {
                if (count($entry)) {
                    $unique_visits = $entry['nb_uniq_visitors'];
                    $visits = $entry['nb_visits'];
                    $bounce_rate = $entry['bounce_rate'];
                    $avg_time_on_site = $entry['avg_time_on_site'];
                } else {
                    $unique_visits = 0;
                    $visits = 0;
                    $bounce_rate = "0%";
                    $avg_time_on_site = 0;
                }

                if (isset($clean_data[$date])) {
                    $clean_data[$date] = array(
                        'unique_visits' => $unique_visits,
                        'visits' => $visits,
                        'bounced_visits' => $bounce_rate * $visits,
                        'total_time_on_site' => $avg_time_on_site * $visits
                    );
                } else {
                    $clean_data[$date]['unique_visits'] += $unique_visits;
                    $clean_data[$date]['visits'] += $visits;
                    $clean_data[$date]['bounced_visits'] += $bounce_rate * $visits;
                    $clean_data[$date]['total_time_on_site'] += $avg_time_on_site * $visits;
                }
            }
        }
    }

    // average time on site
    foreach ($clean_data as $date => &$entry) {
        // average time on site
        $entry[$date]['avg_time_on_site'] = $entry[$date]['total_time_on_site'] / $entry[$date]['visits'];
        // average bounce rate
        $entry[$date]['bounce_rate'] = $entry[$date]['bounced_visits'] / $entry[$date]['visits'];
    }

    return $clean_data;
}


function get_request_for_keyword($keyword, $date_begin, $date_end) {
    $path = "idSite=1&module=API";
    $path += "&period=day&date=".$date_begin.",".$date_end;  // data by day for the range specified
    $path += "&method=VisitsSummary.get";  // get visit report
    $path += "&segment=entryPageUrl=@".$keyword;  // segment to entryUrl containing org keywords

    return $path;
}


/*
VisitsSummary.get returns a general report of visit activity. avg_time_on_site is reported in seconds. Example output:

{
    "2019-03-09":[
        "nb_uniq_visitors":4823,
        "nb_users":0,
        "nb_visits":5369,
        "nb_actions":20332,
        "nb_visits_converted":635,
        "bounce_count":2910,
        "sum_visit_length":1860888,
        "max_actions":97,
        "bounce_rate":"54%",
        "nb_actions_per_visit":3.8,
        "avg_time_on_site":347
    ],
    "2019-03-10":{
        "nb_uniq_visitors":4823,
        "nb_users":0,
        "nb_visits":5369,
        "nb_actions":20332,
        "nb_visits_converted":635,
        "bounce_count":2910,
        "sum_visit_length":1860888,
        "max_actions":97,
        "bounce_rate":"54%",
        "nb_actions_per_visit":3.8,
        "avg_time_on_site":347
    },
    ...
}
*/