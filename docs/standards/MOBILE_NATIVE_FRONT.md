# 📱 Mobile Native Design Standards

## 1. Touch-First Interface
* **Hit Targets:** Minimum touch target size is 44x44 points. Ensure enough spacing between buttons to prevent accidental clicks.
* **Thumb Zone:** Place primary actions (Navigation, CTAs) within easy reach of the user's thumb (bottom half of the screen).

## 2. Platform Conventions
* **Native Feel:** Follow Human Interface Guidelines (iOS) or Material Design (Android) where possible.
* **Safe Area Insets:** Always account for notches, home indicators, and status bars using Safe Area views.
* **Gestures:** Utilize common native gestures (swipe to go back, pull to refresh, long press for menus).

## 3. Resource Management
* **Offline First:** Design for intermittent connectivity. Use loading states and local caching for data.
* **Ratio Locking:** Lock image aspect ratios to prevent distortion on varying phone screen sizes.
* **System Fonts:** Prefer system fonts (SF Pro for iOS, Roboto for Android) to ensure maximum legibility and zero load time.

## 4. Mobile Component Standards
* **Rounded Corners:** Use generous border-radii for buttons and cards (8px–16px) for a modern, native feel.
* **Modals & Sheets:** Use bottom sheets for secondary actions instead of full-page transitions to keep user context.
* **Feedback:** Use haptic feedback (vibrations) sparingly for successful or failed critical actions.