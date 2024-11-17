# VNDB TABLE

## VN

### Fields

- **id**: String, vndbid.

- **title**: String, main title as displayed on the site, typically romanized from the original script.

- **titles**: Array of objects, full list of titles associated with the VN, always contains at least one title
  - **lang**: String, language. Each lanuage appears at most once in the titles list.
  - **title**: String, title in the original script.
  - **official**: Boolean.
  - **main**: Boolean, whether this is the "main" title for the visual novel entry. Exactly one title has this flag set in the `titles` array and it's always the title whose `lang` matches the VN's `olang` field. This field is included for convenience, you can of course also use the `olang` field to grab the main title.

- **aliases**: Array of strings, list of aliases.

- **olang**: String, language the VN has originally been written in.

- **devstatus**: Integer, development status. 0 meaning 'Finished', 1 is 'In development' and 2 for 'Cancelled'.

- **released**: Release date, possibly null.

- **languages**: Array of strings, list of languages this VN is available in. Does not include machine translations.

- **platforms**: Array of strings, list of platforms for which this VN is available.

- **image**: Object, can be null.
  - **id**: String, image identifier.
  - **url**: String.
  - **dims**: Pixel dimensions of the image, array with two integer elements indicating the width and height.
  - **sexual**: Number between 0 and 2 (inclusive), average image flagging vote for sexual content.
  - **violence**: Number between 0 and 2 (inclusize), average image flagging vote for violence.
  - **thumbnail**: String, URL to the thumbnail.
  - **thumbnail_dims**: Pixel dimensions of the thumbnail, array with two integer elements.

- **length**: Integer, possibly null, rough length estimate of the VN between 1 (very short) and 5 (very long). This field is only used as a fallback for when there are no length votes, so you'll probably want to fetch `length_minutes` too.

- **length_minutes**: Integer, possibly null, average of user-submitted play times in minutes.

- **description**: String, possibly null.

- **screenshots**: Array of objects, possibly empty.
  - **screenshots.\***: The above `image.*` fields are also available for screenshots.

- **relations**: Array of objects, list of VNs directly related to this entry.
  - **id**: String, vndbid of the related VN.
  - **title**: String, title of the related VN.
  - **relation**: String, relation type.
  - **relation_official**: Boolean, whether this VN relation is official.

- **tags**: Array of objects, possibly empty. Only directly applied tags are returned, parent tags are not included.
  - **id**: String, vndbid.
  - **name**: String.
  - **category**: String, "cont" for content, "ero" for sexual content and "tech" for techinical tags.
  - **rating**: Number, tag rating between 0 (exclusive) and 3 (inclusize).
  - **spoiler**: Integer, 0, 1 or 2, spoiler level.
  - **lie**: Boolean.

- **developers**: Array of objects. The developers of a VN are all producers with a "developer" role on a release linked to the VN.
  - **id**: String, vndbid.
  - **name**: String.
  - **original**: String, possibly null, name in the original script.

- **staff**: Array of objects, possibly empty.
  - **id**: String, vndbid.
  - **name**: String, possibly romanized name.
  - **original**: String, possibly null, name in original script.
  - **eid**: Integer, edition identifier or *null* when the staff has worked on the "original" version of the visual novel.
  - **role**: String.

- **va**: Array of objects, possibly empty. Each object represents a voice actor relation. The same voice actor may be listed multiple times for different characters and the same character may be listed multiple times if it has been vioced by several people.
  - **staff**: Person who voiced the character.
    - **id**: String, vndbid.
    - **name**: String, possibly romanized name.
    - **original**: String, possibly null, name in original script.
  - **character**: VN character being voiced.
    - **id**: String, vndbid.
    - **name**: String.
    - **original**: String, possibly null, name in the original script.

- **extlinks**: Array of objects, links to external website. This list is equivalent to the links displayed on the releasepages on the site, so it may include redundant entries (e.g. if a Steam ID is known, links to both Steam and SteamDB are included) and links that are automatically fetched from external resources (e.g. PlayAsia, for which a GTIN lookup is performed).
  - **url**: String, URL.
  - **label**: String, English human-readable label for this link.
  - **name**: Internal identifier of the site, intended for applications that want to localize the label or to parse/format/extract remote identifiers. Keep in mind that the list of supported sites, their internal names and their ID types are subject to change, but I'll try to keep things stable.
  - **id**: Remote identifier for this link. Not all sites have a sensible identifier as part of their URL format, in such cases this field is simply equivalent to the URL.

