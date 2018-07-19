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

from .about import About
from .activity import Activity
from .activity_definition import ActivityDefinition
from .activity_list import ActivityList
from .agent import Agent
from .agent_account import AgentAccount
from .agent_list import AgentList
from .attachment import Attachment
from .attachment_list import AttachmentList
from .base import Base
from .context import Context
from .context_activities import ContextActivities
from .documents.activity_profile_document import ActivityProfileDocument
from .documents.agent_profile_document import AgentProfileDocument
from .documents.document import Document
from .documents.state_document import StateDocument
from .extensions import Extensions
from .group import Group
from .http_request import HTTPRequest
from .interaction_component import InteractionComponent
from .interaction_component_list import InteractionComponentList
from .language_map import LanguageMap
from .lrs_response import LRSResponse
from .remote_lrs import RemoteLRS
from .result import Result
from .score import Score
from .serializable_base import SerializableBase
from .statement import Statement
from .statement_base import StatementBase
from .statement_list import StatementList
from .statement_ref import StatementRef
from .statement_targetable import StatementTargetable
from .statements_result import StatementsResult
from .substatement import SubStatement
from .typed_list import TypedList
from .verb import Verb
from .version import Version
