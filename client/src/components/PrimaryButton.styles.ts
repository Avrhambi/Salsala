import { StyleSheet } from "react-native";
import { BorderRadius, Colors, FontSize, FontWeight, MIN_TOUCH_TARGET, Spacing } from "../constants/theme";

export const styles = StyleSheet.create({
  button: {
    backgroundColor: Colors.accent,
    borderRadius: BorderRadius.md,
    minHeight: MIN_TOUCH_TARGET,
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.sm,
    alignItems: "center",
    justifyContent: "center",
  },
  buttonDisabled: {
    backgroundColor: Colors.border,
  },
  label: {
    color: Colors.surface,
    fontSize: FontSize.md,
    fontWeight: FontWeight.bold,
  },
  labelDisabled: {
    color: Colors.textSecondary,
  },
});
