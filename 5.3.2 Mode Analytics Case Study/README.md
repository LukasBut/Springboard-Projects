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
1. Marketing email frequency drop/increase. 
2. Decrease in activation of accounts by Yammer. 
3. Businesses hiring new employees, hence new Yammer users leading to the gradual increase in engagement,
but then drop is due to those users discontinuing their use of Yammer.
4. Broken product feature.
5. Yammer users going on holiday.
6. No reason.

## Method for testing (number corresponds to previous list element)
1. Given that it doesn't make sense to identify the individuals that were active during the week before the drop, but not active during the week 
of the drop (as there are users who weren't active during the busiest week, but were active during the week of the drop, including other
combinations of activity and non-activity of users) we have to try and find patterns across all users and then see if 
any variables correlate with 'active users'.

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


## Findings After Testing Each Hypothesis
1. All queries were limited to roughly a month before the 'engagement drop' week as if indeed the increase/decrease of Yammer emails is the
cause, then the effect of users deciding not to engage with the product wouldn't take long (less that a week I assume).However, I kept the date range at a month
to have enough data to spot trends. First I calculated the average amount of emails/user/week (# Emails/user). The variance was very small leading up to the 
drop so it means that our initial hypothesis was wrong. Then I wondered if perhaps it wasn't so much the emails annoying people, but the lack of engagement with
the emails (due to lack of relevance perhaps) that could be the cause of the drop. Having calculated the '% of Emails Interacted with' column I found
that the proportion remained pretty much constant. So it wasn't the decreased engagement in emails that was the cause either. The scatter graphs 
(found in the report) further reinforce this point (lack of correlation). However, after August 4th the proportion of emails interacted with
did drop by a few percent (more so than the usual variation), but not as significant (proportion wise) as the drop in active users. I concluded that 
emails were not the cause of the drop. It's important to note that it could have been possible to track each individual user and the amount of emails
they get, and how they interacted with them and so on, but that would increase the complexity of the problem immensely and so for the purposes of saving
time I was willing to make a Type 1 error in favor of testing other hypotheses.

2. Next was checking if there was a decrease in activation of Yammer accounts and whether that was the reason. Having calculated the appropriate
columns, I made a scatter graph of the 'Activated Users' and 'Number of (Active) Users' columns and found a strong positive correlation. There were
2 anomalies, but they both corresponded to data points after the drop. From this we can tell that the more users that Yammer activates, the more
active users they will have. It's hard to verify that hypothesis since once again, we would need a highly computationally heavy brute force approach
to check each user and see how often an activated user becomes an active user (one with 1 or more engagements/week) and so on. Having looked at 
values in the 'Number of Users Activated' column we don't find a notable drop so this means that, once again, our initial hypothesis was false.
The 'Activation %' column further reinforces this point. I've made the assumption that if accounts are activated, on average, they are activated within
a week and so on average if an account is created in a given week it is also confirmed in that week and so it makes sense to calculate 
'Activation %' week by week. Interestingly, for the last 2 weeks of the data in the table, the 'Activation %' values are higher following the drop
in engagement by a considerable amount (usual variation is +-1%, the increase is 2%, 6% ). Possibly in response to the drop in engagement as an 
attempt to increase engagement (this goes in tandem with our assumption earlier on that an increased activation of user accounts leads to more 
active users). However, once again we conclude that our initial hypothesis was false.

3.