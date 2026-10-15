# Agent workflow

understand_request -> find_meetings -(no meeting: END)-> identify_customer -(no external attendee: END)->
[research_crm | research_email | research_documents | research_sheets | research_web] (parallel, joined) ->
validate_evidence -> analyze_customer -> identify_risks -> generate_topics -> generate_briefing ->
quality_check -(fail, up to 2 retries)-> generate_briefing | -(pass)-> human_review (interrupt) -> deliver -> END

Conditional routing: no meetings, unresolved customer, quality retry loop.
Fallbacks: customer not in CRM -> attendee-domain identity, CRM node skipped, email/docs still searched.
Tool failures are caught per node and recorded in `errors` instead of crashing the run.
