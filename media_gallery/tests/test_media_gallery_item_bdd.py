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
        self.manager_group = self.env.ref("base.group_system")
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
        # Draft state: not shown
        item = self._create_item(state="draft")
        self.assertFalse(item.can_portal_user_see(self.portal_user))
        # Denied state: not shown
        item.state = "denied"
        self.assertFalse(item.can_portal_user_see(self.portal_user))
        # Approved, public: shown
        item.state = "approved"
        self.assertTrue(item.can_portal_user_see(self.portal_user))
        # Approved, own, portal user is subject: shown
        self._add_subject(item, self.portal_user, visibility="own")
        self.assertTrue(item.can_portal_user_see(self.portal_user))
        # Approved, own, portal user not in subjects: not shown
        item.subject_ids.unlink()
        self.assertTrue(item.can_portal_user_see(self.portal_user))
        self._add_subject(item, self.manager_user)
        self.assertFalse(item.can_portal_user_see(self.portal_user))

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
