/**
 * ItemCard — logic-free card displaying a single shopping list item.
 * Follows FRONTEND_ARCHITECTURE.md: pure presentation, no data fetching.
 */
import React from "react";
import { Pressable, Text, View } from "react-native";
import { styles } from "./ItemCard.styles";

interface ItemCardProps {
  nameHebrew: string;
  quantity: number;
  isBought: boolean;
  onMarkBought?: () => void;
  onRemove?: () => void;
}

export function ItemCard({ nameHebrew, quantity, isBought, onMarkBought, onRemove }: ItemCardProps) {
  return (
    <View style={[styles.card, isBought && styles.cardBought]}>
      <Pressable
        style={styles.checkboxArea}
        onPress={onMarkBought}
        accessibilityLabel="סמן כנקנה"
        disabled={isBought}
      >
        <View style={[styles.checkbox, isBought && styles.checkboxChecked]}>
          {isBought && <Text style={styles.checkmark}>✓</Text>}
        </View>
      </Pressable>

      <View style={styles.nameArea}>
        <Text style={[styles.nameText, isBought && styles.nameTextBought]}>{nameHebrew}</Text>
      </View>

      <View style={styles.quantityBadge}>
        <Text style={styles.quantityText}>{quantity}</Text>
      </View>

      {onRemove && (
        <Pressable style={styles.removeBtn} onPress={onRemove} accessibilityLabel="הסר">
          <Text style={styles.removeBtnText}>×</Text>
        </Pressable>
      )}
    </View>
  );
}
