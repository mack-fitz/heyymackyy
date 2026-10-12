# @heyymackyy playbook (AI photo account)

Scheduled runs read this whole file first. This account is separate from the golf clip pages:
different Zernio profile, different repo, different voice. Never cross-post or mention the golf accounts.

## Accounts (Zernio)
- X @heyymackyy: account ID 6acc660deb5aada570f94a4e (live now)
- Instagram: not created yet. When an Instagram account appears in Zernio on the same profile as
  @heyymackyy (check accounts_list), start posting there too (rules below). Do not use @moremackygolfs.

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

## Pace and timing (Mountain time)
- X: 3 posts a day: morning 8:30-10:00, afternoon 1:00-3:00, evening 7:30-9:30. Vary minutes.
  Mostly single images; about one post a day can be 2-4 images from the same set.
- Instagram (once it exists): 2 feed posts a day (mix of carousels from sets and singles, 4:5),
  plus 1-3 stories a day from leftover singles. Set the AI-generated label on every Instagram post
  (is_ai_generated / AI info) because Instagram expects disclosure of realistic AI images.
- Don't reuse an image on the same platform within 30 days. Prefer images never posted.
- Keep at least 3 days of posts scheduled ahead when there's enough content.

## X settings
- Posts are not explicit, so don't mark them sensitive. If X ever flags or limits the account,
  tell Mack.

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
5. **Message Mack** (SendUserMessage), short: what's scheduled today (times MT, caption each),
   yesterday's X numbers (impressions/views, likes, follows if available), how many unposted
   images are left and how many days that covers (warn under 5 days), anything skipped or failing.
