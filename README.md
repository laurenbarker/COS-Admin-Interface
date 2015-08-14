# OSF Admin Interface

## Django Admin Setup
#### Groups
* general_administrator_group
* prereg_group

#### Permissions
* auth | permission | prereg_admin

## Submodule
* remove token param from the `_on_complete` method of the `DraftRegistrationApproval` class in `website/project/model.py` if present
