# Requirements

1. Need a flexible deployment method of models (deploy models individually as the model and not scripts, minimal code)
2. Deployment via git
3. Validation & feedback is necessary from day 1
4. Summary stats of performance history needs to be accessible

### Notes

- deploy models as json with accompanying Pickle files from git repository
- store model validation after training, use the best fitted model
- need a way to test both models without activating them
  - model is trained and the system chooses the old model or weights, I need to be able to interact with and use the dormant model or weights within the system without having to activate them in order to explore what went wrong
  - perhaps remotely activating models or trained weights manually?
- log all actions for transparency into the system
- automated tests of all functions to insure validity of the system in an automated manner
- specify model validation method in the json file

*Pickle files are serialized Python objects*

___

# Functions

### load_model(model)

Opens a json-formatted meta file and Pickle file containing the serialized, trained model object specified by filename without extension. File is expected to be located within the currently active directory.

### load_training_data(use_csv=True)

Loads data from hardcoded CSV files and returns a merged dataframe.

### train_model(model, data=None)

Trains a given model with stored data, returning the calculated weights

### validate_model(fit, target=None)

Validates the supplied model by the validation method specified in the model definition.

### update_model(model, weights=None)

Retrains a stored model, calculating updated weights via train_model() or new weights passed, then writing them to the Pickle file and stores the metadata to an accompanying json file.

### predict(model, input)

Executes a prediction of the supplied model using the supplied input values.

___

# Server Architecture

## Data

1 SQL server

_Responsibilities_

- Stores analytics data
- receives data pushed out of the production Qgiv environment

## Processing

1 VM w/ the following installed: Anaconda Python distro, RStudio Server, git

_Responsibilities_

- Provides an API endpoint to receive input values and respond with prediction output; varies from one model to another
- Trains models, storing coefficients for future predictions
- Uses git to retrieve new, untrained model configurations
- Stores a training history for the models, tracking tests which indicate whether or not the newly trained coefficients improve accuracy over the older trained coefficients
- Log requests for the purposes of tracking down issues that may arise

___

# Proposed Logical Flow

1. User attempts change in the production client control panel
2. The production control panel, whether it be on the frontend or backend, collects the relevant data points for the form being interacted with and sends them to an API endpoint designating which feature will be changed.
3. The remote system/API processor will recognize the designated feature to change, load the pertinent model, and process the relevant data points (potentially adding complication & bases terms, as dictated from the model).
4. The remote system/API processor performs the prediction for the current system, then performs the change to be made for the specified feature to be changed and repeats the prediction.
5. The difference between the predictions is then returned to the requesting system in production.
6. The production control panel receives the prediction difference and presents this difference, using it's own verbiage and presentation methods, to the user.