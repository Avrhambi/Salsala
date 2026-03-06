/**
 * AppNavigator — bottom-tab navigation wiring all 4 screens.
 * Thumb-zone placement follows MOBILE_NATIVE_FRONT.md (primary actions at bottom).
 */
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import React from "react";
import { Text } from "react-native";
import { HistoryScreen } from "../features/HistoryScreen/HistoryScreen";
import { ListScreen } from "../features/ListScreen/ListScreen";
import { ScannerScreen } from "../features/ScannerScreen/ScannerScreen";
import { StoreScreen } from "../features/StoreScreen/StoreScreen";
import { Colors, FontSize } from "../constants/theme";

export type RootTabParamList = {
  List: undefined;
  Scanner: undefined;
  Stores: undefined;
  History: undefined;
};

const Tab = createBottomTabNavigator<RootTabParamList>();

const TAB_ICONS: Record<keyof RootTabParamList, string> = {
  List: "🛒",
  Scanner: "📷",
  Stores: "📍",
  History: "📋",
};

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: () => (
            <Text style={{ fontSize: FontSize.lg }}>
              {TAB_ICONS[route.name as keyof RootTabParamList]}
            </Text>
          ),
          tabBarActiveTintColor: Colors.accent,
          tabBarInactiveTintColor: Colors.textSecondary,
          tabBarStyle: { backgroundColor: Colors.surface },
          headerStyle: { backgroundColor: Colors.secondary },
          headerTintColor: Colors.surface,
          headerTitleAlign: "center",
        })}
      >
        <Tab.Screen name="List" component={ListScreen} options={{ title: "הרשימה" }} />
        <Tab.Screen name="Scanner" component={ScannerScreen} options={{ title: "סרוק" }} />
        <Tab.Screen name="Stores" component={StoreScreen} options={{ title: "חנויות" }} />
        <Tab.Screen name="History" component={HistoryScreen} options={{ title: "היסטוריה" }} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
