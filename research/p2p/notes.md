# Abandoned gifts

From the slack chat w/ Sandra Billewicz

```
here is the short version and feel free to let me know if you need more detail or if you want to chat through it:
- we are using a browser cookie to store the basic abandoned information ( amount and first name of the abandoned gift)
- In the case that we are able to collect email as well, we will have a more advanced cookie that stores a token which links back to a suspended transaction in the db which will store as much information as the user has entered
- Once the gift is picked up, the cookie is removed and if a suspended transaction existed, that one is completed
- the gift can be picked up from either visiting the page again or clicking an email link ( if we collected email)
```

Need to confirm:

1. logs are created when a suspended transaction is created (or some other manner of identifying these transactions)
2. can we do back end tracking for transactions w/out an email address therefore no suspended transaction?