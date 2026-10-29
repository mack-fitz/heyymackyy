# @heyymackyy playbook (AI photo account)

Scheduled runs read this whole file first. This account is separate from the golf clip pages:
different Zernio profile, different repo, different voice. Never cross-post or mention the golf accounts.

## Accounts (Zernio)
- X @heyymackyy: account ID 6acc660deb5aada570f94a4e
- Instagram @heyymackyyy: account ID 6ae3a47ccb3d8f16f0ac324e (connected Oct 29). Same Zernio profile
  6acc65bd97b2d869b209c7c9. Never use or mention @moremackygolfs, @mackygolfs, @mackthegolfer or mackyyaps.

## What the content is
- AI images of Mack (made with FoxyAI), mostly bikini and gym wear, mostly 4:5 portrait.
- Mack drops them into Dropbox `/abmclip`. Files named `..._1.jpeg`, `..._2.jpeg` with the same
  prefix are one photo set (same shoot); use sets for carousels on Instagram and for X threads or
  multi-image posts. Skip exact duplicates (same name with " (1)", or identical size + prefix).
- Ignore subfolders and anything that isn't an image.

## Voice (captions)
- Silly and flirty. Punny, playful, a little unserious. Lowercase is fine.
- Not cheesy, not "AI-sounding": no inspirational quotes, no "living my best life", no emoji walls,
  no hashtag piles, no "link in bio". Max 1 emoji, often none.
- Short: usually under 12 words. Examples of the feel: "gym said leg day. i said beach day",
  "sun's out, buns... also out", "rating my form 10/10 for no reason", "do these shorts make me look
  like i skipped cardio", "lifeguard on duty (not certified)".
- Never mention OnlyFans, subscriptions, prices or "spicy" content in posts. The X bio
  ("angelbabymack on 0f") handles the funnel. No links in posts (X charges $0.20 per link post).
- Never explicit. If an image looks explicit (nudity, sexual pose), do not post it; list it in the
  message for Mack.

## Pace and timing (Mountain time) — Mack, Oct 29 (replaces the old 3/day)
- 2 posts a day on X and 2 a day on Instagram: morning 7:30-8:15 and evening 7:30-9:30. Vary minutes.
- Each slot is the SAME post on X and Instagram: one Zernio post with both platforms, same caption
  and media.
- **Carousels:** images from the same set (same outfit / look / shoot, whether or not the file names
  share a prefix) post together as ONE carousel post. Instagram up to 10 images, X up to 4 (if a set
  has more than 4, give X the best 4 via customMedia). Prefer one carousel per matching set over
  spreading a set across many posts. Every image in a carousel must pass the AI check; drop any that
  fail (and drop one that breaks set consistency, e.g. different earrings).
- Instagram AI label on every Instagram post: platformSpecificData {madeWithAi: true,
  containsSyntheticMedia: true}.
- Don't reuse an image on the same platform within 30 days. Prefer images never posted. Because each
  slot posts to both, an image posted on X in the last 30 days can't be used even if it's new to IG.
- Keep at least 3 days of posts scheduled ahead when there's enough content.

## X settings
- Posts are not explicit, so don't mark them sensitive. If X ever flags or limits the account,
  tell Mack.

## Fix it yourself (Mack's standing rule)
Mack should never have to tell you to circle back. Every run, before messaging him:
- **Failed posts:** find them (posts_list_failed, and any post in this account's schedule whose
  status is failed/error). Fix the cause (re-encode or shrink media, swap a broken media URL for a
  pinned-commit raw URL, re-crop, shorten a caption) and reschedule into the next open slot, or the
  same slot if it hasn't passed. Retry transient errors once; if it fails again, change approach.
- **Empty slots:** every slot for the next 3 days must have a post. Fill any gap.
- **Bad content:** anything that breaks the rules here (AI tells, wrong crop, cut mid-word, hook
  under the audio bar) gets replaced or re-edited before it goes out.
- **Disconnected account / expired token:** this is the one thing you can't fix — tell Mack
  exactly what to reconnect.