## TAG

### Fields

- **id**: String, vndbid.

- **name**: String.

- **aliases**: Array of strings.

- **description**: String.

- **category**: String, "cont" for content, "ero" for sexual content and "tech" for techinical tags.

- **searchable**: Bool.

- **applicable**: Bool.

- **vn_count**: Integer, number of VNs this tag has been applied to, including any child tags.

## PRODUCER

### Fields

- **id**: String, vndbid.

- **name**: String.

- **original**: String, possibly null, name in the original script.

- **aliases**: Array of strings.

- **lang**: String, primary language.

- **type**: String, producer type, "co" for company, "in" for individual and "ng" for amateur group.

- **description**: String, possibly null.

## STAFF

### Fields

- **id**: String, vndbid.

- **ismain**: Boolean, whether the 'name' and 'original' fields represent the main name for this staff entry.

- **name**: String, possibly romanized name.

- **original**: String, possibly null, name in original script.

- **lang**: String, staff's primary language.

- **gender**: String, possibly null, "m" or "f".

- **description**: String, possibly null.

- **aliases**: Array, list of names used by this person.
  - **aid**: Integer, alias id.
  - **name**: String, name in original script.
  - **ismain**: Boolean, whether this alias is used as "main" name for the staff entry.

## CHARACTER 

### Fields

- **id**: String, vndbid.

- **name**: String.

- **original**: String, possibly null, name in the original script.

- **aliases**: Array of strings.

- **description**: String, possibly null.

- **image**: Object, can be null.
  - **image.\***: Same sub-fields as the `image` visual novel field. (Except for `thumbnail` and `thumbnail_dims` because character images are currently always limited to 235x300px, but that is subject to change in the future).

- **blood_type**: String, possibly null, "a", "b", "ab" or "o".

- **height**: Integer, possibly null, cm.

- **weight**: Integer, possibly null, kg.

- **bust**: Integer, possibly null, cm.

- **waist**: Integer, possibly null, cm.

- **hips**: Integer, possibly null, cm.

- **cup**: String, possibly null, "AAA", "AA", or any single letter in the alphabet.

- **age**: Integer, possibly null, years.

- **birthday**: Possibly null, otherwire an array of two integers: month and day, respectively.

- **sex**: Possibly null, otherwise an array of two strings: the character's apparent (non-spoiler) sex and teh character's real (spoiler) sex. Possible values are `null`, "m", "f", "b" (meaning "both") or "n" (sexless).

- **vns**: Array of objects, visual novels this character appears in. The same visual novel may be listed multiple times with a different release; the spoiler level and role can be different per release.
  - **id**: String, vndbid.
  - **title**: String.
  - **spoiler**: Integer.
  - **role**: String, "main" for protagonist, "primary" for main characters, "side" or "appears".

- **traits**: Array of objects, possibly empty.
  - **id**: String, vndbid.
  - **name**: String. Trait names are not necessarily self-describing, so they should always be displayed together with their "group" (see below).
  - **group_id**: String, vndbid.
  - **group_name**: String.
  - **spoiler**: Integer, 0, 1 or 2, spoiler level.
  - **lie**: Boolen.

## TRAIT

### Fields

- **id**: String, vndbid.

- **name**: String. Trait names are not necessarily self-describing, so they should always be displayed together with their "group" (see below).

- **aliases**: Array of strings.

- **description**: String.

- **searchable**: Bool.

- **applicable**: Bool.

- **group_id**: String, vndbid.

- **group_name**: String.

- **char_count**: Integer, number of characters this trait has een applied to, including child traits.


# ATTENTION

- This database is a subset of an existing online database called VNDB. This means that each entry in the database can exist independently, and other entries referenced within an entry may not exist in the local database. When a user requests an entry that doesn't exist in the local database, I will send a request to the online VNDB to obtain the missing data. However, the final decision on whether to store this data in the local database will be made by the user.
- Additionally, it's important to note that if a user chooses to store a VN (Visual Novel) entry in the local database, it is agreed that all CHARACTER entries related to that VN will also be stored locally. However, if the VN entry is later deleted, there is no guarantee that the associated CHARACTER entries will be deleted simultaneously.