/**
 * AppNavigator — bottom-tab navigation for the 2 MVP screens.
 */
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import React from "react";
import { Text } from "react-native";
import { HistoryScreen } from "../features/HistoryScreen/HistoryScreen";
import { ListScreen } from "../features/ListScreen/ListScreen";
import { Colors, FontSize } from "../constants/theme";

export type RootTabParamList = {
  List: undefined;
  History: undefined;
};

const Tab = createBottomTabNavigator<RootTabParamList>();

const TAB_ICONS: Record<keyof RootTabParamList, string> = {
  List: "🛒",
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
        <Tab.Screen name="List" component={ListScreen} options={{ title: "הרשימות" }} />
        <Tab.Screen name="History" component={HistoryScreen} options={{ title: "היסטוריה" }} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
