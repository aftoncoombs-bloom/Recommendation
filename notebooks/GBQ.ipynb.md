```python
from google.cloud import bigquery
```


```python
API_KEY = "AIzaSyCDEqEf6T-FmtW_0oy7TSX_wsTPrEBpVTo"
```


```python
client = bigquery.Client()
```


    ---------------------------------------------------------------------------

    DefaultCredentialsError                   Traceback (most recent call last)

    /tmp/ipykernel_16187/1295353249.py in <module>
    ----> 1 client = bigquery.Client()
    

    ~/anaconda3/lib/python3.7/site-packages/google/cloud/bigquery/client.py in __init__(self, project, credentials, _http, location, default_query_job_config, default_load_job_config, client_info, client_options)
        245             credentials=credentials,
        246             client_options=client_options,
    --> 247             _http=_http,
        248         )
        249 


    ~/anaconda3/lib/python3.7/site-packages/google/cloud/client/__init__.py in __init__(self, project, credentials, client_options, _http)
        318 
        319     def __init__(self, project=None, credentials=None, client_options=None, _http=None):
    --> 320         _ClientProjectMixin.__init__(self, project=project, credentials=credentials)
        321         Client.__init__(
        322             self, credentials=credentials, client_options=client_options, _http=_http


    ~/anaconda3/lib/python3.7/site-packages/google/cloud/client/__init__.py in __init__(self, project, credentials)
        266 
        267         if project is None:
    --> 268             project = self._determine_default(project)
        269 
        270         if project is None:


    ~/anaconda3/lib/python3.7/site-packages/google/cloud/client/__init__.py in _determine_default(project)
        285     def _determine_default(project):
        286         """Helper:  use default project detection."""
    --> 287         return _determine_default_project(project)
        288 
        289 


    ~/anaconda3/lib/python3.7/site-packages/google/cloud/_helpers/__init__.py in _determine_default_project(project)
        150     """
        151     if project is None:
    --> 152         _, project = google.auth.default()
        153     return project
        154 


    ~/anaconda3/lib/python3.7/site-packages/google/auth/_default.py in default(scopes, request, quota_project_id, default_scopes)
        646             return credentials, effective_project_id
        647 
    --> 648     raise exceptions.DefaultCredentialsError(_CLOUD_SDK_MISSING_CREDENTIALS)
    

    DefaultCredentialsError: Your default credentials were not found. To set up Application Default Credentials, see https://cloud.google.com/docs/authentication/external/set-up-adc for more information.



```python

```
