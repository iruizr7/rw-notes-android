# RW Notes for Android

**Your better brain**

Android app for [RW Notes](https://github.com/iruizr7/rw-notes), forked from [SiYuan Android](https://github.com/siyuan-note/siyuan-android). Report fork-specific issues in [this repository](https://github.com/iruizr7/rw-notes-android/issues).

## Build

1. Build the RW Notes mobile kernel as `kernel.aar` using the core development guide; place it in `app/libs/kernel.aar`.
2. Build the matching RW Notes mobile frontend. Package `appearance`, `guide`, `stage`, and `changelogs` at the root of `app/src/main/assets/app.zip`.
3. Set the Android SDK path in local `local.properties`. Copy `signings.templates.gradle` to ignored `signings.gradle` and configure your own signing identity for release builds. Never commit signing credentials.
4. Use the checked-in Gradle wrapper: `./gradlew assembleOfficialDebug` for development or `./gradlew buildReleaseTask` for configured release channels. Build configuration can be checked with `./gradlew -I scripts/verify-build.gradle :app:verifyBuildConfiguration`.

The application ID is `com.parendum.rwnotes` (`com.parendum.rwnotes.debug` for debug). The Java namespace remains `org.b3log.siyuan` for upstream compatibility. File-provider authority and shortcut targets follow the application ID. Releases are collected under `app/build-release/rw-notes-${versionName}-all`.

Google Play/F-Droid listings for SiYuan are not RW Notes distribution channels. Store publication and a new branded screenshot set remain separate release work.

## Development branches

`main` tracks the official upstream repository. Work on `rw-notes`; select baseline upgrades explicitly after fetching `main`. `origin` is our fork; `upstream` is the official repository.

## Branding and compatibility

The brand is **RW Notes**, with the slogan **Your better brain** and the icon from the core repository's `app/src/assets/icon.svg`. Regenerate native icons with:

```sh
python3 scripts/generate-branding.py --core-repo ../rw-notes
```

This uses the core icon generator and requires Python, Pillow, and Inkscape. Generated icon files are committed; do not edit them by hand. The core checkout must contain the RW Notes branding generator and SVG.

Keep upstream copyright/license notices, internal source names, kernel paths, JavaScript bridges, and the `siyuan:` protocol for compatibility. The shared frontend and kernel must be built from RW Notes; these native changes alone do not rebrand an upstream frontend bundle. Inherited cloud/purchase integrations remain scheduled for removal under the core v0 plan.

The selected baseline is upstream 3.8.8; see the baseline section below. Version fields do not declare v0 feature completion.

## Selected baseline

Core/frontend/kernel: SiYuan `v3.8.8` (`bfe36100477b7bbd66db1a8b8cff5547b2ccdb59`), plus RW Notes changes. Native source: `89c50f2deaccabfab7b9fe5f94d172887f45b95f`. Build matching artifacts from the adjacent `../rw-notes` checkout. The authoritative [baseline record](https://github.com/iruizr7/rw-notes/blob/rw-notes/specs/upstream-baseline.md) lists provenance and validation limits. Full native packaging and device checks remain pending.

The source configuration is restored to the 3.8.8 release (version code 439). Later 3.8.9 alpha changes remain in Git history but are reversed; future upgrades must deliberately reapply those changes. RW Notes branding and the adapted variant checks are retained.
