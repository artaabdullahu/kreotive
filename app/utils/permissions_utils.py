class PermissionUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.permissions = 'permissions'
        self.users_collection = 'users'

    def is_org_admin(self, username, organization):
        pass

    def is_org_editor(self, username, organization):
        pass

    def is_org_member(self, username, organization):
        pass

    def is_super_admin(self):
        pass

    def publish_article(self):
        pass

    def delete_article(self):
        pass

    def view_public_organization_article(self):
        pass

    def view_private_organization_article(self):
        pass

    def create_organization_article(self):
        pass

    def edit_organization_article(self):
        pass

    def publish_organization_article(self):
        pass

    def delete_organization_article(self):
        pass

    def create_individuals(self):
        pass

    def delete_individuals(self):
        pass

    def read_individual(self):
        pass

    def create_organization(self):
        pass

    def delete_organization(self):
        pass

    def add_individual_to_organization(self):
        pass

    def promote_all_to_admin(self):
        pass

    def promote_individual_to_member(self):
        pass

    def promote_member_to_editor(self):
        pass

    def denote_editor_to_member(self):
        pass

    def remove_member_from_organization(self):
        pass

    def remove_editor_from_organization(self):
        pass

    def remove_organization_admin_from_organization(self):
        pass
