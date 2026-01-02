This is an examination of the donation activity surrounding badge awards and automated social media posts within the peer to peer system. The two primary metrics used for comparison are overall averages and a decaying density average. The overall average is the average count of donations that precede or follow an activity over the lifetime of the participation while the decaying density average is the count of donations immediately surrounding an activity with decreasing impact with time (ie, the further it is before or after the event, the less of an impact it has). While these metrics operate on the same scale, they are not directly comparable as the decaying density metric is comprised of multiples of partial consideration of donations inversely proportional to the number of days between the donation and the given activity with a functional limit of influence of 3 days.

# Badges

Badges are a reward system and thus a lagging indicator of individual performance or activity. Given this data is in aggregate, if badges had little to no effect on behavior I would expect to see the majority of activity preceding badge awards as the donation activity would be constantly shifted backwards as more and more badges were awarded and the user did not respond to them. 

68% of users were awarded at least 1 badge and raised \$306.51 and 32% of users were awarded 0 badges and raised \$89.54.

| Metric            | Preceding | Following |
| ----------------- | --------- | --------- |
| overall donations | 1.371738  | 1.712198  |
| decaying density  | 1.512328  | 3.759719  |

Here we see that there are on average 1.37 donations preceding a badge award and 1.71 donations following it. The decaying density averages are more than double following the badge awared being 1.51 preceding and 3.76 following. Clearly donation activity is on the whole shifted after badge awards, primarily when it comes to activity immediately surrounding the badge awards.

This would lead me to believe that badges are indeed driving fundraising. My guess is that the badge is inspiring the participant to greater engagement, or perhaps simply raising their profile with exposure. While the reason is not self evident, it does indeed appear that donations primarily _follow_ badge awards and with a significant bias given the decaying density average. Given users awarded badges raise three times the amount users who are not awarded badges on average, and donations tend to follow these badge awards with such a clear margin, I think it safe to conclude there is a connection between the two.

# Automated Social Posts

Unlike the badge awards, automated social posts are not much of an indicator of event activity as most automated social posts appear to be related to the event end date rather than any particular data point related to the user's performance. I would expect that the social posts are wholly unrelated to user's performance but to draw greater attention to the fundraising page by way of social media and thus drive donations after the posts have been made.

The automated social post data pertains to a rather small subset of the data as only approximately 10% of users have scheduled these, posting 2.43 times. These users on the whole raise nearly twice what the other users raise with an average fundraising total of \$424.38 whereas the users without scheduled social posts raising \$219.03.

The relationship between posts count and funds raised looks pretty weak with a great deal of variance, but holding fairly steady around an average of funds raised per post. Posters do however collect four times the badges than non-posters (8 to 2, respectively) and more than twice the welcome quest steps complete (3.97 to 1.61, respectively).

| Metric            | Preceding | Following |
| ----------------- | --------- | --------- |
| overall donations | 1.553453  | 2.673747  |
| decaying density  | 5.434025  | 5.284498  |

On average 1.55 donations will precede a social post and 2.67 will follow it. This data is based upon automated or scheduled social posts, therefore it is fair to assume that a significant amount of these are scheduled posts based upon certain events within the fundraising center. What is rather interesting here is that while the average total values above would seem to indicate that the majority of donations follow social posts, the decaying density averages appear to be nearly identical with a minimal difference of 5.43 preceding and 5.28 following. These could be considered to be the same value as there is a 1% difference between the two, so the difference is inconsequential.

Another interesting point is that the standard deviations here are flipped, as in the preceding is lower than the proceeding for overall averages where as the proceeding is lower than the preceding for decaying density.

In summary, the majority of donations overall follow social posts but the activity immediately surrounding the social post chronologically is about even. Additionally the distribution is tighter preceding the post overall but tighter following the post when only accounting for activity immediately surrounding the post. This higher concentration of activity could interpreted as a strong association between the two events, however given the lack of difference between the decaying density averages I would stop short of saying they drive immediate donations. It is more likely that the posts drive donations further into the future. It is possible that the decaying density metrics should be opened up a bit, perhaps at multiple steps of 3 days, 5 days, 1 week, and 2 weeks to better evaluate the turnaround of the impact of these social posts.

