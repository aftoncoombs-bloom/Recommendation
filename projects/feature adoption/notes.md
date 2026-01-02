# Stages of adoption

1. __Awareness__: the client becomes aware of the feature or product by marketing efforts, visiting the given control panel page, etc.
2. __Exploration__: the client interacts with the feature or product; could be creating an option or turning on a feature, possibly termporarily, in such a way that it is not revealed to donors
3. __Implementation/adoption__: the client deploys a feature or product, exposing it to potential donors 
4. __Bidirectional Adoption__: the client has sustained a new feature or product and donors have engaged with it
5. __Institutionalized__: the client and donors have sustained contact with a new feature or product such that it has become an institutional component of their fundraising efforts; either representing or represented within 10% or more of the fundraising or donors

# Methods of evaluation

1. Awareness
    1. page views
    2. logging in during a period in which a feature or product has been highlighted in the login form
    3. has received marketing materials
2. Exploration
    1. multiple page views
    2. settings form interactions
    3. creating "test" versions
3. Implementation/adoption
    1. enabling demo version
    2. creating non-"test" versions that may remain hidden from donors
    3. configuring products prior to a marketing campaign
4. Bidirectional adoption
    1. associated __transactions__
5. Institutionalized
    1. represented by >= 10% __transaction__ volume or donor counts (ie, a given transaction source or type)
    2. represented in >= 10% __transaction__ volume or donor counts (ie, donation fee covering, restrictions, custom fields, etc.)
    
# Notes

- Can't do _awareness_ right now; need more specific data points of client control panel interactions
- _exploration_ could be approximated right now with database updates; check for features that were edited/deleted, evidence of past transactions without current feature activation, etc.
- _implementation_ is accessible from current settings
- _bidirectional adoption_ and _institutionalized_ can be calculated from transactions table

# Operations

- to start the process, visit the dashboard.py location and execute "nohup python dashboard.py"
- the dashboard will be available at \[address\]:8050/