- In the message, report fixes as done ("Thursday 8pm was empty — filled it with X"), not as
  questions. Only ask Mack for things you truly can't do.

## Mack's review
Everything scheduled shows on the dashboard's "Up next" queue. Mack may look and ask for changes
in chat; if he says nothing, proceed as planned. Never wait on his approval to post.

## Daily pipeline
1. Clone this repo (add_repo mack-fitz/heyymackyy with push access; git clone --depth 1).
2. **Relay new images:** list Dropbox `/abmclip` (non-recursive). For files not in
   state/processed.json, write their NAMES (one per line, names only, never URLs) to
   inbox/want.txt, commit, push. The fetch-inbox workflow downloads the shared folder using the
   DROPBOX_FOLDER_URL repo secret, puts those files in inbox/media/ and pushes ("Fetch inbox
   media"). Never commit Dropbox links (GitHub blocks the push). Poll `git fetch` until that commit
   lands, pull, check inbox/failed.txt, then `git mv` each file into images/ (keep names), record
   its Dropbox ID in state/processed.json, `git rm` inbox/failed.txt if present, commit, push.
   Images in images/ are served to Zernio from
   https://raw.githubusercontent.com/mack-fitz/heyymackyy/main/images/<name> (URL-encode spaces).
   If the relay step fails, say exactly which step failed and the error text in the message, and
   keep scheduling from images already in images/.
3. **Look at the images** you're about to post (Read them) before writing captions, so the caption
   fits the photo. Crop to 4:5 only if an image is not already 4:5 (center crop, keep the face).
   **AI check is mandatory, every image, every time** (Mack: "don't let things look too AI").
   View the full image AND zoomed crops of each hand, arm, the legs/feet and any mirror. Reject if
   ANY of these: extra or missing arms, legs, hands or fingers (count them: 2 arms, 2 hands,
   5 fingers each where visible); fused, bent-wrong or melting fingers; a hand not connected to an
   arm; a phone grip that makes no sense; a mirror reflection that doesn't match the pose; warped
   straight lines (door frames, racks, tiles) near the body; garbled text or logos; duplicated
   straps or jewelry; waxy, over-smoothed skin; mismatched eyes or earrings. When in doubt, skip.
   Add rejects to `rejected` in state/posted.json with the reason, never post anything listed
   there, and mention rejects in the daily message.
4. **Schedule** with Zernio posts_create_post (scheduled_for in UTC; MT = UTC-6 now, UTC-7 after
   Nov 1). X: platform twitter, accountId above, media_items with type image. Record each post
   in state/schedule.json and state/posted.json, commit, push.
   **Dashboard** (https://claude.ai/artifact/RED3oyrsVPiYhsTJZyTpDK): after any scheduling change run
   `python3 tools/upnext.py /tmp/upnext.json`, upload it as an asset to the dashboard (Artifact
   publish with asset: true), and update `datasets/upnext` source.url + updated (read it first for
   if_version). Refresh `datasets/queue` the same way. Use a `note` on a schedule entry for
   anything Mack should see on the card (e.g. "swapped in: original had a weird hand").
5. **Message Mack** (SendUserMessage), short: what's scheduled today (times MT, caption each),
   yesterday's X numbers (impressions/views, likes, follows if available), how many unposted
   images are left and how many days that covers (warn under 5 days), anything skipped or failing.

## Macky To Do page
**Macky To Do** (https://claude.ai/artifact/NkJnRhgLLfSWz1XXfHbQ79): every run, ArtifactData `update` this account's doc in collection `queues` with `days_left` (number), `detail` (one plain line: what is left and the pace) and `updated` ("Mon D"). Sundays: add 2-3 new docs to `ideas` (fields order, title, where, effort, what, why) that fit Mack's masc/dry/silly vibe. Doc id(s) for this repo: heyymackyy.

Base Camp schedule (same page): every run, ArtifactData `set` collection `schedule`, doc id(s) heyymackyy, to `{items: [{date: "YYYY-MM-DD" (Mountain), time: "HH:MM" 24h Mountain, caption, where?}]}` covering today and tomorrow for that account. The page is now named "Base Camp".
