/**
 * CreateListModal — lets the user create a new named list.
 */
import React, { useState } from "react";
import {
  KeyboardAvoidingView,
  Modal,
  Platform,
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { PrimaryButton } from "../../components/PrimaryButton";
import { BorderRadius, Colors, FontSize, FontWeight, Spacing } from "../../constants/theme";
import { useList } from "../../logic/use-list";
import { useAppStore } from "../../store/app-store";

interface Props {
  visible: boolean;
  onClose: () => void;
}

export function CreateListModal({ visible, onClose }: Props) {
  const [tab, setTab] = useState<"create" | "join">("create");
  const [name, setName] = useState("");
  const [joinId, setJoinId] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { startList, loadList } = useList();
  const userId = useAppStore((s) => s.userId);

  function resetAndClose() {
    setName("");
    setJoinId("");
    setLocalError(null);
    onClose();
  }

  async function handleCreate() {
    const trimmed = name.trim();
    if (!trimmed) { setLocalError("הזן שם לרשימה"); return; }
    const duplicate = useAppStore.getState().lists.some(
      (l) => !l.is_completed && l.name.trim().toLowerCase() === trimmed.toLowerCase()
    );
    if (duplicate) { setLocalError("רשימה פעילה עם שם זה כבר קיימת"); return; }
    setLocalError(null);
    setIsSubmitting(true);
    const list = await startList(userId ? [userId] : [], trimmed);
    setIsSubmitting(false);
    if (list) { resetAndClose(); }
    else { setLocalError(useAppStore.getState().error ?? "שגיאה ביצירת הרשימה"); }
  }

  async function handleJoin() {
    const trimmed = joinId.trim();
    if (!trimmed) { setLocalError("הזן מזהה רשימה"); return; }
    setLocalError(null);
    setIsSubmitting(true);
    await loadList(trimmed);
    setIsSubmitting(false);
    const err = useAppStore.getState().error;
    if (err) { setLocalError(err); }
    else { resetAndClose(); }
  }

  return (
    <Modal visible={visible} animationType="fade" transparent onRequestClose={resetAndClose}>
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === "ios" ? "padding" : "height"}
      >
        <Pressable style={styles.overlay} onPress={resetAndClose}>
          <Pressable style={styles.sheet} onPress={() => {}}>
            <View style={styles.tabRow}>
              <TouchableOpacity
                style={[styles.tab, tab === "create" && styles.tabActive]}
                onPress={() => { setTab("create"); setLocalError(null); }}
              >
                <Text style={[styles.tabText, tab === "create" && styles.tabTextActive]}>צור רשימה</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.tab, tab === "join" && styles.tabActive]}
                onPress={() => { setTab("join"); setLocalError(null); }}
              >
                <Text style={[styles.tabText, tab === "join" && styles.tabTextActive]}>הצטרף</Text>
              </TouchableOpacity>
            </View>

            {localError && <Text style={styles.errorText}>{localError}</Text>}

            {tab === "create" ? (
              <TextInput
                style={styles.input}
                placeholder="שם הרשימה..."
                placeholderTextColor={Colors.textSecondary}
                value={name}
                onChangeText={setName}
                onSubmitEditing={handleCreate}
                returnKeyType="done"
                textAlign="right"
                autoFocus
              />
            ) : (
              <TextInput
                style={styles.input}
                placeholder="הדבק מזהה רשימה..."
                placeholderTextColor={Colors.textSecondary}
                value={joinId}
                onChangeText={setJoinId}
                onSubmitEditing={handleJoin}
                returnKeyType="done"
                autoCapitalize="none"
                autoCorrect={false}
                textAlign="left"
              />
            )}

            <PrimaryButton
              label={tab === "create" ? "צור רשימה" : "הצטרף"}
              onPress={tab === "create" ? handleCreate : handleJoin}
              loading={isSubmitting}
            />

            <TouchableOpacity style={styles.cancelBtn} onPress={resetAndClose}>
              <Text style={styles.cancelText}>ביטול</Text>
            </TouchableOpacity>
          </Pressable>
        </Pressable>
      </KeyboardAvoidingView>
    </Modal>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  overlay: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0,0,0,0.5)",
    padding: Spacing.lg,
  },
  sheet: {
    width: "100%",
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.lg,
    gap: Spacing.md,
  },
  title: {
    fontSize: FontSize.lg,
    fontWeight: "700",
    color: Colors.textPrimary,
    textAlign: "center",
  },
  input: {
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: BorderRadius.sm,
    padding: Spacing.md,
    fontSize: FontSize.md,
    color: Colors.textPrimary,
    backgroundColor: Colors.background,
  },
  tabRow: { flexDirection: "row", borderRadius: BorderRadius.sm, overflow: "hidden", borderWidth: 1, borderColor: Colors.border },
  tab: { flex: 1, paddingVertical: Spacing.sm, alignItems: "center", backgroundColor: Colors.background },
  tabActive: { backgroundColor: Colors.accent },
  tabText: { fontSize: FontSize.sm, color: Colors.textSecondary, fontWeight: "600" },
  tabTextActive: { color: Colors.surface },
  cancelBtn: { alignItems: "center", paddingVertical: Spacing.sm },
  cancelText: { color: Colors.textSecondary, fontSize: FontSize.md },
  errorText: { color: Colors.error, fontSize: FontSize.sm, textAlign: "center" },
});
