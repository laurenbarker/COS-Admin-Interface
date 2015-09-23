import httplib as http

from modularodm import Q

# importing from the osf.io submodule
from utils import submodule_path
import sys
sys.path.insert(0, submodule_path('utils.py'))
from website.project.model import MetaSchema, DraftRegistration, Node, DraftRegistrationApproval
from website.addons.osfstorage.model import OsfStorageFileNode
from framework.mongo.utils import get_or_http_error
from framework.auth.core import User
from framework.auth import Auth
from website.project.metadata.utils import serialize_meta_schema
from website.app import do_set_backends, init_addons
from website import settings as osf_settings
from website.project.views.file import grid_data
from website.app import app
from website.util import web_url_for

import utils

init_addons(osf_settings, routes=False)
do_set_backends(osf_settings)
# TODO[lauren]: use the user who is logged in
adminUser = User.load('dsmpw')


def get_file_data(nid):
    nid = 'h4qbm'

    auth = Auth(adminUser)
    node = Node.load(nid)
    file_node = OsfStorageFileNode.load('5602d5847996ae03b70ca4b1')
    # osfstoragefilenode = 5602d5847996ae03b70ca4b1
    # file_node.path = '/5602d5847996ae03b70ca4b1'

    # import ipdb; ipdb.set_trace();

    with app.test_request_context():
        mfr_url = node.web_url_for('addon_view_or_download_file', path=file_node.path, provider='osfstorage')
        # node.web_url_for('addon_view_or_download_file', path=file_node.path.strip('/'), provider='osfstorage', action='download', _absolute=True, method='GET')

    # response = grid_data(auth=auth, node=node, )

    # file_data = {
    #     'data': response['data']
    # }

    return mfr_url


def get_all_drafts():
    # TODO[lauren]: add query parameters to only retrieve submitted drafts,
    # they will have an approval associated with them
    all_drafts = DraftRegistration.find()

    auth = Auth(adminUser)

    serialized_drafts = {
        'drafts': [utils.serialize_draft_registration(d, auth) for d in all_drafts]
    }
    return serialized_drafts

get_schema_or_fail = lambda query: get_or_http_error(MetaSchema, query)


def get_draft(draft_pk):
    auth = Auth(adminUser)

    draft = DraftRegistration.find(
        Q('_id', 'eq', draft_pk)
    )

    return utils.serialize_draft_registration(draft[0], auth), http.OK


def get_draft_obj(draft_pk):
    auth = Auth(adminUser)

    draft = DraftRegistration.find(
        Q('_id', 'eq', draft_pk)
    )

    return draft[0], auth


def get_approval_obj(approval_pk):
    auth = Auth(adminUser)

    approval = DraftRegistrationApproval.find(
        Q('_id', 'eq', approval_pk)
    )

    return approval[0], auth


def get_schema():
    all_schemas = MetaSchema.find()
    serialized_schemas = {
        'schemas': [utils.serialize_meta_schema(s) for s in all_schemas]
    }
    return serialized_schemas


def get_metaschema(schema_name, schema_version=1):
    meta_schema = get_schema_or_fail(
        Q('name', 'eq', schema_name) &
        Q('schema_version', 'eq', schema_version)
    )
    return serialize_meta_schema(meta_schema), http.OK
