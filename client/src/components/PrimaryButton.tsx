/**
 * PrimaryButton — logic-free CTA button.
 * Follows FRONTEND_ARCHITECTURE.md: pure presentation, no data fetching.
 * Meets 44pt minimum touch target (MOBILE_NATIVE_FRONT.md).
 */
import React from "react";
import { ActivityIndicator, Pressable, Text } from "react-native";
import { Colors } from "../constants/theme";
import { styles } from "./PrimaryButton.styles";

interface PrimaryButtonProps {
  label: string;
  onPress: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export function PrimaryButton({ label, onPress, disabled = false, loading = false }: PrimaryButtonProps) {
  const isDisabled = disabled || loading;

  return (
    <Pressable
      style={[styles.button, isDisabled && styles.buttonDisabled]}
      onPress={onPress}
      disabled={isDisabled}
      accessibilityRole="button"
      accessibilityLabel={label}
    >
      {loading ? (
        <ActivityIndicator color={Colors.surface} />
      ) : (
        <Text style={[styles.label, isDisabled && styles.labelDisabled]}>{label}</Text>
      )}
    </Pressable>
  );
}
