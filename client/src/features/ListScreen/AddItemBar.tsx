/**
 * AddItemBar — plain text input for adding items to the active list.
 * Submit on the keyboard "Done" action or the Add button.
 */
import React, { useState } from "react";
import { StyleSheet, TextInput, TouchableOpacity, Text, View } from "react-native";
import { BorderRadius, Colors, FontSize, Spacing } from "../../constants/theme";
import { useList } from "../../logic/use-list";

interface Props {
  listId: string;
}

export function AddItemBar({ listId }: Props) {
  const [text, setText] = useState("");
  const { addItem } = useList();

  async function handleAdd() {
    const trimmed = text.trim();
    if (!trimmed) return;
    setText("");
    await addItem(listId, trimmed, 1);
  }

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="הוסף פריט..."
        value={text}
        onChangeText={setText}
        onSubmitEditing={handleAdd}
        returnKeyType="done"
        textAlign="right"
      />
      <TouchableOpacity style={styles.addBtn} onPress={handleAdd} accessibilityLabel="הוסף">
        <Text style={styles.addBtnText}>+</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    marginHorizontal: Spacing.md,
    marginBottom: Spacing.sm,
    gap: Spacing.sm,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: BorderRadius.sm,
    padding: Spacing.md,
    fontSize: FontSize.md,
    backgroundColor: Colors.surface,
    color: Colors.textPrimary,
  },
  addBtn: {
    backgroundColor: Colors.accent,
    borderRadius: BorderRadius.sm,
    width: 48,
    alignItems: "center",
    justifyContent: "center",
  },
  addBtnText: {
    color: Colors.surface,
    fontSize: FontSize.xl,
    fontWeight: "700",
  },
});
