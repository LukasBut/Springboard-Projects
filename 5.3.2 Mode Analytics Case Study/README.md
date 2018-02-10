# Mode Analytics Case Study, "A Drop in Engagement"

URL of overview: https://community.modeanalytics.com/sql/tutorial/sql-business-analytics-training/
URL of case study: https://community.modeanalytics.com/sql/tutorial/a-drop-in-user-engagement/

## My unordered list of hypotheses for 'a drop in engagement'
-Users going on holiday and not using Yammer, hence the drop in engagement.

-1st of April is the start of the financial year. It is likely there are alot of new hires in the first few months of the financial year
leading to alot of new created users leading to the gradual increase in engagement. However, it's possible that having tried Yammer a number
of users decide to use other alternatives, leading to the drop in engagement.

-Decrease in activation of accounts by Yammer. The 'organic' loss of a certain amount of users' activity is not compensated by the decreased amount of new
user activity due to lack of activation of user accounts.

-If there was a drop in marketing emails sent to active users then that could have possibly correlated with decreased number of engagements,
or conversely perhaps there was an increase in marketing emails and the user demographic responds negatively to the marketing emails leading to
the abandonment of Yammer altogether. While one couldn't state with absolute certainty that the decreased (or increased) frequency of marketing emails
was the cause of decreased engagements (since correlation does not imply causation), it could nevertheless be the cause.

-A broken product feature (either on the app or the website) leading to a certain section of the users not being able to use Yammer.

