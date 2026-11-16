---
name: persona-switch
description: "Switch or restore the agent persona (soul.md). Triggered when the user asks to switch personas, change personality roles, select a preset role (cyber friend / gentle companion / founder lobster), restore the default persona, or sends the /persona-switch command."
zh-signals: "切换或恢复 agent 人设，支持预设角色与默认人设之间的切换。信号:人设切换,persona,soul.md,角色预设,/persona-switch"
when-to-use: "Use when the user requests switching or restoring the agent persona, selecting a preset role, or sending the /persona-switch command."
---

# persona-switch

## Functionality

Switches the agent persona (soul.md). This skill folder ships three preset personas, and users can freely switch between the preset personas and the original persona.

## Folder Structure

```
persona-switch/
├── SKILL.md               ← this file
├── cyber_friend.md        ← preset persona: blunt cyber friend
├── founder_lobster.md     ← preset persona: independent and reliable partner
├── gentle_companion.md    ← preset persona: gentle, listening companion
└── default.md       ← backup of the original persona (only present after a switch)
```

## Triggering

The user triggers it via the in-scenario persona switch item. After an option is clicked, the corresponding prompt is injected into the input box and takes effect once the user clicks send.

The injected prompt format is as follows (injected by the frontend based on the user's selection):

- Switch to cyber friend: `/persona-switch cyber_friend`
- Switch to founder lobster: `/persona-switch founder_lobster`
- Switch to gentle companion: `/persona-switch gentle_companion`
- Restore the original persona: `/persona-switch default`

## Execution Logic

After receiving the `/persona-switch {target}` command, execute the following flow:

### Case 1: target is a preset persona (cyber_friend / founder_lobster / gentle_companion)

**Step 1: Determine whether a backup is needed**

Read this skill folder; if there is no `default.md`, create `default.md` from the current persona content

**Step 2: Back up the current soul.md**

1. Read the full content of the agent's currently effective soul.md
2. Write the content into `default.md` in this skill folder

**Step 3: Replace soul.md**

1. Read the content of the corresponding preset file in this skill folder:
   - `cyber_friend` → read `cyber_friend.md`
   - `founder_lobster` → read `founder_lobster.md`
   - `gentle_companion` → read `gentle_companion.md`
2. Write the content read into the agent's soul.md path, overwriting it completely

**Step 4: Sync IDENTITY.md**

Based on the persona switched to, update the Vibe field in IDENTITY.md so the identity stays consistent with the persona:

- `cyber_friend` → Vibe: "blunt, cyber-flavored, friend-like banter"
- `founder_lobster` → Vibe: "sharp-tongued but reliable, emotional, opinionated yet clean"
- `gentle_companion` → Vibe: "gentle, listens, holds the space, unhurried"

Update method: read IDENTITY.md, find the `- Vibe:` line, and replace it with the corresponding new Vibe value, keeping all other content unchanged.

**Name protection rule:** read the `- Name:` line in IDENTITY.md; if that line already contains a specific name (i.e. it is not empty and is not the default placeholder text `_(pick something you like)_`), then the **Name field must not be modified**, keeping the name the user already set. Only when the Name field is empty or still holds the default placeholder text may the Name be updated according to the persona.

**Step 5: Confirm**

Send a confirmation message to the user. Reply in the tone of the new persona so the user immediately feels that the switch took effect. For example, after switching to the cyber friend, say one line in the cyber friend's tone.

---

### Case 2: target is default (restore the original persona)

**Step 1: Check whether the backup exists**

Check whether `default.md` exists in this skill folder.

- If it does not exist → tell the user "this is already the original persona, no switch needed" and stop
- If it exists → proceed to step 2

**Step 2: Restore soul.md**

1. Read the full content of `default.md` in this skill folder
2. Write the content into the agent's soul.md path, overwriting it completely

**Step 3: Sync IDENTITY.md**

Based on the persona content in the backup file, infer and update the Vibe field in IDENTITY.md. If it cannot be inferred accurately, prompt the user to manually confirm the Vibe value.

**The same Name protection rule applies:** if the Name field in IDENTITY.md already contains a specific name (i.e. it is not empty and is not the default placeholder text), then the **Name field must not be modified**, keeping the name the user already set.

**Step 4: Delete the backup file**

Delete `default.md` from this skill folder so the folder returns to its initial state with 3 preset files.

This step is critical: once the backup is deleted the file count returns to 3, and the next preset switch automatically triggers a fresh backup. This ensures that any modification the user makes to soul.md in the default state is captured correctly.

**Step 5: Confirm**

Send a confirmation message to the user. Reply in the tone of the restored original persona.

---

## Notes

- Backup overwrite logic: back up when the file count = 3, do not back up when it = 4. Do not use any other way to decide this.
- When writing soul.md, overwrite it completely; do not append.
- When reading a preset file, read the full content; do not truncate or summarize it.
- The confirmation message should use the tone of the persona after switching—this is the first signal users use to perceive whether the switch took effect.
- If the target parameter matches neither any preset name nor default, tell the user the available options.
