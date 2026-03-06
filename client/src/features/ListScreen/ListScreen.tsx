/**
 * ListScreen — primary screen; displays the active shopping list.
 * Smart container: delegates all data ops to useList and useSync hooks.
 * UI state only — no direct API calls.
 */
import React, { useEffect } from "react";
import {
  ActivityIndicator,
  FlatList,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { ItemCard } from "../../components/ItemCard";
import { Colors, FontSize, FontWeight, Spacing } from "../../constants/theme";
import { useList } from "../../logic/use-list";
import { usePriceIntel } from "../../logic/use-price-intel";
import { useSync } from "../../logic/use-sync";
import { useAppStore } from "../../store/app-store";

// Placeholder list ID — replaced by navigation params in the full flow
const DEMO_LIST_ID = "00000000-0000-0000-0000-000000000001";

function ItemRow({ itemId, nameHebrew, quantity }: { itemId: string; nameHebrew: string; quantity: number }) {
  const trend = usePriceIntel(itemId);
  return <ItemCard nameHebrew={nameHebrew} quantity={quantity} trend={trend ?? undefined} />;
}

export function ListScreen() {
  const { loadList } = useList();
  const activeList = useAppStore((s) => s.activeList);
  const isLoading = useAppStore((s) => s.isLoading);
  const error = useAppStore((s) => s.error);

  useSync(activeList?.list_id ?? DEMO_LIST_ID);

  useEffect(() => {
    loadList(DEMO_LIST_ID);
  }, []);

  if (isLoading) {
    return (
      <SafeAreaView style={styles.centered}>
        <ActivityIndicator color={Colors.accent} size="large" />
      </SafeAreaView>
    );
  }

  if (error) {
    return (
      <SafeAreaView style={styles.centered}>
        <Text style={styles.errorText}>{error}</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.heading}>הרשימה שלי</Text>
      <FlatList
        data={activeList?.items ?? []}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <ItemRow itemId={item.id} nameHebrew={item.name_hebrew} quantity={item.default_quantity} />
        )}
        contentContainerStyle={styles.list}
        ListEmptyComponent={<Text style={styles.emptyText}>הרשימה ריקה</Text>}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  centered: { flex: 1, alignItems: "center", justifyContent: "center" },
  heading: {
    fontSize: FontSize.xl,
    fontWeight: FontWeight.bold,
    color: Colors.textPrimary,
    padding: Spacing.md,
    textAlign: "right",
  },
  list: { paddingHorizontal: Spacing.md, paddingBottom: Spacing.xl },
  errorText: { color: Colors.error, fontSize: FontSize.md, padding: Spacing.md },
  emptyText: { color: Colors.textSecondary, textAlign: "center", marginTop: Spacing.xl },
});
