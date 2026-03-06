/**
 * HistoryScreen — displays past shopping trips from transaction history.
 * Placeholder: wired to the transaction API endpoint when ready.
 */
import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { Transaction } from "../../../common/types";
import { TransactionSchema } from "../../../common/validation";
import { z } from "zod";
import { Colors, BorderRadius, FontSize, FontWeight, Spacing } from "../../constants/theme";
import { apiClient } from "../../api/client";
import { useAppStore } from "../../store/app-store";

function TransactionRow({ tx }: { tx: Transaction }) {
  const date = new Date(tx.timestamp).toLocaleDateString("he-IL");
  return (
    <View style={styles.row}>
      <View style={styles.rowLeft}>
        <Text style={styles.storeName}>{tx.store_name}</Text>
        <Text style={styles.date}>{date}</Text>
      </View>
      <Text style={styles.price}>₪{tx.price.toFixed(2)}</Text>
    </View>
  );
}

export function HistoryScreen() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const userId = useAppStore((s) => s.userId);
  const setError = useAppStore((s) => s.setError);

  useEffect(() => {
    if (!userId) return;
    setIsLoading(true);
    apiClient
      .get(`/transaction/history`, { params: { user_id: userId } })
      .then(({ data }) => setTransactions(z.array(TransactionSchema).parse(data)))
      .catch((err: Error) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, [userId]);

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.heading}>היסטוריית קניות</Text>
      {isLoading ? (
        <ActivityIndicator color={Colors.accent} style={styles.loader} />
      ) : (
        <FlatList
          data={transactions}
          keyExtractor={(tx) => tx.transaction_id}
          renderItem={({ item }) => <TransactionRow tx={item} />}
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
  heading: {
    fontSize: FontSize.xl,
    fontWeight: FontWeight.bold,
    color: Colors.textPrimary,
    padding: Spacing.md,
    textAlign: "right",
  },
  loader: { marginTop: Spacing.xl },
  list: { paddingHorizontal: Spacing.md, paddingBottom: Spacing.xl },
  row: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    marginVertical: Spacing.xs,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  rowLeft: { flex: 1 },
  storeName: { fontSize: FontSize.md, fontWeight: FontWeight.medium, color: Colors.textPrimary },
  date: { fontSize: FontSize.xs, color: Colors.textSecondary, marginTop: 2 },
  price: { fontSize: FontSize.lg, fontWeight: FontWeight.bold, color: Colors.accent },
  emptyText: { color: Colors.textSecondary, textAlign: "center", marginTop: Spacing.xl },
});
