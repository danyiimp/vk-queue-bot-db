from .help import help_labeler
from .admins import admins_labeler
from .list import list_labeler
from .end import end_labeler
from .skip import skip_labeler
from .drop import drop_labeler
from .new import new_labeler

labelers = [list_labeler, drop_labeler, skip_labeler, admins_labeler, help_labeler, end_labeler, new_labeler]
