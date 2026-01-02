# Data Exploration

## Goal

Create a model that accurately predicts the volume and transaction count of a form given a set of features.

The initial target variables are `don_form_trans_count` and `don_form_trans_vol`.

## Process

Using a random forest as a starting point, I am attempting to find the best set of features to minimize the MSE.

1. Train an initial algorithm and note the results. 
2. Drop the least important (~10%) features in an attempt to drop the error and remove noise.
3. Model a derivative for the target (Growth Rate, Growth of Growth Rate, etc) 
    or 
   Extrapolate the constituency of an organization or any other feature that represents the scale.
   

## Time Series Modeling

Group by form and how long the settings remained static. What was the average volume and transaction count?
Look for changes to a setting, add lag and check again.


## Algorithm Ideas

- Random Forest
- Gradient Boosting Machine
- Support Vector Machine

Getting this out of the way in the notebook for now

# # Train Support Vector Machine
# classifier = LinearSVC(random_state=0, tol=1e-5)
# classifier.fit(
#     X_train,
#     y_train.values.ravel()
# )

# prediction = classifier.predict(X_test)
# mse = mean_squared_error(prediction, y_test)
# mse