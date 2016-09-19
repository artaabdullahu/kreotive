from flask import Blueprint
from mod_views.user import User
from mod_views.profile import Profile
from flask.ext.login import login_required

mod_profile = Blueprint('profile', __name__, url_prefix='/profile')

profile = Profile()

'''
    Profile
'''
# Article archive page

mod_profile.add_url_rule(
    '/<string:username>/archive',
    methods = ['GET'],
    view_func=profile.archive)

# Article archive page

mod_profile.add_url_rule(
    '/<string:username>/search',
    methods = ['GET'],
    view_func=profile.search)

# Profile about page
mod_profile.add_url_rule(
    '/<string:username>/about',
    methods = ['GET'],
    view_func=profile.about)

# Profile feed page
mod_profile.add_url_rule(
    '/<string:username>',
    methods=['GET'],
    view_func=profile.feed)

# Profile feed page
mod_profile.add_url_rule(
    '/<string:username>/<string:category>',
    methods=['GET'],
    view_func=profile.category_feed)

# Follow a profile
mod_profile.add_url_rule(
    '/<string:username>/<string:action>',
    methods=['POST'],
    view_func=profile.follow)

# Paginated articles of a specific profile
mod_profile.add_url_rule(
    '/articles/<string:username>/<int:skip_posts_number>/<int:posts_per_page>',
    methods=['POST'],
    view_func=profile.paginated_author_articles)

# Profile account settings
mod_profile.add_url_rule(
    '/<string:username>/settings',
    methods=['GET', 'POST'],
    view_func=profile.profile_settings)

# # Articles of a profile/author
# mod_profile.add_url_rule(
#     '/<string:username>/articles',
#     methods=['GET', 'POST'],
#     view_func=profile.articles)
#
# #Profile articles
# mod_profile.add_url_rule(
#     '/<string:username>/articles',
#     methods=['GET'],
#     view_func=profile.articles)

mod_profile.add_url_rule(
    '/<string:username>/memberships',
    methods=["GET"],
    view_func=profile.memberships)

mod_profile.add_url_rule(
    '/upload',
    methods=["GET", 'POST'],
    view_func=profile.upload_avatar)

mod_profile.add_url_rule(
    '/photo/<filename>',
    methods=["GET"],
    view_func=profile.get_avatar_url)
