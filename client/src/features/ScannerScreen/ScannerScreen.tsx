/**
 * ScannerScreen — camera-based receipt OCR upload.
 * Uses expo-camera to capture the image, then delegates to receipt.api.ts.
 * Smart container: logic in hook, UI stays dumb.
 */
import { CameraView, useCameraPermissions } from "expo-camera";
import React, { useRef, useState } from "react";
import {
  ActivityIndicator,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { PrimaryButton } from "../../components/PrimaryButton";
import { Colors, FontSize, FontWeight, Spacing } from "../../constants/theme";
import { uploadReceipt } from "../../api/receipt.api";
import { useAppStore } from "../../store/app-store";

export function ScannerScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [isUploading, setIsUploading] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const cameraRef = useRef<CameraView>(null);
  const setError = useAppStore((s) => s.setError);

  const handleCapture = async () => {
    if (!cameraRef.current) return;
    setIsUploading(true);
    setStatusMessage(null);
    try {
      const photo = await cameraRef.current.takePictureAsync({ quality: 0.8 });
      if (!photo?.uri) throw new Error("Camera did not return an image.");
      const receipt = await uploadReceipt(photo.uri);
      const message = receipt.requires_human_verification
        ? "נדרשת אימות ידני"
        : `נסרקו ${receipt.parsed_items.length} פריטים בהצלחה`;
      setStatusMessage(message);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setIsUploading(false);
    }
  };

  if (!permission) return <View style={styles.centered} />;

  if (!permission.granted) {
    return (
      <SafeAreaView style={styles.centered}>
        <Text style={styles.permissionText}>נדרשת גישה למצלמה</Text>
        <PrimaryButton label="אפשר גישה" onPress={requestPermission} />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.heading}>סרוק קבלה</Text>
      <CameraView ref={cameraRef} style={styles.camera} facing="back" />
      {statusMessage && <Text style={styles.statusText}>{statusMessage}</Text>}
      <View style={styles.buttonRow}>
        <PrimaryButton label="צלם" onPress={handleCapture} loading={isUploading} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  centered: { flex: 1, alignItems: "center", justifyContent: "center", gap: Spacing.md },
  heading: {
    fontSize: FontSize.xl,
    fontWeight: FontWeight.bold,
    color: Colors.textPrimary,
    padding: Spacing.md,
    textAlign: "right",
  },
  camera: { flex: 1, marginHorizontal: Spacing.md, borderRadius: 12 },
  statusText: {
    color: Colors.success,
    fontSize: FontSize.md,
    textAlign: "center",
    padding: Spacing.sm,
  },
  buttonRow: { padding: Spacing.md },
  permissionText: { color: Colors.textPrimary, fontSize: FontSize.md, marginBottom: Spacing.md },
});
