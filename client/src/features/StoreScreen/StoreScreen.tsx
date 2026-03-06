/**
 * StoreScreen — displays geo-ranked store recommendations for the active list.
 * Reads GPS location via expo-location, fetches ranked stores from the API.
 */
import * as Location from "expo-location";
import React, { useCallback, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { StoreRank } from "../../../common/types";
import { PrimaryButton } from "../../components/PrimaryButton";
import { Colors, BorderRadius, FontSize, FontWeight, Spacing } from "../../constants/theme";
import { fetchStoreRecommendations } from "../../api/store.api";
import { useAppStore } from "../../store/app-store";

function StoreRankCard({ rank, index }: { rank: StoreRank; index: number }) {
  return (
    <View style={styles.card}>
      <Text style={styles.rankBadge}>#{index + 1}</Text>
      <View style={styles.cardBody}>
        <Text style={styles.storeId} numberOfLines={1}>{rank.store_id}</Text>
        <Text style={styles.itemCount}>{rank.item_count} פריטים</Text>
      </View>
      <Text style={styles.cost}>₪{rank.total_basket_cost.toFixed(2)}</Text>
    </View>
  );
}

export function StoreScreen() {
  const [isLoading, setIsLoading] = useState(false);
  const [locationError, setLocationError] = useState<string | null>(null);
  const storeRankings = useAppStore((s) => s.storeRankings);
  const setStoreRankings = useAppStore((s) => s.setStoreRankings);
  const activeList = useAppStore((s) => s.activeList);
  const setError = useAppStore((s) => s.setError);

  const handleFindStores = useCallback(async () => {
    if (!activeList) {
      setError("אין רשימה פעילה");
      return;
    }
    setIsLoading(true);
    setLocationError(null);
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        setLocationError("נדרשת גישה למיקום");
        return;
      }
      const location = await Location.getCurrentPositionAsync({});
      const rankings = await fetchStoreRecommendations(activeList.list_id, {
        latitude: location.coords.latitude,
        longitude: location.coords.longitude,
      });
      setStoreRankings(rankings);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setIsLoading(false);
    }
  }, [activeList, setStoreRankings, setError]);

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.heading}>חנויות קרובות</Text>
      {locationError && <Text style={styles.errorText}>{locationError}</Text>}
      <FlatList
        data={storeRankings}
        keyExtractor={(item) => item.store_id}
        renderItem={({ item, index }) => <StoreRankCard rank={item} index={index} />}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <Text style={styles.emptyText}>לחץ למציאת החנויות הזולות ביותר</Text>
        }
      />
      <View style={styles.buttonRow}>
        <PrimaryButton label="מצא חנויות" onPress={handleFindStores} loading={isLoading} />
      </View>
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
  list: { paddingHorizontal: Spacing.md, paddingBottom: Spacing.xl },
  card: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    marginVertical: Spacing.xs,
    flexDirection: "row",
    alignItems: "center",
  },
  rankBadge: { fontSize: FontSize.lg, fontWeight: FontWeight.bold, color: Colors.accent, width: 36 },
  cardBody: { flex: 1, marginHorizontal: Spacing.sm },
  storeId: { fontSize: FontSize.sm, color: Colors.textSecondary },
  itemCount: { fontSize: FontSize.xs, color: Colors.textSecondary, marginTop: 2 },
  cost: { fontSize: FontSize.lg, fontWeight: FontWeight.bold, color: Colors.textPrimary },
  buttonRow: { padding: Spacing.md },
  errorText: { color: Colors.error, padding: Spacing.md, textAlign: "center" },
  emptyText: { color: Colors.textSecondary, textAlign: "center", marginTop: Spacing.xl },
});
