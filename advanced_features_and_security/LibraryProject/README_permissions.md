# Django Permissions and Groups Setup

## Custom Permissions (on `Book` model)
Defined in `bookshelf/models.py` under `Meta`:
- `can_view`: View book list/details
- `can_create`: Add new books
- `can_edit`: Modify existing books
- `can_delete`: Remove books

## Groups
Set up via Django Admin:
- **Viewers**: `can_view`
- **Editors**: `can_view`, `can_create`, `can_edit`
- **Admins**: All permissions

## Views with Access Control
Decorators used to enforce permissions in `bookshelf/views.py`:
- `@permission_required('bookshelf.can_view')`
- `@permission_required('bookshelf.can_create')`
- `@permission_required('bookshelf.can_edit')`
- `@permission_required('bookshelf.can_delete')`

## Testing
Log in as different users from each group to verify:
- Access to views is granted or denied accordingly.
