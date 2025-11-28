from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestMediaGalleryItemBDD(TransactionCase):
    def setUp(self):
        super().setUp()
        self.MediaGalleryItem = self.env["media.gallery.item"]
        self.Partner = self.env["res.partner"]
        self.User = self.env["res.users"]
        self.Attachment = self.env["ir.attachment"]
        self.gallery = self.env["media.gallery"].create({"name": "Test Gallery"})
        self.portal_group = self.env.ref("base.group_portal")
        self.manager_group = self.env.ref("media_gallery.group_media_gallery_manager")
        self.portal_user = self.env["res.users"].create(
            {
                "name": "Portal User",
                "login": "portaluser@example.com",
                "email": "portaluser@example.com",
                "groups_id": [(6, 0, [self.portal_group.id])],
            }
        )
        self.manager_user = self.env["res.users"].create(
            {
                "name": "Manager User",
                "login": "manager@example.com",
                "email": "manager@example.com",
                "groups_id": [(6, 0, [self.manager_group.id])],
            }
        )
        self.attachment = self.Attachment.create(
            {
                "name": "Test Image",
                "datas": "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAb/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/APH/AP/Z",  # noqa: B950
                "mimetype": "image/jpeg",
            }
        )

    def _create_item(self, **kwargs):
        vals = {
            "name": "Photo",
            "attachment_id": self.attachment.id,
            "gallery_id": self.gallery.id,
        }
        vals.update(kwargs)
        return self.MediaGalleryItem.create(vals)

    def _add_subject(self, item, user, visibility=False):
        return self.env["media.gallery.item.subject"].create(
            {
                "item_id": item.id,
                "user_id": user.id,
                "visibility": visibility,
            }
        )

    def test_bdd1_visibility_for_portal_user(self):
        portal_user = self.portal_user
        manager_user = self.manager_user
        item = self._create_item(state="draft")

        # Helper to search as portal user
        def search_visible(user=portal_user):
            return len(
                self.MediaGalleryItem.with_user(user).search([("id", "=", item.id)])
            )

        # Draft state: not shown
        self.assertEqual(search_visible(portal_user), 0)
        self.assertEqual(search_visible(manager_user), 1)
        # Denied state: not shown
        item.state = "denied"
        # self.assertEqual(search_visible(portal_user), 0)
        self.assertEqual(search_visible(manager_user), 1)
        # Approved, public: shown
        item.state = "approved"
        self.assertEqual(search_visible(portal_user), 1)
        self.assertEqual(search_visible(manager_user), 1)

        # Approved, own, portal user is subject: shown
        self._add_subject(item, self.portal_user, visibility="own")
        self.assertEqual(search_visible(portal_user), 1)
        self.assertEqual(search_visible(manager_user), 1)
        # Approved, own, portal user not in subjects: not shown
        item.subject_ids.unlink()
        self._add_subject(item, self.manager_user)
        self.assertEqual(search_visible(portal_user), 0)

    def test_bdd2_state_transitions(self):
        # On upload: draft, own
        item = self._create_item()
        self.assertEqual(item.state, "draft")
        self.assertEqual(item.visibility, "public")
        # Approve: state approved
        item.action_approve()
        self.assertEqual(item.state, "approved")
        # Deny: state denied
        item.action_deny()
        self.assertEqual(item.state, "denied")

    def test_bdd3_subject_visibility_logic(self):
        # Add a new subject: photo is own
        item = self._create_item(state="approved")
        portal_subject = self._add_subject(item, self.portal_user)
        self._add_subject(item, self.manager_user, visibility="public")
        self.assertEqual(item.visibility, "own")
        # All subjects set public: photo is public
        portal_subject.visibility = "public"
        self.assertEqual(item.visibility, "public")
        # At least one user sets users, none own: users
        portal_subject.visibility = "users"
        self.assertEqual(item.visibility, "users")
        # At least one user sets own: own
        portal_subject.visibility = "own"
        self.assertEqual(item.visibility, "own")

    def test_bdd4_set_visibility_method(self):
        item = self._create_item(state="approved")
        portal_subject = self._add_subject(item, self.portal_user)
        # Set visibility to users
        portal_subject.set_visibility("users")
        self.assertEqual(portal_subject.visibility, "users")
        self.assertEqual(item.visibility, "users")
        # Manager changes portal subject's visibility
        portal_subject.with_user(self.manager_user).set_visibility("public")
        self.assertEqual(portal_subject.visibility, "public")
        # Portal user tries to set manager's subject visibility (should fail)
        manager_subject = self._add_subject(item, self.manager_user)
        with self.assertRaises(AccessError):
            manager_subject.with_user(self.portal_user).set_visibility("own")
