/**
 * HistoryScreen — displays completed shopping lists.
 * Reloads on every tab focus; supports item expansion and list reuse.
 */
import { useFocusEffect, useNavigation } from "@react-navigation/native";
import React, { useCallback, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { ShoppingList } from "../../../common/types";
import { BorderRadius, Colors, FontSize, FontWeight, Spacing } from "../../constants/theme";
import { useList } from "../../logic/use-list";
import { useAppStore } from "../../store/app-store";

function HistoryRow({ list, onReuse }: { list: ShoppingList; onReuse: () => void }) {
  const [expanded, setExpanded] = useState(false);
  const date = list.completed_at
    ? new Date(list.completed_at).toLocaleDateString("he-IL")
    : "";

  return (
    <View style={styles.row}>
      <TouchableOpacity style={styles.rowHeader} onPress={() => setExpanded((v) => !v)}>
        <View style={styles.rowInfo}>
          <Text style={styles.listName}>{list.name}</Text>
          <Text style={styles.meta}>{date} · {list.items.length} פריטים</Text>
        </View>
        <TouchableOpacity onPress={onReuse} style={styles.reuseBtn}>
          <Text style={styles.reuseBtnText}>שחזר</Text>
        </TouchableOpacity>
        <Text style={styles.chevron}>{expanded ? "▲" : "▼"}</Text>
      </TouchableOpacity>

      {expanded && (
        <View style={styles.itemsList}>
          {list.items.length === 0
            ? <Text style={styles.noItems}>אין פריטים</Text>
            : list.items.map((item) => (
                <Text key={item.id} style={styles.itemText}>• {item.name_hebrew}</Text>
              ))
          }
        </View>
      )}
    </View>
  );
}

export function HistoryScreen() {
  const history = useAppStore((s) => s.history);
  const isLoading = useAppStore((s) => s.isLoading);
  const userId = useAppStore((s) => s.userId);
  const { loadHistory, reuseList } = useList();
  const navigation = useNavigation<any>();

  // Reload every time this tab comes into focus
  useFocusEffect(
    useCallback(() => {
      if (userId) loadHistory(userId);
    }, [userId])
  );

  async function handleReuse(list: ShoppingList) {
    const result = await reuseList(list);
    if (result) navigation.navigate("List");
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.heading}>היסטוריית קניות</Text>
      {isLoading ? (
        <ActivityIndicator color={Colors.accent} style={styles.loader} />
      ) : (
        <FlatList
          data={history}
          keyExtractor={(l) => l.list_id}
          renderItem={({ item }) => (
            <HistoryRow list={item} onReuse={() => handleReuse(item)} />
          )}
          contentContainerStyle={styles.list}
          ListEmptyComponent={
            <Text style={styles.emptyText}>אין היסטוריית קניות עדיין</Text>
          }
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  heading: { fontSize: FontSize.xl, fontWeight: FontWeight.bold, color: Colors.textPrimary, padding: Spacing.md, textAlign: "right" },
  loader: { marginTop: Spacing.xl },
  list: { paddingHorizontal: Spacing.md, paddingBottom: Spacing.xl },
  row: { backgroundColor: Colors.surface, borderRadius: BorderRadius.md, marginVertical: Spacing.xs, borderWidth: 1, borderColor: Colors.border, overflow: "hidden" },
  rowHeader: { flexDirection: "row", alignItems: "center", padding: Spacing.md },
  rowInfo: { flex: 1 },
  listName: { fontSize: FontSize.md, fontWeight: FontWeight.bold, color: Colors.textPrimary, textAlign: "right" },
  meta: { fontSize: FontSize.xs, color: Colors.textSecondary, marginTop: 2, textAlign: "right" },
  reuseBtn: { backgroundColor: Colors.accent, borderRadius: BorderRadius.sm, paddingHorizontal: Spacing.sm, paddingVertical: 4, marginLeft: Spacing.sm },
  reuseBtnText: { color: Colors.surface, fontSize: FontSize.xs, fontWeight: FontWeight.bold },
  chevron: { color: Colors.textSecondary, fontSize: FontSize.sm, marginLeft: Spacing.sm },
  itemsList: { borderTopWidth: 1, borderTopColor: Colors.border, paddingHorizontal: Spacing.md, paddingVertical: Spacing.sm },
  itemText: { color: Colors.textPrimary, fontSize: FontSize.sm, textAlign: "right", paddingVertical: 2 },
  noItems: { color: Colors.textSecondary, fontSize: FontSize.sm, textAlign: "center" },
  emptyText: { color: Colors.textSecondary, textAlign: "center", marginTop: Spacing.xl },
});
