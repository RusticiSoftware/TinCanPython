"""
Client library for communicating with an LRS (Learning Record Store)
implementing Tin Can API version 1.0.0 or 1.0.1.

Web site: <https://github.com/RusticiSoftware/TinCanPython>

For more info about the Tin Can API, see <http://tincanapi.com/>.
"""

# These imports are for convenience to external modules only.
# Internal tincan modules should continue to use explicit imports,
# since this file will not have run yet.
#
# For example, from the outside, you can say:
# from tincan import RemoteLRS, LRSResponse
#
# but inside the tincan package, we have to use:
#    from tincan.remote_lrs import RemoteLRS
#    from tincan.lrs_response import LRSResponse

from tincan.about import About
from tincan.activity import Activity
from tincan.activity_definition import ActivityDefinition
from tincan.activity_list import ActivityList
from tincan.agent import Agent
from tincan.agent_account import AgentAccount
from tincan.agent_list import AgentList
from tincan.attachment import Attachment
from tincan.attachment_list import AttachmentList
from tincan.base import Base
from tincan.context import Context
from tincan.context_activities import ContextActivities
from tincan.documents.activity_profile_document import ActivityProfileDocument
from tincan.documents.agent_profile_document import AgentProfileDocument
from tincan.documents.document import Document
from tincan.documents.state_document import StateDocument
from tincan.extensions import Extensions
from tincan.group import Group
from tincan.http_request import HTTPRequest
from tincan.interaction_component import InteractionComponent
from tincan.interaction_component_list import InteractionComponentList
from tincan.language_map import LanguageMap
from tincan.lrs_response import LRSResponse
from tincan.remote_lrs import RemoteLRS
from tincan.result import Result
from tincan.score import Score
from tincan.serializable_base import SerializableBase
from tincan.statement import Statement
from tincan.statement_base import StatementBase
from tincan.statement_list import StatementList
from tincan.statement_ref import StatementRef
from tincan.statement_targetable import StatementTargetable
from tincan.statements_result import StatementsResult
from tincan.substatement import SubStatement
from tincan.typed_list import TypedList
from tincan.verb import Verb
from tincan.version import Version
