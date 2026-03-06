/**
 * ItemCard — logic-free card displaying a single shopping list item.
 * Follows FRONTEND_ARCHITECTURE.md: pure presentation, no data fetching.
 */
import React from "react";
import { Pressable, Text, View } from "react-native";
import { TrendValue } from "../../common/types";
import { Colors } from "../constants/theme";
import { styles } from "./ItemCard.styles";

interface ItemCardProps {
  nameHebrew: string;
  quantity: number;
  trend?: TrendValue;
  onPress?: () => void;
}

const TREND_COLOR: Record<TrendValue, string> = {
  [TrendValue.UP]: Colors.error,
  [TrendValue.DOWN]: Colors.success,
  [TrendValue.STABLE]: Colors.textSecondary,
  [TrendValue.NA]: Colors.textSecondary,
};

const TREND_LABEL: Record<TrendValue, string> = {
  [TrendValue.UP]: "↑",
  [TrendValue.DOWN]: "↓",
  [TrendValue.STABLE]: "→",
  [TrendValue.NA]: "",
};

export function ItemCard({ nameHebrew, quantity, trend, onPress }: ItemCardProps) {
  return (
    <Pressable style={styles.card} onPress={onPress} accessibilityRole="button">
      <Text style={styles.nameText}>{nameHebrew}</Text>
      {trend && trend !== TrendValue.NA && (
        <Text style={[styles.trendText, { color: TREND_COLOR[trend] }]}>
          {TREND_LABEL[trend]}
        </Text>
      )}
      <View style={styles.quantityBadge}>
        <Text style={styles.quantityText}>{quantity}</Text>
      </View>
    </Pressable>
  );
}
