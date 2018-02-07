# Mode Analytics Case Study, "A Drop in Engagement"

URL of overview: https://community.modeanalytics.com/sql/tutorial/sql-business-analytics-training/
URL of case study: https://community.modeanalytics.com/sql/tutorial/a-drop-in-user-engagement/

## My un-ordered list of hypotheses for why there was 'a drop in engagement':
-Users going on holiday and not using yammer, hence the drop in engagements.

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

##Criteria:
Given that the ethos of Yammer Analysts, notably to 'maximise the return on their time', as well as the fact that product decisions are based on 
core engagement, retention and growth metrics it would be fair to say that the aim is to provide 'actionably insights'. So the criteria for 
prioritising which hypothesis to test first is the order in which the most possible actionable insight could be gleemed in the shortest amount of 
time. This means giveing a smaller priority to testing hypotheses which, even if found to be true, do not allow Yammer to increase core engagement,
retention etc.

##Given the criteria the order in which the hypotheses will be tested is:
1.Decrease in activation of accounts by Yammer. 
2.Marketing email frequency drop/increase 
3.