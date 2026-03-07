import { StyleSheet } from "react-native";
import { BorderRadius, Colors, FontSize, FontWeight, Spacing } from "../constants/theme";

export const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    marginVertical: Spacing.xs,
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 1,
    borderColor: Colors.border,
    gap: Spacing.sm,
  },
  cardBought: {
    opacity: 0.55,
  },
  checkboxArea: {
    padding: Spacing.xs,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: BorderRadius.sm,
    borderWidth: 2,
    borderColor: Colors.accent,
    alignItems: "center",
    justifyContent: "center",
  },
  checkboxChecked: {
    backgroundColor: Colors.success,
    borderColor: Colors.success,
  },
  checkmark: {
    color: Colors.surface,
    fontSize: FontSize.sm,
    fontWeight: FontWeight.bold,
  },
  nameArea: {
    flex: 1,
  },
  nameText: {
    fontSize: FontSize.md,
    fontWeight: FontWeight.medium,
    color: Colors.textPrimary,
    textAlign: "right",
  },
  nameTextBought: {
    textDecorationLine: "line-through",
    color: Colors.textSecondary,
  },
  quantityBadge: {
    backgroundColor: Colors.accentLight,
    borderRadius: BorderRadius.sm,
    paddingHorizontal: Spacing.sm,
    paddingVertical: Spacing.xs,
    minWidth: 32,
    alignItems: "center",
  },
  quantityText: {
    fontSize: FontSize.sm,
    fontWeight: FontWeight.bold,
    color: Colors.accent,
  },
  removeBtn: {
    backgroundColor: Colors.error,
    borderRadius: BorderRadius.sm,
    width: 32,
    height: 32,
    alignItems: "center",
    justifyContent: "center",
  },
  removeBtnText: {
    color: Colors.surface,
    fontSize: FontSize.lg,
    fontWeight: FontWeight.bold,
  },
});