-There could possibly be no 'reason'. There are obviously fluctuations in the amount of engagements (it's not a constant curve) that are not seen
necessarily as drops or increases attributable to any reason. However, given that fluctuations are usually in the +-80 weekly_users range (excluding
the interval April 28th-5th May) and the drop of engagement is 176 weekly users it's highly unlikely that it falls under the case of 'usual fluctuation'.

## Criteria
Given that the ethos of Yammer Analysts ('maximise the return on their time') as well as the fact that product decisions are based on 
core engagement, retention and growth metrics it would be fair to say that the aim is to provide 'actionably insights'. So the criteria for
hypothesis prioritisation is in the order in which the most actionable insight could be gleemed in the shortest amount of time. This means
giving a smaller priority to testing hypotheses which, even if found to be true, don't allow Yammer to increase core engagement, retention etc.

## List of prioritized hypotheses
1.Marketing email frequency drop/increase. 
2.Decrease in activation of accounts by Yammer. 
3.Businesses hiring new employees, hence new Yammer users leading to the gradual increase in engagement,
but then drop is due to those users discontinuing user of Yammer.
4.Broken product feature.
5.Yammer users going on holiday.
6.No reason.

## Method for testing (number corresponds to previous list element)
1. Having identified the users with no engagement in the 'drop in engagement' period (28th July-4 August) we use the Email Events table 
(tutorial.yammer_emails) to see if those users had more/less marketing emails than the users who did engage in that period. If so then there's a
correlation and the drop/increase in the emails could be the cause.
Given that it doesn't make sense to identify the individuals that were active during the week before the drop, but not active during the week 
of the drop (as there are users who weren't active during the busiest week, but were active during the week of the drop, including other
combinations of activity and non-activity of users) we have to try and find patterns across all users.

2. The Users table (tutorial.yammer_users) has columns 'activated_at' and 'created_at', using which we can group the amount of new users created
and the number of activated users each week to see if there was a noticable decline in activated users or disparity in the 2 values
not seen during the other weeks. If so, having calculated the average amount of engagements of users' in their first week after having their 
accounts activated, we multiply that by the number of users whose accounts were not activated to see if that number can account for the drop in
engagement. If so, then it's very likely that the cause in the drop was due to un-activated user accounts. 

3. Using the 'created_at' column we can test our hypothesis of new hires getting Yammer accounts and tracking their engagements week by week to 
see if a noticeable proportion stopped engaging during the week (28th July-4th August). If so then it's likely our hypothesis is true.

4. Though we have no data on this, in a real life scenario we could get this information on broken product features or faults and hence recommend
that fixing those problems gets a higher priority as fixing them would most likely increase engagement again.

5. We can track the engagement/non engagement of each user to see if there is a period of time when there is a significant or complete drop in 
engagement, but a return to the norm a few weeks later as that would most likely indicate that the user went on holiday. While we cannot impact when
Yammer users go on holiday, if that is found to be the reason for the drop then it's valuable in that it means there are no problems that Yammer
have that are stopping them from meeting their goals of increasing core engagement, retention etc.

6. This cannot be tested as such, and cannot be proven as such as that would require an exhaustive negation of every other possible possibility
which is not most likely not possible and even if it were it would take too much time, only to arrive at an insight (there is no reason for
the drop) which is in-actionable. However, unless disproven it is a possibility and hence worth mentioning as a hypothesis.

add column for was a cause or wasn't a cause (subquery to find list of user_id with no engagement in period) by checking if user_id
is in returned subquery user_id list. 

add column for number of emails in past week (2014-07-21 -- 2014-07-28) per user_id. (group by user_id).
add column for COUNT(cause or not cause)

Contributed  Email Count/user classification during week
YES
NO


sql for problem 1:
SELECT emails.occurred_at, emails.action, inactive.* 
FROM (SELECT users.user_id AS "Users User ID",users.created_at, users.state,
  events.event_type, events.occurred_at
  FROM tutorial.yammer_users users LEFT JOIN tutorial.yammer_events events
  ON users.user_id=events.user_id
  WHERE events.event_type!='engagement' AND
  (SUBSTR(events.occurred_at::VARCHAR,1,10)::date BETWEEN '2014-07-28' AND '2014-08-04')) inactive
JOIN tutorial.yammer_emails emails ON inactive."Users User ID"=emails.user_id


SELECT COUNT(DISTINCT events.user_id) AS "Number of Users",
CASE WHEN events.event_type='engagement' 
AND (SUBSTR(events.occurred_at::VARCHAR,1,10))::date 
BETWEEN '2014-07-28' AND '2014-08-04' THEN 'Cause of drop' 
ELSE 'Not a cause of drop' END AS "Drop Contribution",
COUNT(emails.occurred_at) AS "Number of Emails Sent", 
COUNT(emails.occurred_at)/COUNT(DISTINCT events.user_id) AS "Avg # of emails/user"
FROM tutorial.yammer_events events JOIN tutorial.yammer_emails emails 
ON events.user_id=emails.user_id 
WHERE (SUBSTR(emails.occurred_at::VARCHAR,1,10))::date 
BETWEEN '2014-07-21' AND '2014-07-28' GROUP BY "Drop Contribution";


SELECT user_id AS "User ID", COUNT(occurred_at) as "Number of Emails/user in week prior"
FROM tutorial.yammer_emails 
WHERE SUBSTR(occurred_at::VARCHAR,1,10)::date BETWEEN '2014-07-21' AND '2014-07-27'
GROUP BY user_id ORDER BY user_id ;


SELECT   users.user_id
FROM tutorial.yammer_users users JOIN tutorial.yammer_events events
ON users.user_id=events.user_id
WHERE (events.occurred_at BETWEEN '2014-07-28 12:00:00' AND '2014-08-04 12:00:00')
  AND events.event_type='engagement'
  AND users.activated_at IS NOT NULL

EXCEPT

SELECT  users.user_id
FROM tutorial.yammer_users users JOIN tutorial.yammer_events events
ON users.user_id=events.user_id
WHERE (events.occurred_at BETWEEN '2014-08-04 12:00:00' AND '2014-08-11 12:00:00')
  AND events.event_type='engagement'
  AND users.activated_at IS NOT NULL
  
  //Template for emails/week
  (SELECT 
CASE WHEN occurred_at BETWEEN '2014-07-21 12:00:00' AND '2014-07-28 12:00:00'
  THEN '2014/07/21 - 2014/07/28'
WHEN occurred_at BETWEEN '2014-07-14 12:00:00' AND '2014-07-21 12:00:00'
  THEN '2014/07/14 - 2014/07/21'
WHEN occurred_at BETWEEN '2014-07-07 12:00:00' AND '2014-07-14 12:00:00'
  THEN '2014/07/07 - 2014/07/14'
WHEN occurred_at BETWEEN '2014-06-30 12:00:00' AND '2014-07-14 12:00:00'
  THEN '2014/06/30 - 2014/07/07' ELSE 'Outside intervals' END AS "Week Interval",
COUNT(1) AS "Email Count"
FROM tutorial.yammer_emails 
WHERE occurred_at BETWEEN '2014-06-30 12:00:00' AND '2014-08-04 12:00:00'
GROUP BY 1 ORDER BY 1) email_stats
  

