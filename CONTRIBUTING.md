# Working on this project

How the team works together. Agree any changes to it as a team.

## The loop

1. **Pick up one piece of work.** Something you can finish in a day or two. If it is bigger, split it.
2. **Branch from an up-to-date `main`.**
   ```bash
   git switch main && git pull
   git switch -c add-note-search
   ```
   Name the branch after the change, starting with a verb: `add-note-search`, `fix-empty-task-title`,
   `update-sign-in-copy`. No names or initials.
3. **Commit small and often.** Each commit message says what changed, in the present tense:
   `Add search box to the notes page`.
4. **Run `make test` before you push.** If formatting fails, `make format` fixes it.
5. **Open a pull request** and fill in what it does, how you tested it, and a screenshot for anything
   visual.
6. **Get one review, and wait for CI to pass**, before merging. Delete the branch afterwards.

Never push straight to `main`.

## Reviewing someone else's pull request

Reviewing is how you learn the rest of the codebase, so do it properly:

- Pull the branch and try it, don't just read the diff.
- Check the security line: does every new view's `get_queryset` only return what this user may see?
- Ask questions rather than giving orders: "What happens if the title is empty?"
- Approve when it works and you would be happy to change it next week. It does not have to be how you
  would have written it.

## Code style

The linters and formatters decide layout, so nobody has to argue about it. Beyond that:

- **Copy the existing shape.** Before adding a file, open the nearest similar one and follow it. For a
  new feature, follow [docs/adding-a-feature.md](docs/adding-a-feature.md).
- **Small files, one job each.** One React component per file. If a file passes about 150 lines, split it.
- **Names say what things are.** `task`, not `t` or `data2`.
- **Comments explain why, not what.** If code needs a comment to say what it does, rename or simplify it.
- **Use what is already here.** shadcn components for UI, `apiRequest` for calls, `useQuery` for loading,
  `FormField` for inputs. Search before you build something new.
- **No secrets in the code.** API keys go in `backend/.env`, which is never committed.
