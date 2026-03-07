/**
 * ListScreen — shows all user lists; tap a list to view/manage its items.
 */
import React, { useState } from "react";
import {
  Alert,
  FlatList,
  SafeAreaView,
  Share,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { ShoppingList } from "../../../common/types";
import { ItemCard } from "../../components/ItemCard";
import { PrimaryButton } from "../../components/PrimaryButton";
import { Colors, BorderRadius, FontSize, FontWeight, Spacing } from "../../constants/theme";
import { useList } from "../../logic/use-list";
import { useAppStore } from "../../store/app-store";
import { AddItemBar } from "./AddItemBar";
import { CreateListModal } from "./CreateListModal";

function shareList(list: ShoppingList) {
  Share.share({
    message: `הצטרפ/י לרשימת הקניות שלי "${list.name}"!\nמזהה: ${list.list_id}`,
  });
}

function ListRow({
  list,
  onOpen,
  onDelete,
}: {
  list: ShoppingList;
  onOpen: () => void;
  onDelete: () => void;
}) {
  return (
    <TouchableOpacity style={styles.listRow} onPress={onOpen}>
      <View style={styles.listRowContent}>
        <Text style={styles.listName}>{list.name}</Text>
        <Text style={styles.listMeta}>{list.items.length} פריטים</Text>
      </View>
      <TouchableOpacity onPress={() => shareList(list)} style={styles.shareBtn} accessibilityLabel="שתף רשימה">
        <Text style={styles.shareBtnText}>שתף</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={onDelete} style={styles.deleteBtn} accessibilityLabel="מחק רשימה">
        <Text style={styles.deleteBtnText}>🗑</Text>
      </TouchableOpacity>
    </TouchableOpacity>
  );
}

function ActiveListView({ list }: { list: ShoppingList }) {
  const { removeItem, markBought, rename } = useList();
  const setActiveList = useAppStore((s) => s.setActiveList);

  function handleRename() {
    Alert.prompt("שנה שם", "שם חדש לרשימה:", async (newName) => {
      if (newName?.trim()) await rename(list.list_id, newName.trim());
    });
  }

  return (
    <>
      <View style={styles.activeHeader}>
        <TouchableOpacity onPress={() => setActiveList(null)} style={styles.backBtn}>
          <Text style={styles.backBtnText}>← חזרה</Text>
        </TouchableOpacity>
        <Text style={styles.activeTitle}>{list.name}</Text>
        <TouchableOpacity onPress={handleRename} style={styles.headerBtn}>
          <Text style={styles.headerBtnText}>✏️</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => shareList(list)} style={styles.headerBtn}>
          <Text style={styles.headerBtnText}>שתף</Text>
        </TouchableOpacity>
      </View>

      <AddItemBar listId={list.list_id} />

      <FlatList
        data={list.items}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <ItemCard
            nameHebrew={item.name_hebrew}
            quantity={item.default_quantity}
            isBought={item.is_bought}
            onMarkBought={() => markBought(list.list_id, item.id)}
            onRemove={() => removeItem(list.list_id, item.id)}
          />
        )}
        contentContainerStyle={styles.itemList}
        ListEmptyComponent={<Text style={styles.emptyText}>הרשימה ריקה — הוסף פריט למעלה</Text>}
      />
    </>
  );
}

export function ListScreen() {
  const lists = useAppStore((s) => s.lists);
  const activeList = useAppStore((s) => s.activeList);
  const setActiveList = useAppStore((s) => s.setActiveList);
  const isLoading = useAppStore((s) => s.isLoading);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const { remove } = useList();

  function handleDelete(list: ShoppingList) {
    Alert.alert("מחק רשימה", `האם למחוק את "${list.name}"?`, [
      { text: "ביטול", style: "cancel" },
      { text: "מחק", style: "destructive", onPress: () => remove(list.list_id) },
    ]);
  }

  if (activeList) {
    return (
      <SafeAreaView style={styles.container}>
        <ActiveListView list={activeList} />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.heading}>הרשימות שלי</Text>
        <TouchableOpacity onPress={() => setShowCreateModal(true)} style={styles.addListBtn}>
          <Text style={styles.addListBtnText}>+ רשימה</Text>
        </TouchableOpacity>
      </View>

      {isLoading ? (
        <Text style={styles.loadingText}>טוען...</Text>
      ) : (
        <FlatList
          data={lists.filter((l) => !l.is_completed)}
          keyExtractor={(l) => l.list_id}
          renderItem={({ item }) => (
            <ListRow
              list={item}
              onOpen={() => setActiveList(item)}
              onDelete={() => handleDelete(item)}
            />
          )}
          contentContainerStyle={styles.outerList}
          ListEmptyComponent={
            <View style={styles.centered}>
              <Text style={styles.emptyStateText}>אין רשימות עדיין</Text>
              <PrimaryButton label="צור רשימה" onPress={() => setShowCreateModal(true)} />
            </View>
          }
        />
      )}

      <CreateListModal visible={showCreateModal} onClose={() => setShowCreateModal(false)} />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    padding: Spacing.md,
  },
  heading: { fontSize: FontSize.xl, fontWeight: FontWeight.bold, color: Colors.textPrimary },
  addListBtn: {
    backgroundColor: Colors.accent,
    borderRadius: BorderRadius.sm,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
  },
  addListBtnText: { color: Colors.surface, fontWeight: FontWeight.bold, fontSize: FontSize.md },
  outerList: { paddingHorizontal: Spacing.md, paddingBottom: Spacing.xl },
  listRow: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.md,
    padding: Spacing.md,
    marginVertical: Spacing.xs,
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 1,
    borderColor: Colors.border,
  },
  listRowContent: { flex: 1 },
  listName: { fontSize: FontSize.md, fontWeight: FontWeight.bold, color: Colors.textPrimary },
  listMeta: { fontSize: FontSize.xs, color: Colors.textSecondary, marginTop: 2 },
  shareBtn: { paddingHorizontal: Spacing.sm, paddingVertical: Spacing.xs, marginRight: Spacing.xs },
  shareBtnText: { color: Colors.accent, fontSize: FontSize.sm, fontWeight: FontWeight.bold },
  deleteBtn: { padding: Spacing.sm },
  deleteBtnText: { fontSize: FontSize.lg },
  activeHeader: {
    flexDirection: "row",
    alignItems: "center",
    padding: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  backBtn: { marginRight: Spacing.md },
  backBtnText: { color: Colors.accent, fontSize: FontSize.md },
  activeTitle: { flex: 1, fontSize: FontSize.lg, fontWeight: FontWeight.bold, color: Colors.textPrimary, textAlign: "center" },
  headerBtn: { padding: Spacing.xs, marginLeft: Spacing.xs },
  headerBtnText: { fontSize: FontSize.md, color: Colors.accent },
  itemList: { paddingHorizontal: Spacing.md, paddingBottom: Spacing.xl },
  centered: { flex: 1, alignItems: "center", justifyContent: "center", paddingTop: Spacing.xl },
  emptyStateText: { color: Colors.textSecondary, fontSize: FontSize.lg, marginBottom: Spacing.lg },
  emptyText: { color: Colors.textSecondary, textAlign: "center", marginTop: Spacing.xl },
  loadingText: { color: Colors.textSecondary, textAlign: "center", marginTop: Spacing.xl },
});
