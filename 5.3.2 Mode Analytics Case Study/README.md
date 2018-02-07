# Mode Analytics Case Study, "A Drop in Engagement"

URL of overview: https://community.modeanalytics.com/sql/tutorial/sql-business-analytics-training/
URL of case study: https://community.modeanalytics.com/sql/tutorial/a-drop-in-user-engagement/

## My un-ordered list of hypotheses for why there was 'a drop in engagement'
-Users going on holiday and not using Yammer, hence the drop in engagements.

-Start of financial year is 1st April, possibly most hiring is done in the first few months of the financial year and so lots of new sign ups
in those months, but then as budgets are allocated and people are hired, hiring slows down, so less people sign up to yammer and/or stop using Yammer altogether.

-Decrease in activation of accounts by Yammer. The 'organic' loss of a certain amount of users' activity is not compensated by the decreased amount of new
user activity due to lack of activation of accounts.

-If there was a drop in marketing emails sent to active users then that could have possibly correlated with decreased number of engagements,
or conversely perhaps there was an increase in marketing emails and the user demographic responds negatively to the marketing emails leading to
the abandonment of Yammer altogether. While one couldn't state with absolute certainty that the decreased (or increased) frequency of marketing emails
was the cause of decreased engagements, if no other cause is found it could indeed be the cause.

-A broken product feature (either on the app or the website) leading to a certain section of the users not being able to use Yammer.

-There could possibly be no 'reason'. There are obviously fluctuations in the amount of engagements (its not a constant curve) that are not seen
necessarily as drops or increases attributable to any reason. However, given that fluctuations are usually in the +-80 weekly_users range (excluding
the interval April 28th-5th May) and the drop of engagement is 176 weekly users it's highly unlikely that it falls under the case of 'usual fluctuation'.

## Criteria
Given that the ethos of Yammer Analysts, notably to 'maximise the return on their time', as well as the fact that product decisions are based on 
core engagement, retention and growth metrics it would be fair to say that the aim is to provide 'actionably insights'. So the criteria for 
prioritising which hypothesis to test first is the order in which the most possible actionable insight could be gleemed in the shortest amount of 
time. This means giveing a smaller priority to testing hypotheses which, even if found to be true, do not allow Yammer to increase core engagement,
retention etc.

## List of prioritised hypotheses
1.Marketing email frequency drop/increase 
2.Decrease in activation of accounts by Yammer. 
3.Businesses hiring new employees, hence new Yammer users leading to the gradual increase in engagement,
but then drop is due to those users discontinuing user of Yammer.
4.Broken product feature
5.Yammer users going on holiday.
6.No reason.

## Method for testing (number corresponds to previous list element)
1. Having identified the users with no engagement in the 'drop in engagement' period (28th July-4 August) we use the Email Events table 
(tutorial.yammer_emails) to see if those users had more/less marketing emails than the users who did engage in that period. If so then there's a
correlation and the drop/increase in the emails could be the cause.
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




