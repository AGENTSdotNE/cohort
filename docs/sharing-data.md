# Sharing data between users

[Adding a feature](adding-a-feature.md) builds data that belongs to one person: each user sees only their
own tasks. Most projects also need data that several people touch. Staff might see everyone's requests, a
record might be handed to someone else, and two people might edit the same thing. This guide shows the
smallest change for each case, using the `Task` example.

In every case, `get_queryset` decides what a user can see and change. Hiding a button in React protects
nothing, because anyone can send the request themselves. Decide the rules first, write them in your
decision log, then pick the sections that match. Each one starts from the code in the feature guide.

## Everyone can read, only the owner can change

Inside `TaskViewSet`, return every row for reads, and only the user's own rows for changes. Changing
someone else's task then gets a 404, exactly as before.

```python
from rest_framework import permissions

from .models import Task


class TaskViewSet(viewsets.ModelViewSet):
    ...

    def get_queryset(self):
        if self.request.method in permissions.SAFE_METHODS:
            return Task.objects.all()

        return self.request.user.tasks.all()
```

The screen now lists other people's tasks, so send the owner too and only show the buttons on your own:

```python
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'done', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at']
```

`test_you_only_see_your_own_tasks` from the feature guide is now wrong. Replace it with tests that
everyone sees every task, and that changing or deleting someone else's task gets a 404.

## A record handed to someone else

Add a second user field to the model, then run `uv run python manage.py makemigrations` and `make migrate`:

```python
class Task(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks'
    )
```

Both people can see and update the task, but only the owner can delete it:

```python
from django.db.models import Q

from .models import Task


class TaskViewSet(viewsets.ModelViewSet):
    ...

    def get_queryset(self):
        user = self.request.user

        if self.request.method == 'DELETE':
            return user.tasks.all()

        return Task.objects.filter(Q(owner=user) | Q(assigned_to=user))
```

Add `assigned_to` to the serializer's `fields`, or changes to it are silently ignored. Then stop the
assignee handing the task on to someone else:

```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'done', 'created_at', 'assigned_to']
        read_only_fields = ['id', 'created_at']

    def validate_assigned_to(self, assignee):
        user = self.context['request'].user

        if self.instance and self.instance.owner != user and assignee != self.instance.assigned_to:
            raise serializers.ValidationError('Only the owner can hand this task to someone else.')

        return assignee
```

In `tasks/tests/test_tasks.py`, test the owner assigning, the assignee seeing and updating it, the
assignee failing to reassign or delete it, and a third user getting a 404 for all of it.

## A role, such as staff or coordinator

Use Django's built-in groups rather than adding a field to the user. Create the group in Django admin
(**Groups**, then **Add**), and add people to it from their user page.

```python
def is_coordinator(user):
    return user.groups.filter(name='Coordinators').exists()


class TaskViewSet(viewsets.ModelViewSet):
    ...

    def get_queryset(self):
        if is_coordinator(self.request.user):
            return Task.objects.all()

        return self.request.user.tasks.all()
```

This lets coordinators change and delete every task, not only see them. If they should only read, add
`and self.request.method in permissions.SAFE_METHODS` to the `if`. If you also hand tasks to people, the
last line is the `Q(owner=user) | Q(assigned_to=user)` filter from the section above.

Groups live in the database, so create the group again on every environment, including staging. In tests,
create it yourself, and test the "cannot" as well as the "can". These go in `tasks/tests/test_tasks.py`
beside the feature guide's tests, which already import `APITestCase`, `create_user` and `Task`:

```python
from django.contrib.auth.models import Group


class CoordinatorTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        Task.objects.create(owner=create_user(email='other@example.com'), title='Theirs')

    def test_a_coordinator_sees_every_task(self):
        Group.objects.create(name='Coordinators').user_set.add(self.user)

        response = self.client.get('/api/tasks/')

        self.assertEqual([task['title'] for task in response.data], ['Theirs'])

    def test_anyone_else_sees_only_their_own(self):
        response = self.client.get('/api/tasks/')

        self.assertEqual(response.data, [])
```

## Two people editing the same record

Without a check, the last person to save silently overwrites the other's change. A version number catches
it: the frontend sends back the version it loaded, and the save is refused if someone has saved since.

Add the field, then run `makemigrations` and `make migrate`:

```python
class Task(models.Model):
    ...
    version = models.PositiveIntegerField(default=0)
```

Add `'version'` to the serializer's existing `fields`, and check it on every change:

```python
class TaskSerializer(serializers.ModelSerializer):
    ...

    def validate(self, attrs):
        if self.instance is None:
            attrs.pop('version', None)
            return attrs

        if 'version' not in attrs:
            raise serializers.ValidationError('Send the version you loaded with every change.')

        if attrs['version'] != self.instance.version:
            raise serializers.ValidationError('Someone else changed this since you opened it. Reload to see it.')

        attrs['version'] = self.instance.version + 1

        return attrs
```

On the frontend, add `version: number` to the `Task` type, and send it with every change:

```ts
export const updateTask = (task: Task, changes: Partial<Pick<Task, 'title' | 'done'>>) =>
  apiRequest<Task>(`/tasks/${task.id}/`, { method: 'PATCH', body: { ...changes, version: task.version } })
```

Change `TaskItem` to call `updateTask(task, { done: !task.done })`.

Every existing test that sends a `PATCH` now needs `'version'` too. Include it even in tests that expect a
refusal, such as the assignee reassigning, or the 400 comes from the missing version instead of the rule
you meant to test. Then add a test that saves twice with the same version: the second save should get a
400 and leave the first change in place.

A refused save shows its message like any other error: under a form that uses `useApiForm`, or in the
toast for buttons like `TaskItem`. The list then reloads, because `useTaskMutation` refreshes it when a
change fails as well as when it succeeds, so the user sees the newer version.

Two saves in the very same instant can still both pass this check. That is rare enough to accept here.

Simpler options are fine too, as long as the team chose them: last save wins, or only one person can edit
at a time. Write the choice in your decision log.

## Check before you open a pull request

- [ ] You wrote down who can see and who can change each kind of record.
- [ ] There is a test for each "cannot", not only each "can".
- [ ] You tried it in the browser with two accounts. `make seed` creates them.
