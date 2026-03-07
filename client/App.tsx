import React, { useEffect, useState } from "react";
import { ActivityIndicator, View } from "react-native";
import { AppNavigator } from "./src/navigation/AppNavigator";
import { createUser } from "./src/api/user.api";
import { useAppStore } from "./src/store/app-store";

export default function App() {
  const setUserId = useAppStore((s) => s.setUserId);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    createUser("Anonymous")
      .then((user) => setUserId(user.user_id))
      .catch((err) => console.error("createUser failed:", err))
      .finally(() => setReady(true));
  }, []);

  if (!ready) {
    return <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}><ActivityIndicator /></View>;
  }

  return <AppNavigator />;
}
